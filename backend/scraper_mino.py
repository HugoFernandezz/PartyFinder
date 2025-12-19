#!/usr/bin/env python3
"""
Scraper usando Mino.ai API para bypass de Cloudflare.
Usa IA y lenguaje natural para extraer datos visualmente de sitios web.

Mino.ai es una herramienta de automatización basada en IA que extrae
datos de páginas web visualmente, ideal para sitios con protección
anti-scraping como Cloudflare.
"""

import json
import os
import sys
import requests
from typing import List, Dict, Optional

# Forzar UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# URLs de las discotecas a scrapear
VENUE_URLS = [
    ("luminata-disco", "https://site.fourvenues.com/es/luminata-disco/events"),
    ("el-club-by-odiseo", "https://site.fourvenues.com/es/el-club-by-odiseo/events"),
    ("dodo-club", "https://site.fourvenues.com/es/dodo-club/events")
]

MINO_API_URL = "https://mino.ai/v1/automation/run-sse"

# Debug mode
DEBUG = os.environ.get('DEBUG', '').lower() in ('1', 'true', 'yes')


def get_api_key() -> str:
    """Obtiene la API key de Mino.ai."""
    api_key = os.environ.get('MINO_API_KEY')
    if not api_key:
        print("❌ Error: MINO_API_KEY no configurada")
        print("   Configura: $env:MINO_API_KEY = 'tu-api-key'")
        sys.exit(1)
    return api_key


def fetch_with_mino(url: str, goal: str, api_key: str, use_stealth: bool = True) -> Optional[Dict]:
    """
    Ejecuta una automatización con Mino.ai y obtiene el resultado.
    
    Args:
        url: URL a visitar
        goal: Descripción en lenguaje natural de qué extraer
        api_key: API key de Mino
        use_stealth: Usar modo stealth para bypass de Cloudflare
        
    Returns:
        dict: Resultado JSON de Mino o None si falló
    """
    payload = {
        "url": url,
        "goal": goal,
        "browser_profile": "stealth" if use_stealth else "lite"
    }
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        print(f"   🤖 Consultando Mino.ai...")
        
        response = requests.post(
            MINO_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=180  # 3 minutos para sitios lentos
        )
        
        if response.status_code != 200:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"      {response.text[:300]}")
            return None
        
        # Procesar eventos SSE
        result_json = None
        
        for line in response.iter_lines():
            if not line:
                continue
                
            line_str = line.decode('utf-8')
            
            if line_str.startswith('data: '):
                try:
                    event_data = json.loads(line_str[6:])
                    event_type = event_data.get('type', '')
                    
                    if event_type == 'PROGRESS':
                        purpose = event_data.get('purpose', '')
                        if purpose and DEBUG:
                            print(f"   📍 {purpose}")
                    
                    elif event_type == 'COMPLETE':
                        status = event_data.get('status', '')
                        if status == 'COMPLETED':
                            result_json = event_data.get('resultJson')
                            print(f"   ✅ Completado")
                        else:
                            print(f"   ⚠️ Status: {status}")
                            error = event_data.get('error', '')
                            if error:
                                print(f"      Error: {error}")
                    
                    elif event_type == 'STREAMING_URL' and DEBUG:
                        stream_url = event_data.get('streamingUrl', '')
                        if stream_url:
                            print(f"   🔗 Stream: {stream_url}")
                            
                except json.JSONDecodeError:
                    continue
        
        if DEBUG and result_json:
            print(f"   📦 Respuesta: {json.dumps(result_json, indent=2)[:500]}...")
        
        return result_json
        
    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout después de 180s")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def scrape_venue_events(venue_id: str, url: str, api_key: str) -> List[Dict]:
    """
    Scrapea los eventos de un venue usando Mino.ai.
    Usa extracción visual inteligente basada en IA.
    
    Returns:
        list: Lista de eventos encontrados
    """
    venue_name = venue_id.replace('-', ' ').title()
    
    # Prompt optimizado para extracción visual
    goal = f"""
    This is an events page for a nightclub. Wait for the page to fully load 
    (bypass any Cloudflare or security checks if needed).
    
    Find all events listed on this page and extract them as a JSON array.
    For each event card/item you see, extract:
    - name: the event title/name 
    - date: the date shown (in YYYY-MM-DD format if possible)
    - imageUrl: the URL of the event image/flyer
    - description: any description text (optional)
    
    Return a JSON object like: {{"events": [...]}}
    
    If you cannot find events or the page doesn't load, return: {{"events": [], "error": "description of what happened"}}
    
    The venue name is: {venue_name}
    """
    
    result = fetch_with_mino(url, goal, api_key, use_stealth=True)
    
    if not result:
        return []
    
    # Procesar resultado
    events = []
    error = result.get('error', '')
    
    if error:
        print(f"   ⚠️ Mino reportó: {error}")
    
    # Extraer eventos del resultado (Mino puede devolver en varios formatos)
    raw_events = []
    if isinstance(result, dict):
        raw_events = result.get('events', []) or result.get('data', []) or []
    elif isinstance(result, list):
        raw_events = result
    
    if not isinstance(raw_events, list):
        raw_events = []
    
    for e in raw_events:
        if not isinstance(e, dict):
            continue
        
        event_name = e.get('name', '') or e.get('title', '') or e.get('eventName', '')
        if not event_name:
            continue
            
        event = {
            'id': str(e.get('id', '')) or f"{venue_id}_{len(events)}",
            'name': event_name,
            'description': e.get('description', '') or '',
            'date': e.get('date', '') or e.get('eventDate', '') or '',
            'imageUrl': e.get('imageUrl', '') or e.get('image', '') or e.get('flyer', ''),
            'venueId': venue_id,
            'venueName': venue_name,
        }
        events.append(event)
    
    return events


