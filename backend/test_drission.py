#!/usr/bin/env python3
"""
Test de DrissionPage contra FourVenues/Cloudflare en Raspberry Pi.
DrissionPage es una librería anti-detección que no requiere webdriver.
"""

import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("data", exist_ok=True)

def test_drission():
    print("=" * 60)
    print("TEST: DrissionPage vs FourVenues/Cloudflare")
    print("=" * 60)
    
    # 1. Importar DrissionPage
    print("\n[1/5] Importando DrissionPage...")
    try:
        from DrissionPage import ChromiumPage, ChromiumOptions
        print("      OK - DrissionPage importado")
    except ImportError as e:
        print(f"      FAIL - {e}")
        print("      Ejecutar: pip install DrissionPage")
        return False
    
    # 2. Configurar opciones
    print("\n[2/5] Configurando opciones del navegador...")
    try:
        options = ChromiumOptions()
        # Argumentos críticos para Linux ARM
        options.set_argument('--no-sandbox')
        options.set_argument('--disable-dev-shm-usage')
        options.set_argument('--disable-gpu')
        options.set_argument('--disable-setuid-sandbox')
        options.set_argument('--disable-software-rasterizer')
        options.set_argument('--headless=new')  # Nuevo modo headless de Chrome
        options.set_argument('--remote-debugging-port=9222')
        
        # Usar Chromium del sistema
        browser_path = '/usr/bin/chromium-browser'
        if os.path.exists(browser_path):
            options.set_browser_path(browser_path)
            print(f"      Usando: {browser_path}")
        else:
            print("      WARN: chromium-browser no encontrado, usando por defecto")
        
        # Configurar user-data-dir temporal
        import tempfile
        user_data = tempfile.mkdtemp(prefix='drission_')
        options.set_argument(f'--user-data-dir={user_data}')
        print(f"      User data: {user_data}")
        
        print("      OK - Opciones configuradas")
    except Exception as e:
        print(f"      FAIL - {e}")
        return False
    
    # 3. Iniciar navegador
    print("\n[3/5] Iniciando navegador...")
    try:
        page = ChromiumPage(options)
        print("      OK - Navegador iniciado")
    except Exception as e:
        print(f"      FAIL - {e}")
        import traceback
        print(traceback.format_exc())
        return False
    
    # 4. Navegar a FourVenues
    print("\n[4/5] Navegando a FourVenues...")
    url = "https://site.fourvenues.com/es/luminata-disco/events"
    print(f"      URL: {url}")
    
    try:
        page.get(url, timeout=60)
        print("      OK - Navegacion iniciada")
    except Exception as e:
        print(f"      FAIL - {e}")
        page.quit()
        return False
    
    # 5. Esperar bypass de Cloudflare
    print("\n[5/5] Esperando bypass de Cloudflare...")
    challenge_keywords = ["momento", "checking", "just", "wait", "cloudflare", "verifying"]
    
    import time
    success = False
    for i in range(90):
        time.sleep(1)
        try:
            title = page.title
        except:
            title = ""
        
        title_lower = title.lower() if title else ""
        is_challenge = any(kw in title_lower for kw in challenge_keywords)
        
        if title and not is_challenge:
            try:
                html_len = len(page.html)
                if html_len > 1000:
                    print(f"      OK - Challenge resuelto en {i}s!")
                    print(f"      Titulo: {title[:50]}")
                    print(f"      HTML: {html_len} bytes")
                    success = True
                    break
            except:
                pass
        
        if i % 10 == 0 and i > 0:
            print(f"      Esperando... ({i}s) - Titulo: {title[:30] if title else 'N/A'}")
    
    if not success:
        print("      FAIL - Timeout esperando Cloudflare")
        try:
            with open("data/debug_drission.html", "w") as f:
                f.write(page.html)
            print("      Guardado HTML en data/debug_drission.html")
        except:
            pass
        page.quit()
        return False
    
    # Esperar Angular
    print("\n[EXTRA] Esperando Angular (15s)...")
    time.sleep(15)
    
    # Buscar eventos
    html = page.html
    print(f"      HTML total: {len(html)} bytes")
    
    import re
    import json
    
    json_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>([^<]+)</script>'
    matches = re.findall(json_pattern, html, re.DOTALL)
    
    events_found = 0
    for match in matches:
        try:
            data = json.loads(match)
            if isinstance(data, dict):
                for key in data.keys():
                    if 'events' in key.lower() and isinstance(data[key], dict):
                        if 'data' in data[key] and isinstance(data[key]['data'], list):
                            events_found = len(data[key]['data'])
                            break
        except:
            pass
    
    page.quit()
    
    print(f"\n{'='*60}")
    if events_found > 0:
        print(f"SUCCESS! Encontrados {events_found} eventos")
        print("DrissionPage funciona correctamente!")
    else:
        print("WARN: No se encontraron eventos")
        with open("data/debug_drission_no_events.html", "w") as f:
            f.write(html)
    print("="*60)
    
    return events_found > 0

if __name__ == "__main__":
    result = test_drission()
    sys.exit(0 if result else 1)
