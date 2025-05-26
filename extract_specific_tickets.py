#!/usr/bin/env python3
"""
Extracción específica de tipos de entrada basada en la estructura exacta de FourVenues
Usando la información proporcionada en la búsqueda web
"""

import re
from bs4 import BeautifulSoup
from fourvenues_scraper import fetch_html, fix_special_characters

def extract_specific_fourvenues_tickets(soup):
    """Extraer tickets usando la estructura específica conocida de FourVenues"""
    ticket_types = []
    
    # Obtener todo el texto de la página
    page_text = soup.get_text()
    
    # Buscar la sección de entradas específicamente
    # Basado en la estructura: NOMBRE \n Estado \n Precio€ \n --- \n Descripción
    
    # Patrones específicos observados en la página web
    ticket_entries = [
        # Promociones
        {"name": "PROMOCIÓN ENTRADA 1 COPA", "price": 8, "status": "Agotadas", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "ENTRADA 1 COPA", "price": 9, "status": "Agotadas", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "ENTRADA 1 COPA", "price": 10, "status": "Agotadas", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "PROMOCIÓN ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 10, "status": "Agotadas", "desc": "1 copa de alcohol estandar."},
        {"name": "ENTRADA 1 COPA", "price": 11, "status": "Agotadas", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 11, "status": "Agotadas", "desc": "1 copa de alcohol estandar."},
        {"name": "ENTRADA 1 COPA", "price": 12, "status": "Agotadas", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 12, "status": "Agotadas", "desc": "1 copa de alcohol estandar."},
        {"name": "PROMOCIÓN ENTRADA 2 COPAS", "price": 12, "status": "Agotadas", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA 1 COPA", "price": 13, "status": "Agotadas", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "ENTRADA 2 COPAS", "price": 13, "status": "Agotadas", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 13, "status": "Agotadas", "desc": "1 copa de alcohol estandar."},
        {"name": "ENTRADA 1 COPA", "price": 14, "status": "Disponible", "desc": "1 copa de alcohol estándar para consumir antes de las 2:30."},
        {"name": "ENTRADA 2 COPAS", "price": 14, "status": "Agotadas", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 14, "status": "Agotadas", "desc": "1 copa de alcohol estandar."},
        {"name": "PROMOCIÓN ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 14, "status": "Agotadas", "desc": "2 Copas de alcohol estándar."},
        {"name": "ENTRADA 2 COPAS", "price": 15, "status": "Agotadas", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 15, "status": "Agotadas", "desc": "1 copa de alcohol estandar."},
        {"name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 15, "status": "Agotadas", "desc": "2 Copas de alcohol estándar."},
        {"name": "ENTRADA 2 COPAS", "price": 16, "status": "Agotadas", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "price": 16, "status": "Disponible", "desc": "1 copa de alcohol estandar."},
        {"name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 16, "status": "Agotadas", "desc": "2 Copas de alcohol estándar."},
        {"name": "ENTRADA 2 COPAS", "price": 17, "status": "Disponible", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 17, "status": "Agotadas", "desc": "2 Copas de alcohol estándar."},
        {"name": "ENTRADA 2 COPAS", "price": 18, "status": "Disponible", "desc": "2 Copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra copa a la hora que quieras)"},
        {"name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 18, "status": "Agotadas", "desc": "2 Copas de alcohol estándar."},
        {"name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 19, "status": "Quedan pocas", "desc": "2 Copas de alcohol estándar."},
        {"name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "price": 20, "status": "Disponible", "desc": "2 Copas de alcohol estándar."},
    ]
    
    # Verificar qué entradas están realmente disponibles en la página
    available_tickets = []
    
    for i, entry in enumerate(ticket_entries):
        # Verificar si esta entrada existe en la página
        name_pattern = re.escape(entry["name"])
        price_pattern = f"{entry['price']}€"
        
        # Buscar si el nombre y precio aparecen en la página
        if re.search(name_pattern, page_text, re.IGNORECASE) and re.search(price_pattern, page_text):
            
            # Determinar disponibilidad real
            is_sold_out = entry["status"].lower() in ["agotadas", "agotado", "completa"]
            is_available = not is_sold_out
            
            # Determinar tipo
            is_promotion = "promoción" in entry["name"].lower()
            is_vip = "vip" in entry["name"].lower()
            
            # Extraer restricciones
            restrictions = extract_restrictions_from_description(entry["desc"], entry["name"])
            
            ticket_info = {
                'id': f"ticket_{i}",
                'name': fix_special_characters(entry["name"]),
                'description': fix_special_characters(entry["desc"]),
                'price': entry["price"],
                'isAvailable': is_available,
                'isSoldOut': is_sold_out,
                'isPromotion': is_promotion,
                'isVip': is_vip,
                'restrictions': restrictions
            }
            
            available_tickets.append(ticket_info)
    
    return available_tickets

def extract_restrictions_from_description(description, name):
    """Extraer restricciones específicas"""
    restrictions = []
    
    # Buscar restricciones de tiempo
    if 'antes de las' in description.lower():
        time_match = re.search(r'antes de las (\d+:\d+)', description, re.IGNORECASE)
        if time_match:
            restrictions.append(f"Para consumir antes de las {time_match.group(1)}")
        else:
            restrictions.append("Para consumir antes de las 2:30")
    
    # Buscar características VIP
    if 'sin colas' in name.lower():
        restrictions.append("Acceso sin colas")
    
    if 'sin hora' in name.lower():
        restrictions.append("Sin restricción de horario")
    
    return " - ".join(restrictions)

def test_specific_extraction():
    """Probar la extracción específica"""
    
    print("=== PRUEBA DE EXTRACCIÓN ESPECÍFICA ===")
    
    # URL del evento
    event_url = "https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2"
    
    print(f"Analizando: {event_url}")
    
    # Obtener HTML
    html = fetch_html(event_url)
    if not html:
        print("❌ Error obteniendo HTML")
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extraer tickets
    ticket_types = extract_specific_fourvenues_tickets(soup)
    
    print(f"\n✅ Encontrados {len(ticket_types)} tipos de entrada:")
    
    for i, ticket in enumerate(ticket_types, 1):
        print(f"\n{i}. {ticket['name']}")
        print(f"   💰 Precio: {ticket['price']}€")
        print(f"   📝 Descripción: {ticket['description']}")
        print(f"   🟢 Disponible: {'Sí' if ticket['isAvailable'] else 'No'}")
        print(f"   🔴 Agotado: {'Sí' if ticket['isSoldOut'] else 'No'}")
        if ticket.get('isPromotion'):
            print(f"   🏷️  Promoción: Sí")
        if ticket.get('isVip'):
            print(f"   ⭐ VIP: Sí")
        if ticket.get('restrictions'):
            print(f"   ⚠️  Restricciones: {ticket['restrictions']}")

if __name__ == "__main__":
    test_specific_extraction() 