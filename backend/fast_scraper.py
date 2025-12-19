#!/usr/bin/env python3
"""
Fast Scraper para Cloudflare Bypass - Fase 2: Motor de Red
============================================================
Scraping de alto rendimiento usando curl_cffi con TLS impersonation.

Optimizado para Raspberry Pi 4 ARM64 (4GB RAM):
- Sin navegador pesado, solo peticiones HTTP
- TLS fingerprint matching (JA3/JA4) con Chrome
- Renovación automática de sesión si expira

Uso:
    python3 fast_scraper.py --test                    # Test de conexión
    python3 fast_scraper.py --scrape                  # Scraping de eventos
    python3 fast_scraper.py --full-scrape --upload    # Scraping completo + Firebase
"""

import asyncio
import json
import os
import sys
import time
import platform
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Intentar importar curl_cffi
try:
    from curl_cffi import requests as curl_requests
    from curl_cffi.requests import Session as CurlSession
    CURL_AVAILABLE = True
except ImportError:
    CURL_AVAILABLE = False
    print("⚠️ curl_cffi no disponible, usando httpx como fallback")
    try:
        import httpx
    except ImportError:
        print("❌ Ni curl_cffi ni httpx están instalados")
        print("   Instalar con: pip install curl_cffi  o  pip install httpx")
        sys.exit(1)

# Configuración
SESSION_FILE = Path(__file__).parent / "session.json"
DATA_DIR = Path(__file__).parent / "data"

# URLs de las discotecas a scrapear
VENUE_URLS = [
    "https://site.fourvenues.com/es/luminata-disco/events",
    "https://site.fourvenues.com/es/el-club-by-odiseo/events",
    "https://site.fourvenues.com/es/dodo-club/events"
]

# Versiones de Chrome para impersonation
CHROME_IMPERSONATE = "chrome120"  # Debe coincidir con la versión del navegador


class SessionExpiredError(Exception):
    """Excepción cuando la sesión de Cloudflare ha expirado."""
    pass


class CloudflareBlockedError(Exception):
    """Excepción cuando Cloudflare bloquea la petición."""
    pass


def load_session(filepath: Path = SESSION_FILE) -> Optional[Dict[str, Any]]:
    """
    Carga los datos de sesión desde archivo JSON.
    
    Returns:
        dict: Datos de sesión o None si no existe/expiró
    """
    if not filepath.exists():
        print(f"❌ No existe archivo de sesión: {filepath}")
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar expiración
        if data.get('expires_at', 0) < time.time():
            remaining = (time.time() - data.get('expires_at', 0)) / 3600
            print(f"⚠️ Sesión expirada hace {remaining:.1f} horas")
            return None
        
        # Verificar cookies requeridas
        if 'cf_clearance' not in data.get('cookies', {}):
            print("⚠️ Sesión sin cf_clearance")
            return None
        
        remaining = (data.get('expires_at', 0) - time.time()) / 3600
        print(f"✅ Sesión válida cargada (expira en {remaining:.1f}h)")
        return data
        
    except Exception as e:
        print(f"❌ Error cargando sesión: {e}")
        return None


async def renew_session(url: str = None) -> Optional[Dict[str, Any]]:
    """
    Renueva la sesión ejecutando el session_getter.
    
    Returns:
        dict: Nueva sesión o None si falla
    """
    print("\n🔄 Renovando sesión...")
    
    # Importar session_getter
    try:
        from session_getter import get_session, save_session
    except ImportError:
        # Ejecutar como subproceso
        import subprocess
        script_path = Path(__file__).parent / "session_getter.py"
        
        cmd = [sys.executable, str(script_path), "--force"]
        if url:
            cmd.extend(["--url", url])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error renovando sesión:\n{result.stderr}")
            return None
        
        return load_session()
    
    # Usar directamente
    session = await get_session(url or "https://site.fourvenues.com/es/luminata-disco/events")
    if session:
        save_session(session)
    return session


