#!/usr/bin/env python3
"""Test simple de nodriver en Raspberry Pi."""

import asyncio
import nodriver as uc

async def test():
    print('Iniciando test de nodriver...')
    try:
        # Probar diferentes configuraciones
        configs = [
            {'headless': True, 'sandbox': False},
            {'headless': False, 'sandbox': False},
        ]
        
        for i, cfg in enumerate(configs):
            print(f'\n--- Config {i+1}: {cfg} ---')
            try:
                browser = await uc.start(
                    headless=cfg['headless'],
                    sandbox=cfg['sandbox'],
                    browser_args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-setuid-sandbox',
                    ],
                )
                print('  Browser iniciado OK!')
                page = await browser.get('about:blank')
                print('  Pagina cargada OK!')
                title = await page.evaluate("document.title")
                print(f'  Titulo: {title}')
                browser.stop()
                print('  SUCCESS!')
                break
            except Exception as e:
                print(f'  ERROR: {type(e).__name__}: {str(e)[:200]}')
                continue
                
    except Exception as e:
        print(f'ERROR GENERAL: {type(e).__name__}: {e}')

if __name__ == "__main__":
    asyncio.run(test())
