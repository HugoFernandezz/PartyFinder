#!/usr/bin/env python3
"""
Script para generar datos de prueba con eventos agotados
"""

import json
from datetime import datetime, timedelta

def create_test_data_with_sold_out():
    """Crear datos de prueba que incluyen eventos agotados"""
    
    # Datos base
    venues = [
        {
            "id": "1",
            "name": "LUMINATA DISCO",
            "description": "Discoteca en Murcia",
            "address": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
            "imageUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
            "website": "https://www.fourvenues.com/es/luminata-disco",
            "phone": "+34 968 000 000",
            "isActive": True,
            "category": {
                "id": "1",
                "name": "Discoteca",
                "icon": "musical-notes"
            }
        },
        {
            "id": "2",
            "name": "EL CLUB by ODISEO",
            "description": "Eventos de EL CLUB by ODISEO en Murcia",
            "address": "Centro de Ocio ODISEO, Murcia, España",
            "imageUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
            "website": "https://www.fourvenues.com/es/el-club-by-odiseo",
            "phone": "+34 968 000 000",
            "isActive": True,
            "category": {
                "id": "2",
                "name": "Discoteca",
                "icon": "musical-notes"
            }
        }
    ]
    
    # Eventos de prueba
    parties = []
    
    # Evento 1: Disponible (con entradas disponibles)
    parties.append({
        "id": "1",
        "venueId": "1",
        "venueName": "LUMINATA DISCO",
        "title": "Viernes REGGAETÓN - DISPONIBLE",
        "description": "Evento con entradas disponibles. Una noche única con la mejor música y ambiente de Murcia.",
        "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "startTime": "23:30",
        "endTime": "07:00",
        "price": 8,
        "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/20bb50f5-abb1-42a9-70f8-643b8cccce00/w=550",
        "ticketUrl": "https://www.fourvenues.com/es/luminata-disco/events/test-disponible",
        "isAvailable": True,
        "capacity": 300,
        "soldTickets": 150,
        "tags": ["Fiestas"],
        "venueAddress": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
        "ticketTypes": [
            {
                "id": "ticket_0",
                "name": "ENTRADA PROMOCIÓN",
                "description": "Entrada con precio promocional.",
                "price": 8,
                "isAvailable": True,
                "isSoldOut": False,
                "isPromotion": True,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_1",
                "name": "ENTRADA GENERAL",
                "description": "Entrada general al evento.",
                "price": 12,
                "isAvailable": True,
                "isSoldOut": False,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            }
        ]
    })
    
    # Evento 2: AGOTADO (todas las entradas agotadas)
    parties.append({
        "id": "2",
        "venueId": "1",
        "venueName": "LUMINATA DISCO",
        "title": "Sábado COMERCIAL - AGOTADO",
        "description": "Evento completamente agotado. Todas las entradas han sido vendidas.",
        "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "startTime": "23:30",
        "endTime": "07:00",
        "price": 10,
        "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/20bb50f5-abb1-42a9-70f8-643b8cccce00/w=550",
        "ticketUrl": "https://www.fourvenues.com/es/luminata-disco/events/test-agotado",
        "isAvailable": False,
        "capacity": 300,
        "soldTickets": 300,
        "tags": ["Fiestas"],
        "venueAddress": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
        "ticketTypes": [
            {
                "id": "ticket_0",
                "name": "ENTRADA PROMOCIÓN",
                "description": "Entrada con precio promocional.",
                "price": 10,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": True,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_1",
                "name": "ENTRADA GENERAL",
                "description": "Entrada general al evento.",
                "price": 15,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_2",
                "name": "ENTRADA VIP",
                "description": "Entrada VIP con acceso preferente.",
                "price": 20,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": True,
                "restrictions": ""
            }
        ]
    })
    
    # Evento 3: Parcialmente agotado (algunas entradas disponibles)
    parties.append({
        "id": "3",
        "venueId": "2",
        "venueName": "EL CLUB by ODISEO",
        "title": "YOU by ODISEO - POCAS ENTRADAS",
        "description": "Evento con pocas entradas disponibles. ¡Últimas oportunidades!",
        "date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
        "startTime": "23:00",
        "endTime": "06:00",
        "price": 8,
        "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/201bd664-98b6-457a-1c1b-805a15ecaf00/w=550",
        "ticketUrl": "https://www.fourvenues.com/es/el-club-by-odiseo/events/test-pocas",
        "isAvailable": True,
        "capacity": 300,
        "soldTickets": 280,
        "tags": ["Fiestas"],
        "venueAddress": "Centro de Ocio ODISEO, Murcia, España",
        "ticketTypes": [
            {
                "id": "ticket_0",
                "name": "ENTRADA SUPER REDUCIDA",
                "description": "Entrada con precio especial reducido.",
                "price": 8,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_1",
                "name": "ENTRADA REDUCIDA",
                "description": "Entrada con precio reducido.",
                "price": 10,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_2",
                "name": "ENTRADA GENERAL",
                "description": "Entrada general al evento.",
                "price": 15,
                "isAvailable": True,
                "isSoldOut": False,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            }
        ]
    })
    
    # Evento 4: Otro evento agotado
    parties.append({
        "id": "4",
        "venueId": "2",
        "venueName": "EL CLUB by ODISEO",
        "title": "PASSION FRUIT - SOLD OUT",
        "description": "Evento especial completamente agotado. ¡Gracias por el apoyo!",
        "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "startTime": "23:00",
        "endTime": "06:00",
        "price": 12,
        "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/31454263-cafa-4bbf-5afc-0ea72d9ea300/w=550",
        "ticketUrl": "https://www.fourvenues.com/es/el-club-by-odiseo/events/test-sold-out",
        "isAvailable": False,
        "capacity": 300,
        "soldTickets": 300,
        "tags": ["Fiestas"],
        "venueAddress": "Centro de Ocio ODISEO, Murcia, España",
        "ticketTypes": [
            {
                "id": "ticket_0",
                "name": "ANTICIPADA REDUCIDA",
                "description": "Entrada con precio reducido.",
                "price": 12,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_1",
                "name": "ANTICIPADA GENERAL",
                "description": "Entrada general al evento.",
                "price": 15,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": False,
                "restrictions": ""
            },
            {
                "id": "ticket_2",
                "name": "ANTICIPADA VIP",
                "description": "Entrada VIP con acceso preferente.",
                "price": 25,
                "isAvailable": False,
                "isSoldOut": True,
                "isPromotion": False,
                "isVip": True,
                "restrictions": ""
            }
        ]
    })
    
    return {
        "venues": venues,
        "parties": parties
    }

def main():
    """Generar archivo de datos de prueba"""
    print("Generando datos de prueba con eventos agotados...")
    
    test_data = create_test_data_with_sold_out()
    
    # Guardar datos de prueba
    with open('test_sold_out_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos de prueba generados:")
    print(f"   - Venues: {len(test_data['venues'])}")
    print(f"   - Parties: {len(test_data['parties'])}")
    
    # Mostrar resumen de eventos
    print(f"\n📋 Resumen de eventos:")
    for party in test_data['parties']:
        status = "🔴 AGOTADO" if not party['isAvailable'] else "🟢 DISPONIBLE"
        available_tickets = len([t for t in party['ticketTypes'] if t['isAvailable']])
        total_tickets = len(party['ticketTypes'])
        print(f"   {status} - {party['title']} ({available_tickets}/{total_tickets} tipos disponibles)")
    
    print(f"\n📁 Archivo guardado: test_sold_out_data.json")
    print(f"\n💡 Para probar:")
    print(f"   1. Copia el contenido a cached_data.json")
    print(f"   2. Reinicia la app")
    print(f"   3. Verifica que los eventos agotados aparezcan en gris con texto rojo")

if __name__ == "__main__":
    main() 