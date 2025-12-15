#!/usr/bin/env python3
"""
Scraper usando ScrapingBee API para bypass de Cloudflare.
Optimizado para usar menos créditos.
"""

import json
import os
import sys
import re
import requests
from typing import List, Dict
from urllib.parse import urlencode

# Forzar UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VENUE_URLS = [
    ("luminata-disco", "https://site.fourvenues.com/es/luminata-disco/events"),
    ("el-club-by-odiseo", "https://site.fourvenues.com/es/el-club-by-odiseo/events"),
    ("dodo-club", "https://site.fourvenues.com/es/dodo-club/events")
]

def get_api_key() -> str:
    """Obtiene la API key de ScrapingBee."""
    api_key = os.environ.get('SCRAPINGBEE_API_KEY')
    if not api_key:
        print("❌ Error: SCRAPINGBEE_API_KEY no configurada")
        sys.exit(1)
    return api_key

def fetch_with_scrapingbee(url: str, api_key: str) -> str:
    """Obtiene el HTML usando ScrapingBee (MÍNIMO créditos: ~5/request)."""
    params = {
        'api_key': api_key,
        'url': url,
        'render_js': 'true',  # ~5 créditos - necesario para Angular
        # SIN premium_proxy ni stealth_proxy para ahorrar
        'block_resources': 'false',
        'wait': '8000',
    }
    
    response = requests.get(
        'https://app.scrapingbee.com/api/v1/',
        params=params,
        timeout=90
    )
    
    if response.status_code == 200:
        return response.text
    elif response.status_code == 500:
        # Si falla, reintentar CON premium_proxy
        print(f"   ⚠️ Reintentando con premium_proxy...")
        params['premium_proxy'] = 'true'
        response = requests.get(
            'https://app.scrapingbee.com/api/v1/',
            params=params,
            timeout=90
        )
        if response.status_code == 200:
            return response.text
    
    print(f"   ❌ Error: {response.status_code} - {response.text[:150]}")
    return ""

def extract_events_from_html(html: str, venue_id: str, venue_name: str) -> List[Dict]:
    """Extrae eventos del JSON embebido, con venue info."""
    events = []
    
    # Buscar scripts con type="application/json"
    json_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>([^<]+)</script>'
    matches = re.findall(json_pattern, html, re.DOTALL)
    
    for match in matches:
        try:
            data = json.loads(match)
            if not isinstance(data, dict):
                continue
                
            for key, value in data.items():
                if 'events' not in key.lower():
                    continue
                if not isinstance(value, dict) or 'data' not in value:
                    continue
                if not isinstance(value['data'], list):
                    continue
                    
                for e in value['data']:
                    # Extraer fecha - puede estar en varios campos
                    date = e.get('date') or e.get('startDate') or e.get('start_date') or ''
                    if isinstance(e.get('dates'), list) and e['dates']:
                        date = e['dates'][0].get('date', date)
                    
                    # Extraer imagen - puede estar en varios lugares
                    image_url = ''
                    if isinstance(e.get('flyer'), dict):
                        image_url = e['flyer'].get('image') or e['flyer'].get('url') or ''
                    elif isinstance(e.get('image'), str):
                        image_url = e['image']
                    elif isinstance(e.get('images'), list) and e['images']:
                        image_url = e['images'][0] if isinstance(e['images'][0], str) else e['images'][0].get('url', '')
                    
                    # Extraer venue del JSON o usar el del URL
                    place = e.get('place', {})
                    v_id = place.get('id', venue_id) if isinstance(place, dict) else venue_id
                    v_name = place.get('name', venue_name) if isinstance(place, dict) else venue_name
                    
                    event = {
                        'id': e.get('id', ''),
                        'name': e.get('name', ''),
                        'description': e.get('description') or '',
                        'date': date,
                        'imageUrl': image_url,
                        'venueId': v_id,
                        'venueName': v_name,
                    }
                    events.append(event)
        except:
            continue
    
    return events

def deduplicate_events(events: List[Dict]) -> List[Dict]:
    """Elimina eventos duplicados por ID."""
    seen = set()
    unique = []
    for event in events:
        if event['id'] and event['id'] not in seen:
            seen.add(event['id'])
            unique.append(event)
    return unique

def scrape_all_venues() -> List[Dict]:
    """Scrapea todos los venues."""
    api_key = get_api_key()
    all_events = []
    
    for venue_id, url in VENUE_URLS:
        venue_name = venue_id.replace('-', ' ').title()
        print(f"\n📡 Scrapeando: {venue_name}")
        
        html = fetch_with_scrapingbee(url, api_key)
        
        if html:
            print(f"   📥 HTML: {len(html)} bytes")
            events = extract_events_from_html(html, venue_id, venue_name)
            print(f"   📦 Eventos: {len(events)}")
            all_events.extend(events)
        else:
            print(f"   ⚠️ Sin HTML")
    
    # Deduplicar
    unique_events = deduplicate_events(all_events)
    print(f"\n🔄 Total único: {len(unique_events)} (de {len(all_events)} totales)")
    
    return unique_events

def upload_to_firebase(events: List[Dict]):
    """Sube eventos a Firebase."""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        if not firebase_admin._apps:
            cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                print("❌ serviceAccountKey.json no encontrado")
                return False
        
        db = firestore.client()
        events_ref = db.collection('events')
        
        # Limpiar existentes
        for doc in events_ref.stream():
            doc.reference.delete()
        
        # Subir nuevos
        for event in events:
            events_ref.add(event)
        
        print(f"✅ Subidos {len(events)} eventos a Firebase")
        return True
        
    except Exception as e:
        print(f"❌ Error Firebase: {e}")
        return False

def main():
    print("=" * 60)
    print("PartyFinder - Scraper API (ScrapingBee)")
    print("=" * 60)
    
    events = scrape_all_venues()
    
    if events:
        os.makedirs('data', exist_ok=True)
        with open('data/events.json', 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        print(f"💾 Guardados en data/events.json")
        
        if '--firebase' in sys.argv:
            upload_to_firebase(events)
    else:
        print("\n⚠️ No se encontraron eventos")
    
    return len(events) > 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
