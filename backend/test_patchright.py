#!/usr/bin/env python3
"""
Test de Patchright contra FourVenues/Cloudflare en Raspberry Pi.
Patchright es un fork de Playwright con patches anti-detección.
"""

import asyncio
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

async def test_patchright():
    print("=" * 60)
    print("TEST: Patchright vs FourVenues/Cloudflare")
    print("=" * 60)
    
    # 1. Importar Patchright
    print("\n[1/5] Importando Patchright...")
    try:
        from patchright.async_api import async_playwright
        print("      OK - Patchright importado")
    except ImportError as e:
        print(f"      FAIL - {e}")
        print("      Ejecutar: pip install patchright && patchright install chromium")
        return False
    
    # 2. Iniciar navegador
    print("\n[2/5] Iniciando navegador Chromium (patchright headless=False)...")
    try:
        async with async_playwright() as p:
            # IMPORTANTE: headless=False para bypass de Cloudflare
            # Requiere Xvfb en sistemas sin display
            browser = await p.chromium.launch(
                headless=False,  # Cloudflare detecta headless=True
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )
            print("      OK - Navegador iniciado")
            
            # 3. Crear página
            print("\n[3/5] Creando contexto...")
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='es-ES',
            )
            page = await context.new_page()
            print("      OK - Contexto creado")
            
            # 4. Navegar a FourVenues
            print("\n[4/5] Navegando a FourVenues...")
            url = "https://site.fourvenues.com/es/luminata-disco/events"
            print(f"      URL: {url}")
            
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print("      OK - Navegacion iniciada")
            
            # 5. Esperar bypass de Cloudflare
            print("\n[5/5] Esperando bypass de Cloudflare...")
            challenge_keywords = ["momento", "checking", "just", "wait", "cloudflare", "verifying"]
            
            success = False
            for i in range(90):
                await asyncio.sleep(1)
                try:
                    title = await page.title()
                except:
                    title = ""
                
                title_lower = title.lower() if title else ""
                is_challenge = any(kw in title_lower for kw in challenge_keywords)
                
                if title and not is_challenge:
                    try:
                        body_len = await page.evaluate("document.body.innerHTML.length")
                        if body_len > 1000:
                            print(f"      OK - Challenge resuelto en {i}s!")
                            print(f"      Titulo: {title[:50]}")
                            print(f"      HTML: {body_len} bytes")
                            success = True
                            break
                    except:
                        pass
                
                if i % 10 == 0 and i > 0:
                    print(f"      Esperando... ({i}s) - Titulo: {title[:30] if title else 'N/A'}")
            
            if not success:
                print("      FAIL - Timeout esperando Cloudflare")
                html = await page.content()
                os.makedirs("data", exist_ok=True)
                with open("data/debug_patchright.html", "w") as f:
                    f.write(html)
                print("      Guardado HTML en data/debug_patchright.html")
                await browser.close()
                return False
            
            # Esperar Angular
            print("\n[EXTRA] Esperando Angular (15s)...")
            await asyncio.sleep(15)
            
            # Buscar eventos
            html = await page.content()
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
            
            print(f"\n{'='*60}")
            if events_found > 0:
                print(f"SUCCESS! Encontrados {events_found} eventos")
                print("Patchright funciona correcamente!")
            else:
                print("WARN: No se encontraron eventos")
                os.makedirs("data", exist_ok=True)
                with open("data/debug_patchright_no_events.html", "w") as f:
                    f.write(html)
            print("="*60)
            
            await browser.close()
            return events_found > 0
            
    except Exception as e:
        import traceback
        print(f"      FAIL - {type(e).__name__}: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    result = asyncio.run(test_patchright())
    sys.exit(0 if result else 1)
