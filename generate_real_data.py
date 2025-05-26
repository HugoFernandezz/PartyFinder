#!/usr/bin/env python3
"""
Script para generar datos reales de FourVenues en formato JSON limpio
"""

import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def fetch_html(url):
    """Obtener HTML de una URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error obteniendo HTML de {url}: {e}")
        return None

def extract_fourvenues_tickets(soup):
    """Extraer tickets usando los datos JSON estructurados de Schema.org en los scripts"""
    ticket_types = []
    
    # Buscar en todos los scripts por datos JSON de Schema.org
    scripts = soup.find_all('script')
    for script in scripts:
        if not script.string:
            continue
        
        # Buscar patrones JSON de ofertas (Schema.org)
        offer_pattern = r'\{"@type":"Offer","priceCurrency":"EUR","price":(\d+),"name":"([^"]+)"[^}]*"availability":"([^"]+)"[^}]*\}'
        offers = re.findall(offer_pattern, script.string)
        
        if offers:
            for price, name, availability in offers:
                is_available = availability == "https://schema.org/InStock"
                
                ticket_types.append({
                    "id": f"ticket_{len(ticket_types)}",
                    "name": name.strip(),
                    "description": f"Entrada al evento.",
                    "price": int(price),
                    "isAvailable": is_available,
                    "isSoldOut": not is_available,
                    "isPromotion": "PROMOCIÓN" in name.upper(),
                    "isVip": "VIP" in name.upper(),
                    "restrictions": ""
                })
    
    return ticket_types

def extract_minimum_price(ticket_types):
    """Extraer el precio mínimo de los tipos de entrada disponibles"""
    if not ticket_types:
        return 0
    
    available_tickets = [
        ticket for ticket in ticket_types 
        if ticket.get('isAvailable', True) and not ticket.get('isSoldOut', False) and ticket.get('price', 0) > 0
    ]
    
    if available_tickets:
        return min(ticket['price'] for ticket in available_tickets)
    
    return min(ticket['price'] for ticket in ticket_types if ticket.get('price', 0) > 0) if ticket_types else 0

def scrape_venue_events(venue_name, venue_url, venue_id):
    """Scraper específico para un venue de FourVenues"""
    html = fetch_html(venue_url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    events = []
    
    # Buscar enlaces de eventos
    event_links = soup.find_all('a', href=re.compile(r'/events/'))
    event_urls = set()
    
    for link in event_links:
        href = link.get('href')
        if href and '/events/' in href:
            if href.startswith('/'):
                href = 'https://www.fourvenues.com' + href
            event_urls.add(href)
    
    # Procesar cada evento
    for event_url in list(event_urls)[:5]:  # Limitar a 5 eventos por venue
        try:
            event_html = fetch_html(event_url)
            if not event_html:
                continue
                
            event_soup = BeautifulSoup(event_html, 'html.parser')
            
            # Extraer título
            title_elem = event_soup.find('h1')
            title = title_elem.get_text().strip() if title_elem else "Evento sin título"
            
            # Extraer fecha y hora
            date_match = re.search(r'(\d{2}-\d{2}-\d{4})', event_url)
            if date_match:
                date_str = date_match.group(1)
                date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                event_date = date_obj.strftime('%Y-%m-%d')
            else:
                event_date = "2025-06-01"
            
            # Extraer imagen
            img_elem = event_soup.find('img')
            image_url = img_elem.get('src') if img_elem else "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center"
            if image_url and image_url.startswith('/'):
                image_url = 'https://www.fourvenues.com' + image_url
            
            # Extraer tipos de entrada
            ticket_types = extract_fourvenues_tickets(event_soup)
            price = extract_minimum_price(ticket_types)
            
            event = {
                "id": str(len(events) + 1),
                "venueId": venue_id,
                "venueName": venue_name,
                "title": title,
                "description": f"Evento exclusivo en {venue_name}. Una noche única con la mejor música y ambiente de Murcia.",
                "date": event_date,
                "startTime": "23:30",
                "endTime": "07:00",
                "price": price,
                "imageUrl": image_url,
                "ticketUrl": event_url,
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Murcia, España",
                "ticketTypes": ticket_types
            }
            
            events.append(event)
            
        except Exception as e:
            print(f"Error procesando evento {event_url}: {e}")
            continue
    
    return events

def generate_real_data():
    """Generar datos reales de FourVenues"""
    
    venues_config = [
        {
            "id": "1",
            "name": "MACCAO OPEN AIR CLUB",
            "url": "https://www.fourvenues.com/es/hugo-fernandez-gil",
            "description": "Eventos de MACCAO OPEN AIR CLUB en Murcia",
            "address": "Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España",
            "category": {"id": "1", "name": "Club", "icon": "musical-notes"}
        },
        {
            "id": "2", 
            "name": "LUMINATA DISCO",
            "url": "https://www.fourvenues.com/es/luminata-disco",
            "description": "Eventos de LUMINATA DISCO en Murcia",
            "address": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
            "category": {"id": "2", "name": "Discoteca", "icon": "musical-notes"}
        },
        {
            "id": "3",
            "name": "EL CLUB by ODISEO", 
            "url": "https://www.fourvenues.com/es/el-club-by-odiseo",
            "description": "Eventos de EL CLUB by ODISEO en Murcia",
            "address": "Centro de Ocio ODISEO, Murcia, España",
            "category": {"id": "3", "name": "Discoteca", "icon": "musical-notes"}
        }
    ]
    
    venues = []
    all_parties = []
    
    for venue_config in venues_config:
        print(f"Procesando venue: {venue_config['name']}")
        
        # Crear venue
        venue = {
            "id": venue_config["id"],
            "name": venue_config["name"],
            "description": venue_config["description"],
            "address": venue_config["address"],
            "imageUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
            "website": venue_config["url"],
            "phone": "+34 968 000 000",
            "isActive": True,
            "category": venue_config["category"]
        }
        venues.append(venue)
        
        # Obtener eventos del venue
        events = scrape_venue_events(venue_config["name"], venue_config["url"], venue_config["id"])
        all_parties.extend(events)
        print(f"Encontrados {len(events)} eventos en {venue_config['name']}")
    
    data = {
        "venues": venues,
        "parties": all_parties
    }
    
    # Guardar datos
    with open('data/events_real.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Datos reales generados exitosamente:")
    print(f"   - Venues: {len(venues)}")
    print(f"   - Parties: {len(all_parties)}")
    print(f"   - Archivo guardado: data/events_real.json")
    
    return data

if __name__ == "__main__":
    generate_real_data() 