def create_session(session_data: Dict[str, Any]) -> Any:
    """
    Crea una sesión HTTP con las cookies y headers correctos.
    
    Args:
        session_data: Datos de sesión de session.json
    
    Returns:
        Sesión HTTP configurada
    """
    cookies = session_data.get('cookies', {})
    user_agent = session_data.get('user_agent', '')
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    if CURL_AVAILABLE:
        # curl_cffi con TLS impersonation
        session = CurlSession(impersonate=CHROME_IMPERSONATE)
        session.headers.update(headers)
        for name, value in cookies.items():
            session.cookies.set(name, value)
        return session
    else:
        # Fallback a httpx
        return httpx.Client(headers=headers, cookies=cookies, follow_redirects=True)


def check_cloudflare_block(response) -> None:
    """
    Verifica si Cloudflare está bloqueando la petición.
    
    Raises:
        SessionExpiredError: Si la cookie ha expirado
        CloudflareBlockedError: Si Cloudflare bloquea por otra razón
    """
    status = response.status_code
    
    # Códigos de error de Cloudflare
    if status == 403:
        text = response.text[:500] if hasattr(response, 'text') else ''
        if 'cf-' in text.lower() or 'cloudflare' in text.lower():
            raise SessionExpiredError("Cookie cf_clearance expirada")
        raise CloudflareBlockedError(f"Acceso denegado (403)")
    
    if status == 503:
        raise CloudflareBlockedError("Cloudflare en modo de espera (503)")
    
    # Error 1020 de Cloudflare
    if 'error code: 1020' in (response.text[:1000] if hasattr(response, 'text') else ''):
        raise SessionExpiredError("Error 1020: Acceso denegado por Cloudflare")


def extract_events_from_html(html: str) -> List[Dict]:
    """
    Extrae los eventos del JSON embebido en el HTML de Angular.
    """
    import re
    
    json_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>([^<]+)</script>'
    json_matches = re.findall(json_pattern, html, re.DOTALL)
    
    for json_str in json_matches:
        try:
            data = json.loads(json_str)
            
            # Buscar claves que contengan 'events'
            for key in data.keys():
                if 'events' in key.lower() and isinstance(data[key], dict):
                    if 'data' in data[key] and isinstance(data[key]['data'], list):
                        return data[key]['data']
                        
        except json.JSONDecodeError:
            continue
    
    return []


def extract_event_data_from_html(html: str) -> tuple:
    """
    Extrae los tickets y la información del evento del JSON embebido.
    
    Returns:
        tuple: (tickets_list, event_info_dict)
    """
    import re
    
    json_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>([^<]+)</script>'
    json_matches = re.findall(json_pattern, html, re.DOTALL)
    
    tickets = []
    event_info = None
    
    for json_str in json_matches:
        try:
            data = json.loads(json_str)
            
            if isinstance(data, dict):
                for key in data.keys():
                    value = data[key]
                    
                    if not isinstance(value, dict):
                        continue
                    
                    # Buscar la clave de tickets
                    if 'tickets' in key.lower() and 'data' in value:
                        if isinstance(value['data'], list):
                            tickets = value['data']
                    
                    # Buscar datos del evento
                    if 'event' in key.lower() and 'tickets' not in key.lower() and 'lists' not in key.lower():
                        event_info = value.get('data', value)
                        
        except json.JSONDecodeError:
            continue
    
    return tickets, event_info


