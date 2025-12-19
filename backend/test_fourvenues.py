#!/usr/bin/env python3
"""
Test completo de scraping con Playwright + Stealth en Raspberry Pi.
Prueba específica contra FourVenues para verificar bypass de Cloudflare.
"""

import asyncio
import sys
import os

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

async def test_fourvenues():
    print("=" * 60)
    print("TEST: Playwright + Stealth vs FourVenues/Cloudflare")
    print("=" * 60)
    
    # 1. Importar Playwright
    print("\n[1/6] Importando Playwright...")
    try:
        from playwright.async_api import async_playwright
        print("      OK - Playwright importado")
    except ImportError as e:
        print(f"      FAIL - {e}")
        print("      Ejecutar: pip install playwright && playwright install chromium")
        return False
    
    # 2. Importar Stealth
    print("\n[2/6] Importando playwright-stealth...")
    stealth_func = None
    try:
        from playwright_stealth import stealth
        stealth_func = stealth
        print("      OK - stealth importado")
    except ImportError as e:
        print(f"      WARN - {e}")
        print("      Continuando sin stealth (puede ser detectado por Cloudflare)")
    
    # 3. Iniciar navegador
    print("\n[3/6] Iniciando navegador Chromium...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-setuid-sandbox',
                ]
            )
            print("      OK - Navegador iniciado")
            
            # 4. Crear contexto y página
            print("\n[4/6] Configurando contexto...")
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='es-ES',
            )
            page = await context.new_page()
            
            # Aplicar stealth si disponible
            if stealth_func:
                stealth_func(page)
                print("      OK - Stealth aplicado")
            else:
                print("      WARN - Sin stealth")
            
            # 5. Navegar a FourVenues
            print("\n[5/6] Navegando a FourVenues...")
            url = "https://site.fourvenues.com/es/luminata-disco/events"
            print(f"      URL: {url}")
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                print("      OK - Navegacion iniciada")
            except Exception as e:
                print(f"      FAIL - Error navegando: {e}")
                await browser.close()
                return False
            
            # 6. Esperar y verificar Cloudflare
            print("\n[6/6] Esperando bypass de Cloudflare...")
            challenge_keywords = ["momento", "checking", "just", "wait", "cloudflare", "verifying"]
            
            success = False
            for i in range(60):
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
                            print(f"      OK - Challenge resuelto en {i}s")
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
                # Guardar HTML para debug
                html = await page.content()
                with open("data/debug_cloudflare.html", "w") as f:
                    f.write(html)
                print("      Guardado HTML en data/debug_cloudflare.html")
                await browser.close()
                return False
            
            # Esperar carga de Angular
            print("\n[EXTRA] Esperando Angular (15s)...")
            await asyncio.sleep(15)
            
            # Obtener HTML y buscar eventos
            html = await page.content()
            print(f"      HTML total: {len(html)} bytes")
            
            # Buscar eventos en JSON
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
                print("El scraper deberia funcionar correctamente.")
            else:
                print("WARN: No se encontraron eventos en el JSON")
                print("Puede ser que la pagina no tenga eventos o el formato cambio")
                with open("data/debug_no_events.html", "w") as f:
                    f.write(html)
                print("Guardado HTML en data/debug_no_events.html")
            print("="*60)
            
            await browser.close()
            return events_found > 0
            
    except Exception as e:
        import traceback
        print(f"      FAIL - Error general: {type(e).__name__}: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Crear directorio data si no existe
    os.makedirs("data", exist_ok=True)
    
    result = asyncio.run(test_fourvenues())
    sys.exit(0 if result else 1)
