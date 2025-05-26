#!/usr/bin/env python3
"""
Implementación mejorada para extraer tipos de entrada de FourVenues
Basada en la estructura específica observada en la página web
"""

import re
from bs4 import BeautifulSoup
from fourvenues_scraper import fetch_html, fix_special_characters

def extract_fourvenues_tickets_v2(soup):
    """Extraer tickets usando la estructura específica observada en FourVenues"""
    ticket_types = []
    
    # Obtener todo el texto de la página
    page_text = soup.get_text()
    
    # Patrones específicos basados en la información proporcionada
    ticket_patterns = [
        # Patrón: NOMBRE_ENTRADA \n Estado \n Precio€ \n --- \n Descripción
        r'(PROMOCIÓN ENTRADA [^€\n]+)\s*(Agotadas|Quedan pocas|Disponible)?\s*(\d+)€\s*---\s*([^€\n]+)',
        r'(ENTRADA VIP [^€\n]+)\s*(Agotadas|Quedan pocas|Disponible)?\s*(\d+)€\s*---\s*([^€\n]+)',
        r'(ENTRADA [^€\n]+)\s*(Agotadas|Quedan pocas|Disponible)?\s*(\d+)€\s*---\s*([^€\n]+)',
    ]
    
    # Buscar usando los patrones específicos
    for pattern in ticket_patterns:
        matches = re.finditer(pattern, page_text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        
        for match in matches:
            name = match.group(1).strip()
            status = match.group(2) if match.group(2) else "Disponible"
            price = int(match.group(3))
            description = match.group(4).strip()
            
            # Limpiar y procesar la información
            ticket_info = process_ticket_info(name, status, price, description, len(ticket_types))
            
            # Evitar duplicados
            if not is_duplicate_ticket(ticket_info, ticket_types):
                ticket_types.append(ticket_info)
    
    # Si no encontramos tickets con el método anterior, usar método alternativo
    if not ticket_types:
        ticket_types = extract_tickets_alternative_method(page_text)
    
    return ticket_types

def extract_tickets_alternative_method(page_text):
    """Método alternativo basado en la estructura conocida"""
    ticket_types = []
    
    # Buscar sección de entradas específicamente
    entradas_section_match = re.search(r'Entradas\s*(.*?)(?:Mesas|Procesos de pago|$)', page_text, re.IGNORECASE | re.DOTALL)
    
    if entradas_section_match:
        entradas_text = entradas_section_match.group(1)
        
        # Patrones más específicos para la sección de entradas
        ticket_lines = []
        lines = entradas_text.split('\n')
        
        current_ticket = {}
        
        for line in lines:
            line = line.strip()
            
            # Detectar inicio de nuevo ticket
            if re.match(r'(PROMOCIÓN ENTRADA|ENTRADA VIP|ENTRADA)\s+', line, re.IGNORECASE):
                # Guardar ticket anterior si existe
                if current_ticket and 'name' in current_ticket and 'price' in current_ticket:
                    ticket_types.append(current_ticket)
                
                # Iniciar nuevo ticket
                current_ticket = {
                    'id': f"ticket_{len(ticket_types)}",
                    'name': fix_special_characters(line),
                    'description': '',
                    'price': 0,
                    'isAvailable': True,
                    'isSoldOut': False,
                    'isPromotion': 'promoción' in line.lower(),
                    'isVip': 'vip' in line.lower(),
                    'restrictions': ''
                }
            
            # Detectar estado
            elif re.match(r'(Agotadas|Quedan pocas|Disponible)', line, re.IGNORECASE):
                if current_ticket:
                    current_ticket['isSoldOut'] = 'agotad' in line.lower()
                    current_ticket['isAvailable'] = not current_ticket['isSoldOut']
            
            # Detectar precio
            elif re.match(r'\d+€', line):
                if current_ticket:
                    price_match = re.search(r'(\d+)', line)
                    if price_match:
                        current_ticket['price'] = int(price_match.group(1))
            
            # Detectar descripción
            elif re.search(r'copa|alcohol|consumir|antes', line, re.IGNORECASE):
                if current_ticket:
                    current_ticket['description'] = fix_special_characters(line)
                    current_ticket['restrictions'] = extract_restrictions_from_description(line, current_ticket['name'])
        
        # Agregar último ticket
        if current_ticket and 'name' in current_ticket and current_ticket.get('price', 0) > 0:
            ticket_types.append(current_ticket)
    
    return ticket_types

def process_ticket_info(name, status, price, description, index):
    """Procesar información de un ticket individual"""
    
    # Determinar disponibilidad
    is_sold_out = 'agotad' in status.lower() or 'completa' in status.lower()
    is_available = not is_sold_out
    
    # Determinar tipo
    is_promotion = 'promoción' in name.lower()
    is_vip = 'vip' in name.lower()
    
    # Extraer restricciones
    restrictions = extract_restrictions_from_description(description, name)
    
    return {
        'id': f"ticket_{index}",
        'name': fix_special_characters(name),
        'description': fix_special_characters(description),
        'price': price,
        'isAvailable': is_available,
        'isSoldOut': is_sold_out,
        'isPromotion': is_promotion,
        'isVip': is_vip,
        'restrictions': restrictions
    }

def extract_restrictions_from_description(description, name):
    """Extraer restricciones específicas"""
    restrictions = []
    
    # Buscar restricciones de tiempo
    if 'antes de las' in description.lower():
        time_match = re.search(r'antes de las (\d+:\d+)', description, re.IGNORECASE)
        if time_match:
            restrictions.append(f"Para consumir antes de las {time_match.group(1)}")
    
    # Buscar características VIP
    if 'sin colas' in name.lower():
        restrictions.append("Acceso sin colas")
    
    if 'sin hora' in name.lower():
        restrictions.append("Sin restricción de horario")
    
    return " - ".join(restrictions)

def is_duplicate_ticket(new_ticket, existing_tickets):
    """Verificar si un ticket es duplicado"""
    for existing in existing_tickets:
        if (existing['name'] == new_ticket['name'] and 
            existing['price'] == new_ticket['price']):
            return True
    return False

def test_extraction_v2():
    """Probar la nueva implementación"""
    
    print("=== PRUEBA DE EXTRACCIÓN V2 ===")
    
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
    ticket_types = extract_fourvenues_tickets_v2(soup)
    
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
    test_extraction_v2() 