#!/usr/bin/env python3
"""
Session Getter para Cloudflare Bypass - Fase 1: Motor de Interacción
=====================================================================
Script asíncrono con nodriver para obtener sesión válida de Cloudflare.

Optimizado para Raspberry Pi 4 ARM64 (4GB RAM):
- Usa Chromium del sistema (/usr/bin/chromium-browser)
- Xvfb para simular display sin pantalla física
- Comportamiento humano para pasar Turnstile
- Extrae cookies cf_clearance y User-Agent

Uso:
    python3 session_getter.py --url "https://site.fourvenues.com/es/luminata-disco/events"
    python3 session_getter.py  # Usa URL por defecto
"""

import asyncio
import json
import os
import sys
import time
import random
import argparse
import platform
from pathlib import Path
from typing import Optional, Dict, Any

# Intentar importar nodriver
try:
    import nodriver as uc
except ImportError:
    print("❌ Error: nodriver no está instalado")
    print("   Instalar con: pip install nodriver")
    sys.exit(1)

# Intentar importar pyvirtualdisplay (solo necesario en Linux sin display)
VIRTUAL_DISPLAY = None
if platform.system() == 'Linux' and not os.environ.get('DISPLAY'):
    try:
        from pyvirtualdisplay import Display
        VIRTUAL_DISPLAY = Display
    except ImportError:
        print("⚠️ Warning: pyvirtualdisplay no instalado, Xvfb no disponible")
        print("   Instalar con: pip install pyvirtualdisplay")
        print("   Y asegurar que Xvfb está instalado: sudo apt install xvfb")

# Configuración
DEFAULT_URL = "https://site.fourvenues.com/es/luminata-disco/events"
SESSION_FILE = Path(__file__).parent / "session.json"
COOKIE_TTL_HOURS = 8  # Tiempo de vida de la cookie cf_clearance


def get_chromium_path() -> Optional[str]:
    """
    Busca el ejecutable de Chromium en el sistema.
    Prioriza el Chromium del sistema para ARM64.
    """
    if platform.system() == 'Linux':
        # Rutas comunes en Linux/Raspberry Pi
        linux_paths = [
            '/usr/bin/chromium-browser',  # Raspberry Pi OS
            '/usr/bin/chromium',          # Algunas distros
            '/usr/bin/google-chrome',     # Chrome
            '/snap/bin/chromium',         # Snap
        ]
        for path in linux_paths:
            if os.path.exists(path):
                return path
    
    elif platform.system() == 'Windows':
        localappdata = os.environ.get('LOCALAPPDATA', '')
        chrome_paths = [
            os.path.join(localappdata, 'Google', 'Chrome', 'Application', 'chrome.exe'),
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
    
    elif platform.system() == 'Darwin':
        mac_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
        ]
        for path in mac_paths:
            if os.path.exists(path):
                return path
    
    return None


async def simulate_human_behavior(page) -> None:
    """
    Simula comportamiento humano para pasar detección de bots.
    Incluye movimientos de ratón aleatorios y scrolls.
    """
    try:
        # Espera aleatoria inicial (como haría un humano)
        await asyncio.sleep(random.uniform(1.5, 3.0))
        
        # Movimientos de ratón aleatorios (varios puntos)
        for _ in range(random.randint(2, 4)):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            try:
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.3, 0.8))
            except Exception:
                pass
        
        # Scroll suave (simula lectura de página)
        try:
            await page.evaluate("window.scrollBy(0, 100)")
            await asyncio.sleep(random.uniform(0.5, 1.0))
            await page.evaluate("window.scrollBy(0, -50)")
        except Exception:
            pass
        
        # Espera adicional aleatoria
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
    except Exception as e:
        # No es crítico si falla, continuar
        print(f"   ⚠️ Comportamiento humano parcial: {e}")


async def wait_for_cloudflare_resolution(page, timeout: int = 90) -> bool:
    """
    Espera a que se resuelva el challenge de Cloudflare.
    
    Args:
        page: Página del navegador
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        bool: True si el challenge se resolvió
    """
    print("⏳ Resolviendo challenge de Cloudflare...")
    
    start_time = time.time()
    last_status = ""
    
    while (time.time() - start_time) < timeout:
        await asyncio.sleep(1)
        
        try:
            title = await page.evaluate("document.title") or ""
            body_length = await page.evaluate("document.body.innerHTML.length")
        except Exception:
            title = ""
            body_length = 0
        
        # Palabras clave que indican challenge activo
        challenge_keywords = [
            'momento', 'checking', 'just', 'hang', 'wait', 
            'sec', 'cloudflare', 'verifying', 'loading'
        ]
        
        is_challenge = any(kw in title.lower() for kw in challenge_keywords)
        
        # Status para debug
        elapsed = int(time.time() - start_time)
        status = f"[{elapsed}s] Título: {title[:40]}..." if len(title) > 40 else f"[{elapsed}s] Título: {title}"
        
        if status != last_status and elapsed % 10 == 0:
            print(f"   {status}")
            last_status = status
        
        # Challenge resuelto si:
        # 1. El título no contiene palabras de challenge
        # 2. La página tiene contenido sustancial
        if not is_challenge and body_length > 2000:
            print(f"✅ Challenge resuelto en {elapsed}s - Título: {title[:50]}")
            return True
        
        # Simular comportamiento humano periódicamente
        if elapsed % 15 == 0 and elapsed > 0:
            await simulate_human_behavior(page)
    
    print(f"❌ Timeout después de {timeout}s esperando Cloudflare")
    return False


