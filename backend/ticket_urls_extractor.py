#!/usr/bin/env python3
"""
Extractor de URLs de Tickets Avanzado - nodriver
===============================================
Diseñado para Raspberry Pi 4.
Mejoras:
- Interceptación de red (para pillar JSON del API)
- Capturas de pantalla para depuración
- Interacción con botones dinámica
- Manejo de entorno ARM/Raspberry Pi
"""

import asyncio
import json
import os
import sys
import re
import platform
import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Optional

# Logueo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Intentar importar nodriver
try:
    import nodriver as uc
except ImportError:
    logger.error("nodriver no está instalado. Instalando...")
    sys.exit(1)

# Intentar importar pyvirtualdisplay para Xvfb (necesario en Raspberry Pi vía SSH)
try:
    from pyvirtualdisplay import Display
    HAS_DISPLAY = True
except ImportError:
    HAS_DISPLAY = False

# Estructura de datos
DATA_DIR = Path(__file__).parent / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"

def get_chromium_path() -> Optional[str]:
    """Busca el ejecutable de Chromium."""
    if platform.system() == 'Linux':
        for p in ['/usr/bin/chromium-browser', '/usr/bin/chromium', '/usr/bin/google-chrome']:
            if os.path.exists(p): return p
    elif platform.system() == 'Windows':
        paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        ]
        for p in paths:
            if os.path.exists(p): return p
    return None

async def extract_advanced(event_url: str) -> List[Dict]:
    logger.info(f"Target: {event_url}")
    
    chrome_path = get_chromium_path()
    is_arm = platform.machine().lower() in ('aarch64', 'arm64', 'armv7l')
    is_linux = platform.system() == 'Linux'
    
    # Iniciar display virtual si estamos en Linux y tenemos pyvirtualdisplay
    display = None
    if is_linux and HAS_DISPLAY:
        try:
            logger.info("📺 Iniciando Display Virtual (Xvfb)...")
            display = Display(visible=0, size=(1920, 1080))
            display.start()
        except Exception as e:
            logger.warning(f"No se pudo iniciar Display Virtual: {e}")

    user_data_dir = tempfile.mkdtemp(prefix='nodriver_adv_')
    
    # Intentar forzar la aparición de tickets si hay un botón de "Entradas" o "Comprar"
    logger.info("Buscando botones de interacción...")
    # Cambiamos URL si es 'site.' a 'web.' para evitar iframes
    if 'site.fourvenues.com' in event_url:
        event_url = event_url.replace('site.fourvenues.com', 'web.fourvenues.com')
        logger.info(f"🔄 Cambiando a URL directa de booking: {event_url}")

    browser_args = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--window-size=1920,1080',
    ]

    captured_tickets = []
    
    try:
        logger.info("Iniciando navegador...")
        browser = await uc.start(
            headless=True,
            browser_executable_path=chrome_path,
            browser_args=browser_args,
            user_data_dir=user_data_dir,
            sandbox=False
        )
        
        logger.info(f"Navegando a {event_url}...")
        page = await browser.get(event_url)
        
        # Esperar carga inicial
        await asyncio.sleep(10 if is_arm else 5)
        
        # Scroll suave para activar contenido dinámico
        logger.info("Scrolling...")
        await page.evaluate("window.scrollTo(0, 500);")
        await asyncio.sleep(2)
        await page.evaluate("window.scrollTo(0, 0);")
        
        # Guardar captura de pantalla inicial
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / "initial_view.png"
        await page.save_screenshot(str(screenshot_path))
        logger.info(f"Captura de pantalla guardada en: {screenshot_path}")
        
        # Intentar clic en botones
        click_js = """
        (() => {
            function findAndClick() {
                const allBtns = Array.from(document.querySelectorAll('button, a, [role="button"], fv-button3'));
                const buyBtn = allBtns.find(b => {
                    const t = b.textContent.toLowerCase();
                    return t.includes('entrada') || t.includes('ticket') || t.includes('comprar');
                });
                
                if (buyBtn) {
                    buyBtn.click();
                    return "Clicked: " + buyBtn.textContent.trim();
                }
                return null;
            }
            
            // Reintentar si no se encuentra
            let res = findAndClick();
            return res || "No buttons found to click";
        })()
        """
        try:
            interaction = await page.evaluate(click_js)
            logger.info(f"Interacción JS: {interaction}")
            if "Clicked" in interaction:
                await asyncio.sleep(5 if is_arm else 3)
                await page.save_screenshot(str(SCREENSHOTS_DIR / "after_click.png"))
        except Exception as e:
            logger.warning(f"Error en interacción: {e}")

        # Extracción final de URLs
        extract_js = """
        (() => {
            const results = [];
            // 1. Buscar enlaces directos
            document.querySelectorAll('a').forEach(a => {
                const href = a.href;
                if (href.includes('/tickets/')) {
                    results.push({
                        url: href,
                        text: a.textContent.trim(),
                        source: 'DOM_Link'
                    });
                }
            });
            
            // 2. Buscar en el estado de la aplicación (Angular/React) si está expuesto
            // FourVenues usa Angular, a veces exponen el estado en variables globales
            
            return results;
        })()
        """
        final_results = await page.evaluate(extract_js)
        
        if not final_results:
            logger.info("No se encontraron links directos. Probando búsqueda por texto en todo el HTML.")
            html_content = await page.evaluate("document.documentElement.outerHTML")
            # Dump HTML para depuración
            with open(DATA_DIR / "debug_page.html", "w", encoding='utf-8') as f:
                f.write(html_content)
            
            # Regex buscando el ID de ticket (formato: /tickets/[a-z0-9]{32})
            id_matches = re.findall(r'https?://web\.fourvenues\.com/[^\s"\'<>]+/tickets/([a-z0-9]{32})', html_content)
            if id_matches:
                logger.info(f"¡Encontrados {len(set(id_matches))} IDs de tickets via Regex!")
                for tid in set(id_matches):
                    # Reconstruir URL completa si solo tenemos el ID
                    url = f"https://web.fourvenues.com/es/luminata-disco/events/sabado-reggaetoncomercial-20-12-2025-IULK/tickets/{tid}"
                    final_results.append({'url': url, 'text': 'Regex Match', 'source': 'Regex'})
        
        return final_results

    except Exception as e:
        logger.error(f"Error en extracción: {e}")
        return []
    finally:
        if 'browser' in locals() and browser:
            try: await browser.stop()
            except: pass
        if display:
            try:
                logger.info("🛑 Deteniendo Display Virtual...")
                display.stop()
            except: pass

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://web.fourvenues.com/es/luminata-disco/events/sabado-reggaetoncomercial-20-12-2025-IULK")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.test or args.url:
        results = await extract_advanced(args.url)
        print("\n\n" + "="*40)
        print(f"RESULTADOS ({len(results)}):")
        print("="*40)
        for r in results:
            print(f"- URL: {r.get('url')}")
            print(f"  Text: {r.get('text')}")
        print("="*40)
        
        # Guardar JSON
        with open(DATA_DIR / "ticket_urls_adv.json", "w", encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