async def fetch_url(session, url: str, retry_count: int = 2) -> Optional[str]:
    """
    Hace una petición GET a una URL con reintentos.
    
    Args:
        session: Sesión HTTP
        url: URL a obtener
        retry_count: Número de reintentos
    
    Returns:
        str: Contenido HTML o None si falla
    """
    for attempt in range(retry_count + 1):
        try:
            if CURL_AVAILABLE:
                response = session.get(url, timeout=30)
            else:
                response = session.get(url, timeout=30)
            
            check_cloudflare_block(response)
            
            if response.status_code == 200:
                return response.text
            
            print(f"   ⚠️ HTTP {response.status_code} para {url}")
            
        except (SessionExpiredError, CloudflareBlockedError):
            raise  # Re-lanzar para manejar arriba
        except Exception as e:
            if attempt < retry_count:
                print(f"   ⚠️ Reintentando ({attempt + 1}/{retry_count}): {e}")
                await asyncio.sleep(2)
            else:
                print(f"   ❌ Error: {e}")
    
    return None


async def scrape_events(
    session_data: Dict[str, Any],
    urls: List[str] = None,
    scrape_tickets: bool = True
) -> List[Dict]:
    """
    Scrapea eventos de las URLs configuradas.
    
    Args:
        session_data: Datos de sesión
        urls: Lista de URLs (default: VENUE_URLS)
        scrape_tickets: Si obtener detalles de tickets
    
    Returns:
        list: Lista de eventos
    """
    target_urls = urls or VENUE_URLS
    all_events = []
    
    session = create_session(session_data)
    
    print(f"\n📡 Scrapeando {len(target_urls)} venues...")
    
    try:
        for url in target_urls:
            print(f"\n   🔗 {url}")
            
            html = await fetch_url(session, url)
            if not html:
                continue
            
            events = extract_events_from_html(html)
            print(f"      ✅ {len(events)} eventos encontrados")
            
            all_events.extend(events)
            
            # Pausa entre venues
            if url != target_urls[-1]:
                await asyncio.sleep(1)
        
        # Scraping de detalles de tickets
        if scrape_tickets and all_events:
            print(f"\n🎫 Obteniendo detalles de {len(all_events)} eventos...")
            
            for i, event in enumerate(all_events):
                org = event.get('organization', {})
                org_slug = org.get('slug', '')
                event_slug = event.get('slug', '')
                event_code = event.get('code', '')
                
                if org_slug and event_slug:
                    event_url = f"https://site.fourvenues.com/es/{org_slug}/events/{event_slug}-{event_code}"
                    
                    try:
                        html = await fetch_url(session, event_url)
                        if html:
                            tickets, event_info = extract_event_data_from_html(html)
                            
                            # Añadir url_compra a cada ticket
                            for ticket in tickets:
                                ticket_id = ticket.get('id', '')
                                if ticket_id:
                                    ticket['url_compra'] = f"https://web.fourvenues.com/es/{org_slug}/events/{event_slug}-{event_code}/tickets/{ticket_id}"
                            
                            event['_scraped_tickets'] = tickets
                            event['_scraped_event_info'] = event_info
                            
                            if tickets:
                                print(f"      [{i+1}/{len(all_events)}] ✅ {len(tickets)} tickets")
                            
                    except (SessionExpiredError, CloudflareBlockedError):
                        raise
                    except Exception as e:
                        print(f"      [{i+1}/{len(all_events)}] ⚠️ Error: {e}")
                    
                    # Pausa entre eventos
                    await asyncio.sleep(0.5)
    
    finally:
        # Cerrar sesión
        if hasattr(session, 'close'):
            session.close()
    
    print(f"\n🎉 Total: {len(all_events)} eventos scrapeados")
    return all_events


