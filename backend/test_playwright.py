#!/usr/bin/env python3
"""Test de Playwright + Stealth en Raspberry Pi."""

import asyncio

async def test():
    print("=" * 50)
    print("Test de Playwright + Stealth")
    print("=" * 50)
    
    # Test Playwright
    try:
        from playwright.async_api import async_playwright
        print("[OK] Playwright importado")
    except Exception as e:
        print(f"[ERROR] Playwright: {e}")
        return
    
    # Test Stealth
    try:
        from playwright_stealth import stealth_async
        print("[OK] playwright-stealth importado")
        have_stealth = True
    except Exception as e:
        print(f"[WARN] playwright-stealth: {e}")
        have_stealth = False
    
    # Test lanzar navegador
    print("\nIniciando navegador...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )
            print("[OK] Navegador iniciado")
            
            context = await browser.new_context()
            page = await context.new_page()
            
            if have_stealth:
                await stealth_async(page)
                print("[OK] Stealth aplicado")
            
            # Probar navegacion simple
            await page.goto("https://httpbin.org/headers", timeout=30000)
            content = await page.content()
            print(f"[OK] Pagina cargada ({len(content)} bytes)")
            
            # Ver User-Agent
            await page.goto("https://httpbin.org/user-agent", timeout=30000)
            body = await page.inner_text("body")
            print(f"[INFO] User-Agent: {body[:100]}")
            
            await browser.close()
            print("\n[SUCCESS] Todas las pruebas pasaron!")
            
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test())
