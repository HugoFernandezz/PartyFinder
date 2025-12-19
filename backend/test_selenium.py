#!/usr/bin/env python3
"""
Test de Selenium + undetected-chromedriver en Raspberry Pi.
"""

import sys
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("data", exist_ok=True)

def test_selenium():
    print("=" * 60)
    print("TEST: Selenium + undetected-chromedriver vs FourVenues")
    print("=" * 60)
    
    # 1. Importar
    print("\n[1/5] Importando undetected-chromedriver...")
    try:
        import undetected_chromedriver as uc
        print("      OK - undetected_chromedriver importado")
    except ImportError as e:
        print(f"      FAIL - {e}")
        return False
    
    # 2. Configurar opciones
    print("\n[2/5] Configurando opciones...")
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless=new')
    options.binary_location = '/usr/bin/chromium-browser'
    print("      OK - Opciones configuradas")
    
    # 3. Iniciar navegador
    print("\n[3/5] Iniciando navegador...")
    try:
        driver = uc.Chrome(options=options, version_main=136)
        print("      OK - Navegador iniciado")
    except Exception as e:
        print(f"      FAIL - {e}")
        import traceback
        print(traceback.format_exc())
        return False
    
    # 4. Navegar
    print("\n[4/5] Navegando a FourVenues...")
    url = "https://site.fourvenues.com/es/luminata-disco/events"
    print(f"      URL: {url}")
    
    try:
        driver.get(url)
        print("      OK - Navegacion iniciada")
    except Exception as e:
        print(f"      FAIL - {e}")
        driver.quit()
        return False
    
    # 5. Esperar Cloudflare
    print("\n[5/5] Esperando bypass de Cloudflare...")
    challenge_keywords = ["momento", "checking", "just", "wait", "cloudflare"]
    
    success = False
    for i in range(90):
        time.sleep(1)
        try:
            title = driver.title
        except:
            title = ""
        
        title_lower = title.lower() if title else ""
        is_challenge = any(kw in title_lower for kw in challenge_keywords)
        
        if title and not is_challenge:
            try:
                html_len = len(driver.page_source)
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
        print("      FAIL - Timeout")
        try:
            with open("data/debug_selenium.html", "w") as f:
                f.write(driver.page_source)
        except:
            pass
        driver.quit()
        return False
    
    # Esperar Angular
    print("\n[EXTRA] Esperando Angular (15s)...")
    time.sleep(15)
    
    html = driver.page_source
    driver.quit()
    
    # Buscar eventos
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
    
    print(f"\n{'='*60}")
    if events_found > 0:
        print(f"SUCCESS! Encontrados {events_found} eventos")
    else:
        print("WARN: No se encontraron eventos")
        with open("data/debug_selenium_no_events.html", "w") as f:
            f.write(html)
    print("="*60)
    
    return events_found > 0

if __name__ == "__main__":
    result = test_selenium()
    sys.exit(0 if result else 1)