def transform_to_app_format(events: List[Dict]) -> List[Dict]:
    """
    Transforma los eventos al formato de la app PartyFinder.
    """
    transformed = []
    
    for event in events:
        org = event.get('organization', {})
        location = event.get('location', {})
        scraped_info = event.get('_scraped_event_info', {}) or {}
        
        # Fechas
        start_timestamp = scraped_info.get('start') or event.get('dates', {}).get('start')
        end_timestamp = scraped_info.get('end') or event.get('dates', {}).get('end')
        date_timestamp = scraped_info.get('date') or event.get('dates', {}).get('date') or start_timestamp
        
        fecha = datetime.now().strftime('%Y-%m-%d')
        hora_inicio = "23:00"
        hora_fin = "06:00"
        
        if date_timestamp:
            try:
                fecha = datetime.fromtimestamp(date_timestamp).strftime('%Y-%m-%d')
            except:
                pass
        
        if start_timestamp:
            try:
                hora_inicio = datetime.fromtimestamp(start_timestamp).strftime('%H:%M')
            except:
                pass
        
        if end_timestamp:
            try:
                hora_fin = datetime.fromtimestamp(end_timestamp).strftime('%H:%M')
            except:
                pass
        
        # Imagen
        scraped_images = scraped_info.get('images', {})
        image_url = (
            scraped_info.get('image') or 
            event.get('image') or 
            scraped_images.get('medium') or 
            event.get('images', {}).get('main') or 
            org.get('images', {}).get('main', '')
        )
        
        # Tickets
        scraped_tickets = event.get('_scraped_tickets', [])
        entradas = []
        
        if scraped_tickets:
            for ticket in scraped_tickets:
                price_raw = ticket.get('price', 0)
                if isinstance(price_raw, str):
                    price_raw = price_raw.replace('€', '').replace(',', '.').strip()
                try:
                    price = float(price_raw)
                except:
                    price = 0
                
                entrada = {
                    "id": ticket.get('id', ''),
                    "tipo": ticket.get('name', 'Entrada General'),
                    "precio": str(price),
                    "agotadas": ticket.get('isSoldOut', False),
                    "url_compra": ticket.get('url_compra', ''),
                }
                entradas.append(entrada)
        
        if not entradas:
            entradas = [{
                "tipo": "Entrada General",
                "precio": "0",
                "agotadas": False,
                "url_compra": ""
            }]
        
        # Tags
        tags = []
        for g in event.get('musicGenres', []):
            if isinstance(g, dict) and g.get('name'):
                tags.append(g.get('name'))
        if not tags:
            tags = ['Fiesta']
        
        # URL
        org_slug = org.get('slug', '')
        event_slug = event.get('slug', '')
        event_code = event.get('code', '')
        url_evento = f"https://site.fourvenues.com/es/{org_slug}/events/{event_slug}-{event_code}" if org_slug and event_slug else ""
        
        transformed_event = {
            "evento": {
                "nombreEvento": event.get('name', 'Evento'),
                "descripcion": scraped_info.get('description') or event.get('description', ''),
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "imagen_url": image_url,
                "url_evento": url_evento,
                "entradas": entradas,
                "tags": tags,
                "edad_minima": scraped_info.get('age') or event.get('age', 18),
                "lugar": {
                    "nombre": org.get('name', 'Venue'),
                    "direccion": location.get('addressComplete') or location.get('address', ''),
                    "ciudad": location.get('city', ''),
                    "categoria": "Discoteca"
                }
            }
        }
        
        transformed.append(transformed_event)
    
    return transformed