def extract_cookies_from_page(cookies: list) -> Dict[str, str]:
    """
    Extrae las cookies relevantes de Cloudflare.
    
    Args:
        cookies: Lista de cookies del navegador
    
    Returns:
        dict: Diccionario con las cookies importantes
    """
    cf_cookies = {}
    
    # Cookies de Cloudflare a buscar
    target_cookies = ['cf_clearance', '__cf_bm', 'cf_chl_rc', '__cflb']
    
    for cookie in cookies:
        name = cookie.get('name', '')
        if name in target_cookies:
            cf_cookies[name] = cookie.get('value', '')
    
    return cf_cookies


async def get_session(url: str = DEFAULT_URL, max_retries: int = 3) -> Optional[Dict[str, Any]]:
    """
    Obtiene una sesión válida de Cloudflare.
    
    Args:
        url: URL del sitio objetivo
        max_retries: Número máximo de reintentos
    
    Returns:
        dict: Datos de sesión o None si falla
    """
    is_arm = platform.machine().lower() in ('aarch64', 'arm64', 'armv7l')
    is_linux = platform.system() == 'Linux'
    
    # Iniciar display virtual si es necesario (Linux sin display)
    display = None
    if is_linux and VIRTUAL_DISPLAY and not os.environ.get('DISPLAY'):
        try:
            display = VIRTUAL_DISPLAY(visible=0, size=(1920, 1080))
            display.start()
            print("📺 Display virtual Xvfb iniciado (1920x1080)")
        except Exception as e:
            print(f"⚠️ No se pudo iniciar Xvfb: {e}")
            print("   Intentando sin display virtual...")
    
    chrome_path = get_chromium_path()
    if not chrome_path:
        print("❌ No se encontró Chromium/Chrome en el sistema")
        return None
    
    print(f"🌐 URL objetivo: {url}")
    print(f"🔧 Chromium: {chrome_path}")
    if is_arm:
        print("📱 Modo ARM64 detectado - configuración optimizada para Raspberry Pi")
    
    # Argumentos del navegador
    browser_args = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-setuid-sandbox',
        '--disable-extensions',
        '--window-size=1920,1080',
        '--no-first-run',
        '--no-default-browser-check',
    ]
    
    # Optimizaciones adicionales para ARM64
    if is_arm:
        browser_args.extend([
            '--disable-accelerated-2d-canvas',
            '--disable-software-rasterizer',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--memory-pressure-off',
        ])
    
    session_data = None
    
    for attempt in range(max_retries):
        browser = None
        
        try:
            if attempt > 0:
                wait_time = 5 * (attempt + 1)
                print(f"\n⏳ Reintento {attempt + 1}/{max_retries} (esperando {wait_time}s)...")
                await asyncio.sleep(wait_time)
                
                # Limpiar procesos zombie en ARM
                if is_arm:
                    os.system("pkill -9 -f 'chrome.*--remote-debugging' 2>/dev/null")
                    await asyncio.sleep(1)
            
            print(f"\n🚀 Iniciando navegador (intento {attempt + 1}/{max_retries})...")
            
            # Crear directorio temporal para el perfil
            import tempfile
            user_data_dir = os.path.join(tempfile.gettempdir(), f'nodriver_session_{attempt}')
            
            browser = await uc.start(
                headless=False,  # Headless=False con Xvfb evita detección
                browser_executable_path=chrome_path,
                browser_args=browser_args,
                user_data_dir=user_data_dir,
                port=9222 + attempt,  # Puerto diferente por intento
            )
            
            # Espera adicional en ARM
            if is_arm:
                print("   Estabilizando navegador en ARM (8s)...")
                await asyncio.sleep(8)
            else:
                await asyncio.sleep(2)
            
            print("   ✅ Navegador iniciado")
            
            # Navegar a la URL
            print(f"   Navegando a {url}...")
            page = await browser.get(url)
            
            # Simular comportamiento humano inicial
            await simulate_human_behavior(page)
            
            # Esperar resolución de Cloudflare
            if not await wait_for_cloudflare_resolution(page, timeout=90):
                print("   ❌ No se pudo resolver el challenge")
                continue
            
            # Esperar un poco más para asegurar que las cookies están establecidas
            await asyncio.sleep(3)
            
            # Extraer cookies
            try:
                all_cookies = await page.browser.cookies.get_all()
            except Exception:
                # Método alternativo
                all_cookies = await page.evaluate("""
                    document.cookie.split(';').map(c => {
                        const [name, value] = c.trim().split('=');
                        return {name, value};
                    })
                """)
            
            cf_cookies = extract_cookies_from_page(all_cookies)
            
            if not cf_cookies.get('cf_clearance'):
                print("   ⚠️ No se encontró cf_clearance, reintentando...")
                continue
            
            # Obtener User-Agent
            user_agent = await page.evaluate("navigator.userAgent")
            
            # Construir datos de sesión
            current_time = int(time.time())
            session_data = {
                "cookies": cf_cookies,
                "user_agent": user_agent,
                "url": url,
                "created_at": current_time,
                "expires_at": current_time + (COOKIE_TTL_HOURS * 3600),
                "chromium_version": user_agent.split('Chrome/')[1].split()[0] if 'Chrome/' in user_agent else "unknown"
            }
            
            print(f"\n✅ Sesión obtenida exitosamente!")
            print(f"   📦 Cookies: {list(cf_cookies.keys())}")
            print(f"   🌐 User-Agent: {user_agent[:60]}...")
            print(f"   ⏰ Válida por: {COOKIE_TTL_HOURS} horas")
            
            break
            
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {str(e)[:100]}")
            if attempt == max_retries - 1:
                import traceback
                traceback.print_exc()
        
        finally:
            # Cerrar navegador inmediatamente para liberar recursos
            if browser:
                try:
                    browser.stop()
                    print("   🧹 Navegador cerrado")
                except Exception:
                    pass
    
    # Cerrar display virtual
    if display:
        try:
            display.stop()
            print("📺 Display virtual cerrado")
        except Exception:
            pass
    
    return session_data


