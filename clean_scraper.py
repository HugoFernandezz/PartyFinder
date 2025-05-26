#!/usr/bin/env python3
"""
Scraper limpio de FourVenues que genera solo JSON
"""

import json
import sys
import io
from contextlib import redirect_stdout

# Importar las funciones del scraper original
from fourvenues_scraper import (
    fetch_html, extract_event_details, extract_fourvenues_tickets,
    extract_minimum_price, fix_special_characters
)
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_venue_clean(venue_name, venue_url, venue_id):
    """Scraper limpio para un venue específico"""
    html = fetch_html(venue_url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Buscar enlaces de eventos
    event_links = soup.find_all('a', href=re.compile(r'/events/'))
    event_urls = set()
    
    for link in event_links:
        href = link.get('href')
        if href and '/events/' in href:
            if href.startswith('/'):
                href = 'https://www.fourvenues.com' + href
            event_urls.add(href)
    
    events = []
    for event_url in event_urls:
        try:
            # Usar la función original pero capturar solo el resultado
            event_html = fetch_html(event_url)
            if not event_html:
                continue
                
            event_soup = BeautifulSoup(event_html, 'html.parser')
            
            # Extraer detalles del evento usando las funciones originales
            title_elem = event_soup.find('h1')
            title = title_elem.get_text().strip() if title_elem else "Evento sin título"
            title = fix_special_characters(title)
            
            # Extraer fecha de la URL
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
            
            # Extraer tipos de entrada usando la función original
            ticket_types = extract_fourvenues_tickets(event_soup)
            price = extract_minimum_price(ticket_types)
            
            # Crear evento
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
                "venueAddress": get_venue_address(venue_name),
                "ticketTypes": ticket_types
            }
            
            events.append(event)
            
        except Exception:
            continue
    
    return events

def get_venue_address(venue_name):
    """Obtener dirección del venue"""
    addresses = {
        "MACCAO OPEN AIR CLUB": "Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España",
        "LUMINATA DISCO": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
        "EL CLUB by ODISEO": "Centro de Ocio ODISEO, Murcia, España"
    }
    return addresses.get(venue_name, "Murcia, España")

def generate_clean_data():
    """Generar datos limpios de FourVenues"""
    
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
        events = scrape_venue_clean(venue_config["name"], venue_config["url"], venue_config["id"])
        all_parties.extend(events)
    
    data = {
        "venues": venues,
        "parties": all_parties
    }
    
    return data

if __name__ == "__main__":
    # Generar datos y imprimir solo JSON
    data = generate_clean_data()
    print(json.dumps(data, indent=2, ensure_ascii=False)) 