async def scrape_and_save(
    upload_to_firebase: bool = False,
    auto_renew: bool = True
) -> List[Dict]:
    """
    Ejecuta el scraping completo y guarda resultados.
    
    Args:
        upload_to_firebase: Subir a Firebase
        auto_renew: Renovar sesión automáticamente si expira
    
    Returns:
        list: Eventos transformados
    """
    print("=" * 60)
    print("PartyFinder - Fast Scraper (Fase 2)")
    print("=" * 60)
    
    # Cargar sesión
    session_data = load_session()
    
    if not session_data:
        if auto_renew:
            session_data = await renew_session()
            if not session_data:
                print("❌ No se pudo obtener sesión")
                return []
        else:
            print("❌ No hay sesión válida. Ejecutar session_getter.py primero")
            return []
    
    # Scraping con manejo de sesión expirada
    try:
        raw_events = await scrape_events(session_data)
        
    except SessionExpiredError:
        if auto_renew:
            print("\n⚠️ Sesión expirada, renovando...")
            session_data = await renew_session()
            if session_data:
                raw_events = await scrape_events(session_data)
            else:
                print("❌ No se pudo renovar sesión")
                return []
        else:
            print("❌ Sesión expirada. Usar --auto-renew o ejecutar session_getter.py")
            return []
    
    if not raw_events:
        print("❌ No se encontraron eventos")
        return []
    
    # Transformar
    transformed_events = transform_to_app_format(raw_events)
    
    # Crear directorio data si no existe
    DATA_DIR.mkdir(exist_ok=True)
    
    # Guardar datos crudos
    with open(DATA_DIR / 'raw_events.json', 'w', encoding='utf-8') as f:
        json.dump(raw_events, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Datos crudos: {DATA_DIR / 'raw_events.json'}")
    
    # Guardar datos transformados
    with open(DATA_DIR / 'events.json', 'w', encoding='utf-8') as f:
        json.dump(transformed_events, f, indent=2, ensure_ascii=False)
    print(f"💾 Datos transformados: {DATA_DIR / 'events.json'}")
    
    # Subir a Firebase
    if upload_to_firebase:
        print("\n📤 Subiendo a Firebase...")
        try:
            from firebase_config import upload_events_to_firestore, delete_old_events
            
            delete_old_events()
            upload_events_to_firestore(transformed_events)
            print("✅ Datos subidos a Firebase")
        except Exception as e:
            print(f"❌ Error subiendo a Firebase: {e}")
    
    return transformed_events


async def test_connection() -> bool:
    """
    Test de conexión con sesión actual.
    
    Returns:
        bool: True si la conexión funciona
    """
    print("=" * 60)
    print("PartyFinder - Test de Conexión")
    print("=" * 60)
    
    session_data = load_session()
    if not session_data:
        print("❌ No hay sesión. Ejecutar: python3 session_getter.py")
        return False
    
    session = create_session(session_data)
    test_url = "https://site.fourvenues.com/es/luminata-disco/events"
    
    print(f"\n🔗 Probando: {test_url}")
    
    try:
        if CURL_AVAILABLE:
            response = session.get(test_url, timeout=30)
        else:
            response = session.get(test_url, timeout=30)
        
        check_cloudflare_block(response)
        
        if response.status_code == 200:
            content_length = len(response.text)
            events = extract_events_from_html(response.text)
            print(f"✅ Conexión exitosa!")
            print(f"   HTTP: {response.status_code}")
            print(f"   Contenido: {content_length} bytes")
            print(f"   Eventos detectados: {len(events)}")
            return True
        else:
            print(f"⚠️ HTTP {response.status_code}")
            return False
            
    except SessionExpiredError as e:
        print(f"❌ Sesión expirada: {e}")
        return False
    except CloudflareBlockedError as e:
        print(f"❌ Bloqueado por Cloudflare: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if hasattr(session, 'close'):
            session.close()


async def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description='Fast Scraper con bypass de Cloudflare'
    )
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Solo test de conexión'
    )
    parser.add_argument(
        '--scrape', '-s',
        action='store_true',
        help='Ejecutar scraping'
    )
    parser.add_argument(
        '--full-scrape', '-f',
        action='store_true',
        help='Scraping completo con tickets'
    )
    parser.add_argument(
        '--upload', '-u',
        action='store_true',
        help='Subir resultados a Firebase'
    )
    parser.add_argument(
        '--no-auto-renew',
        action='store_true',
        help='No renovar sesión automáticamente'
    )
    
    args = parser.parse_args()
    
    # Si no se especifica ninguna acción, mostrar ayuda
    if not any([args.test, args.scrape, args.full_scrape]):
        parser.print_help()
        return 0
    
    if args.test:
        success = await test_connection()
        return 0 if success else 1
    
    if args.scrape or args.full_scrape:
        events = await scrape_and_save(
            upload_to_firebase=args.upload,
            auto_renew=not args.no_auto_renew
        )
        return 0 if events else 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