def save_session(session_data: Dict[str, Any], filepath: Path = SESSION_FILE) -> bool:
    """
    Guarda los datos de sesión en un archivo JSON.
    
    Args:
        session_data: Datos de la sesión
        filepath: Ruta del archivo de salida
    
    Returns:
        bool: True si se guardó correctamente
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)
        print(f"💾 Sesión guardada en: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error guardando sesión: {e}")
        return False


def load_session(filepath: Path = SESSION_FILE) -> Optional[Dict[str, Any]]:
    """
    Carga los datos de sesión desde un archivo JSON.
    
    Args:
        filepath: Ruta del archivo
    
    Returns:
        dict: Datos de sesión o None si no existe/expiró
    """
    if not filepath.exists():
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar si ha expirado
        if data.get('expires_at', 0) < time.time():
            print("⚠️ Sesión expirada")
            return None
        
        return data
    except Exception as e:
        print(f"⚠️ Error cargando sesión: {e}")
        return None


def is_session_valid(filepath: Path = SESSION_FILE) -> bool:
    """
    Verifica si existe una sesión válida.
    
    Args:
        filepath: Ruta del archivo de sesión
    
    Returns:
        bool: True si la sesión es válida
    """
    session = load_session(filepath)
    return session is not None and 'cf_clearance' in session.get('cookies', {})


async def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description='Obtiene sesión de Cloudflare para bypass'
    )
    parser.add_argument(
        '--url', '-u',
        default=DEFAULT_URL,
        help=f'URL objetivo (default: {DEFAULT_URL})'
    )
    parser.add_argument(
        '--output', '-o',
        default=str(SESSION_FILE),
        help=f'Archivo de salida (default: {SESSION_FILE})'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Forzar nueva sesión aunque exista una válida'
    )
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Solo verificar si existe sesión válida'
    )
    
    args = parser.parse_args()
    output_path = Path(args.output)
    
    print("=" * 60)
    print("PartyFinder - Session Getter (Fase 1)")
    print("=" * 60)
    
    # Solo verificar
    if args.check:
        if is_session_valid(output_path):
            session = load_session(output_path)
            remaining = (session['expires_at'] - time.time()) / 3600
            print(f"✅ Sesión válida encontrada (expira en {remaining:.1f}h)")
            return 0
        else:
            print("❌ No hay sesión válida")
            return 1
    
    # Verificar si ya existe sesión válida (a menos que --force)
    if not args.force and is_session_valid(output_path):
        session = load_session(output_path)
        remaining = (session['expires_at'] - time.time()) / 3600
        print(f"✅ Sesión válida existente (expira en {remaining:.1f}h)")
        print("   Usa --force para obtener nueva sesión")
        return 0
    
    # Obtener nueva sesión
    session = await get_session(args.url)
    
    if session:
        save_session(session, output_path)
        return 0
    else:
        print("\n❌ No se pudo obtener la sesión")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