def deduplicate_events(events: List[Dict]) -> List[Dict]:
    """Elimina eventos duplicados por nombre+fecha."""
    seen = set()
    unique = []
    for event in events:
        # Key = nombre + fecha + venue
        key = f"{event.get('name', '')}_{event.get('date', '')}_{event.get('venueId', '')}"
        if key not in seen:
            seen.add(key)
            unique.append(event)
    return unique


def scrape_all_venues() -> List[Dict]:
    """Scrapea todos los venues usando Mino.ai."""
    api_key = get_api_key()
    all_events = []
    
    print("\n" + "=" * 60)
    print("PartyFinder - Scraper Mino.ai")
    print("=" * 60)
    
    for venue_id, url in VENUE_URLS:
        venue_name = venue_id.replace('-', ' ').title()
        print(f"\n📡 Scrapeando: {venue_name}")
        print(f"   🌐 {url}")
        
        events = scrape_venue_events(venue_id, url, api_key)
        print(f"   📦 Eventos encontrados: {len(events)}")
        
        for e in events:
            print(f"      • {e.get('name', 'Sin nombre')}")
        
        all_events.extend(events)
    
    # Deduplicar
    unique_events = deduplicate_events(all_events)
    print(f"\n🔄 Total único: {len(unique_events)} (de {len(all_events)} totales)")
    
    return unique_events


def upload_to_firebase(events: List[Dict]) -> bool:
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
        print("🗑️ Limpiando eventos anteriores...")
        for doc in events_ref.stream():
            doc.reference.delete()
        
        # Subir nuevos
        print("📤 Subiendo eventos...")
        for event in events:
            events_ref.add(event)
        
        print(f"✅ Subidos {len(events)} eventos a Firebase")
        return True
        
    except ImportError:
        print("❌ firebase-admin no instalado")
        print("   pip install firebase-admin")
        return False
    except Exception as e:
        print(f"❌ Error Firebase: {e}")
        return False


def main():
    """Punto de entrada principal."""
    events = scrape_all_venues()
    
    if events:
        # Guardar localmente
        os.makedirs('data', exist_ok=True)
        output_path = os.path.join('data', 'events.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Guardados en {output_path}")
        
        # Subir a Firebase si se especifica
        if '--firebase' in sys.argv:
            print("\n" + "-" * 40)
            upload_to_firebase(events)
    else:
        print("\n⚠️ No se encontraron eventos")
    
    print("\n" + "=" * 60)
    return len(events) > 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
