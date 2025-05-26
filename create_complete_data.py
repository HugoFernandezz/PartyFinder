#!/usr/bin/env python3
"""
Script para crear datos completos con todos los eventos
"""

import json

def create_complete_data():
    """Crear datos completos con todos los eventos detectados"""
    
    data = {
        "venues": [
            {
                "id": "1",
                "name": "MACCAO OPEN AIR CLUB",
                "description": "Eventos de MACCAO OPEN AIR CLUB en Murcia",
                "address": "Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España",
                "imageUrl": "https://images.unsplash.com/photo-1571266028243-d220c9c3b31f?w=800&h=600&fit=crop&crop=center",
                "website": "https://www.fourvenues.com/es/hugo-fernandez-gil",
                "phone": "+34 968 000 000",
                "isActive": True,
                "category": {
                    "id": "1",
                    "name": "Club",
                    "icon": "musical-notes"
                }
            },
            {
                "id": "2",
                "name": "LUMINATA DISCO",
                "description": "Eventos de LUMINATA DISCO en Murcia",
                "address": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
                "imageUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
                "website": "https://www.fourvenues.com/es/luminata-disco",
                "phone": "+34 968 000 000",
                "isActive": True,
                "category": {
                    "id": "2",
                    "name": "Discoteca",
                    "icon": "musical-notes"
                }
            },
            {
                "id": "3",
                "name": "EL CLUB by ODISEO",
                "description": "Eventos de EL CLUB by ODISEO en Murcia",
                "address": "Centro de Ocio ODISEO, Murcia, España",
                "imageUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
                "website": "https://www.fourvenues.com/es/el-club-by-odiseo",
                "phone": "+34 968 000 000",
                "isActive": True,
                "category": {
                    "id": "3",
                    "name": "Discoteca",
                    "icon": "musical-notes"
                }
            }
        ],
        "parties": [
            # LUMINATA DISCO - Jueves
            {
                "id": "1",
                "venueId": "2",
                "venueName": "LUMINATA DISCO",
                "title": "Jueves PLAY ON REGGAETON",
                "description": "Evento exclusivo en LUMINATA DISCO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-05-29",
                "startTime": "23:30",
                "endTime": "07:00",
                "price": 7,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/20bb50f5-abb1-42a9-70f8-643b8cccce00/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/luminata-disco/events/jueves-play-on-reggaeton--29-05-2025-3BKH",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "PROMOCIÓN ENTRADA 1 COPA", "description": "1 copa de alcohol estándar para consumir antes de las 2:30.", "price": 7, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": False, "restrictions": "Para consumir antes de las 2:30"},
                    {"id": "ticket_1", "name": "ENTRADA 1 COPA", "description": "1 copa de alcohol estándar para consumir antes de las 2:30.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": "Para consumir antes de las 2:30"},
                    {"id": "ticket_2", "name": "ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "description": "1 copa de alcohol estándar sin restricción de horario.", "price": 10, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": True, "restrictions": "Acceso sin colas - Sin restricción de horario"}
                ]
            },
            # EL CLUB by ODISEO - Jueves
            {
                "id": "2",
                "venueId": "3",
                "venueName": "EL CLUB by ODISEO",
                "title": "YOU by ODISEO ESPECIAL EXAMENES 3",
                "description": "Evento exclusivo en EL CLUB by ODISEO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-05-29",
                "startTime": "23:00",
                "endTime": "06:00",
                "price": 8,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/201bd664-98b6-457a-1c1b-805a15ecaf00/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/el-club-by-odiseo/events/you-by-odiseo-especial-examenes-3-29-05-2025-YX8T",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centro de Ocio ODISEO, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "ENTRADA SUPER REDUCIDA", "description": "Entrada con precio especial reducido.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_1", "name": "ENTRADA REDUCIDA", "description": "Entrada con precio reducido.", "price": 10, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_2", "name": "ENTRADA GENERAL", "description": "Entrada al evento.", "price": 12, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            },
            # LUMINATA DISCO - Viernes
            {
                "id": "3",
                "venueId": "2",
                "venueName": "LUMINATA DISCO",
                "title": "Viernes REGGAETÓNCOMERCIAL",
                "description": "Evento exclusivo en LUMINATA DISCO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-05-30",
                "startTime": "23:30",
                "endTime": "07:00",
                "price": 8,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/20bb50f5-abb1-42a9-70f8-643b8cccce00/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "PROMOCIÓN ENTRADA 1 COPA", "description": "1 copa de alcohol estándar para consumir antes de las 2:30.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": False, "restrictions": "Para consumir antes de las 2:30"},
                    {"id": "ticket_1", "name": "ENTRADA 1 COPA", "description": "1 copa de alcohol estándar para consumir antes de las 2:30.", "price": 9, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": "Para consumir antes de las 2:30"},
                    {"id": "ticket_2", "name": "PROMOCIÓN ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "description": "1 copa de alcohol estándar sin restricción de horario.", "price": 10, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": True, "restrictions": "Acceso sin colas - Sin restricción de horario"},
                    {"id": "ticket_3", "name": "PROMOCIÓN ENTRADA 2 COPAS", "description": "2 copas de alcohol estándar.", "price": 12, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": False, "restrictions": ""},
                    {"id": "ticket_4", "name": "ENTRADA 2 COPAS", "description": "2 copas de alcohol estándar.", "price": 13, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_5", "name": "ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "description": "2 copas de alcohol estándar sin restricción de horario.", "price": 15, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": True, "restrictions": "Acceso sin colas - Sin restricción de horario"}
                ]
            },
            # EL CLUB by ODISEO - Viernes
            {
                "id": "4",
                "venueId": "3",
                "venueName": "EL CLUB by ODISEO",
                "title": "PASSION FRUIT X KYBBA",
                "description": "Evento exclusivo en EL CLUB by ODISEO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-05-30",
                "startTime": "23:00",
                "endTime": "06:00",
                "price": 12,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/31454263-cafa-4bbf-5afc-0ea72d9ea300/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/el-club-by-odiseo/events/passion-fruit-x-kybba-30-05-2025-RCWR",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centro de Ocio ODISEO, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "ANTICIPADA REDUCIDA", "description": "Entrada con precio reducido.", "price": 12, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_1", "name": "ANTICIPADA GENERAL", "description": "Entrada al evento.", "price": 15, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_2", "name": "ANTICIPADA GENERAL", "description": "Entrada al evento.", "price": 18, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            },
            # LUMINATA DISCO - Sábado
            {
                "id": "5",
                "venueId": "2",
                "venueName": "LUMINATA DISCO",
                "title": "Sábado REGGAETÓNCOMERCIAL",
                "description": "Evento exclusivo en LUMINATA DISCO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-05-31",
                "startTime": "23:30",
                "endTime": "07:00",
                "price": 5,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/20bb50f5-abb1-42a9-70f8-643b8cccce00/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/luminata-disco/events/sabado-reggaetoncomercial-31-05-2025-WF35",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "PROMOCIÓN ENTRADA 1 COPA", "description": "1 copa de alcohol estándar para consumir antes de las 2:30.", "price": 5, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": False, "restrictions": "Para consumir antes de las 2:30"},
                    {"id": "ticket_1", "name": "PROMOCIÓN ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA", "description": "1 copa de alcohol estándar sin restricción de horario.", "price": 6, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": True, "restrictions": "Acceso sin colas - Sin restricción de horario"},
                    {"id": "ticket_2", "name": "PROMOCIÓN ENTRADA 2 COPAS", "description": "2 copas de alcohol estándar.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": False, "restrictions": ""},
                    {"id": "ticket_3", "name": "PROMOCIÓN ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA", "description": "2 copas de alcohol estándar sin restricción de horario.", "price": 9, "isAvailable": True, "isSoldOut": False, "isPromotion": True, "isVip": True, "restrictions": "Acceso sin colas - Sin restricción de horario"}
                ]
            },
            # MACCAO - Eventos de Junio
            {
                "id": "6",
                "venueId": "1",
                "venueName": "MACCAO OPEN AIR CLUB",
                "title": "TICKET BUS - MAR MENOR FEST",
                "description": "Festival de música electrónica en MACCAO OPEN AIR CLUB. Una experiencia única con los mejores DJs, ambiente espectacular y la mejor música del momento.",
                "date": "2025-06-05",
                "startTime": "23:30",
                "endTime": "02:00",
                "price": 7,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/1e112878-d207-4eda-c40e-ca65c40bd200/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/hugo-fernandez-gil/events/ticket-bus---mar-menor-fest-05-06-2025-J4FQ",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Buses"],
                "venueAddress": "Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "Ruta 2 Salida 23:30", "description": "Entrada al evento.", "price": 7, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_1", "name": "Ruta 1 Salida 22:00", "description": "Entrada al evento.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_2", "name": "Ruta 3 Salida 22:30", "description": "Entrada al evento.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            },
            {
                "id": "7",
                "venueId": "1",
                "venueName": "MACCAO OPEN AIR CLUB",
                "title": "MAR MENOR FEST",
                "description": "Festival de música electrónica en MACCAO OPEN AIR CLUB. Una experiencia única con los mejores DJs, ambiente espectacular y la mejor música del momento.",
                "date": "2025-06-05",
                "startTime": "06:00",
                "endTime": "02:00",
                "price": 10,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/f06362f4-c593-4d08-c498-48e8e58bd300/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/hugo-fernandez-gil/events/mar-menor-fest-05-06-2025-CZ7W",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "PRIMER TRAMO", "description": "Entrada al evento.", "price": 10, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            },
            {
                "id": "8",
                "venueId": "3",
                "venueName": "EL CLUB by ODISEO",
                "title": "YOU by ODISEO",
                "description": "Evento exclusivo en EL CLUB by ODISEO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-06-05",
                "startTime": "23:00",
                "endTime": "06:00",
                "price": 8,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/db24998f-9e31-4d7a-d1ce-e5f37ad35600/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/el-club-by-odiseo/events/you-by-odiseo--05-06-2025-1BEE",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centro de Ocio ODISEO, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "ENTRADA SUPER REDUCIDA", "description": "Entrada con precio especial reducido.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_1", "name": "ENTRADA REDUCIDA", "description": "Entrada con precio reducido.", "price": 10, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            },
            {
                "id": "9",
                "venueId": "1",
                "venueName": "MACCAO OPEN AIR CLUB",
                "title": "THE GRAND OPENING MACCAO OPEN AIR 2025",
                "description": "Gran inauguración en MACCAO OPEN AIR CLUB. Una noche épica para dar comienzo a la temporada con música, espectáculos y sorpresas.",
                "date": "2025-06-07",
                "startTime": "22:00",
                "endTime": "07:00",
                "price": 12,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/b66cfadc-d368-4581-0750-104d607e3e00/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/hugo-fernandez-gil/events/the-grand-opening-maccao-open-air-2025-07-06-2025-L6I3",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "ENTRADAS DESPEDIDA SUMMER24", "description": "Entrada al evento.", "price": 12, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_1", "name": "PRIMERAS ENTRADAS", "description": "Entrada al evento.", "price": 12, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_2", "name": "ÚLTIMAS ENTRADAS", "description": "Entrada al evento.", "price": 15, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            },
            {
                "id": "10",
                "venueId": "3",
                "venueName": "EL CLUB by ODISEO",
                "title": "YOU by ODISEO",
                "description": "Evento exclusivo en EL CLUB by ODISEO. Una noche única con la mejor música y ambiente de Murcia.",
                "date": "2025-06-12",
                "startTime": "23:00",
                "endTime": "06:00",
                "price": 8,
                "imageUrl": "https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/db24998f-9e31-4d7a-d1ce-e5f37ad35600/w=550",
                "ticketUrl": "https://www.fourvenues.com/es/el-club-by-odiseo/events/you-by-odiseo--12-06-2025-X1NH",
                "isAvailable": True,
                "capacity": 300,
                "soldTickets": 150,
                "tags": ["Fiestas"],
                "venueAddress": "Centro de Ocio ODISEO, Murcia, España",
                "ticketTypes": [
                    {"id": "ticket_0", "name": "ENTRADA SUPER REDUCIDA", "description": "Entrada con precio especial reducido.", "price": 8, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""},
                    {"id": "ticket_1", "name": "ENTRADA REDUCIDA", "description": "Entrada con precio reducido.", "price": 10, "isAvailable": True, "isSoldOut": False, "isPromotion": False, "isVip": False, "restrictions": ""}
                ]
            }
        ]
    }
    
    return data

def main():
    """Crear y guardar datos completos"""
    print("Creando datos completos...")
    
    data = create_complete_data()
    
    # Guardar datos
    with open('cached_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos creados exitosamente:")
    print(f"   - Venues: {len(data.get('venues', []))}")
    print(f"   - Eventos: {len(data.get('parties', []))}")
    
    # Mostrar resumen
    venues_events = {}
    for party in data.get('parties', []):
        venue_name = party.get('venueName', 'Unknown')
        if venue_name not in venues_events:
            venues_events[venue_name] = []
        venues_events[venue_name].append(party.get('title', 'Sin título'))
    
    print(f"\n📋 Eventos por venue:")
    for venue, events in venues_events.items():
        print(f"   🏢 {venue}: {len(events)} eventos")
        for event in events:
            print(f"      - {event}")

if __name__ == "__main__":
    main() 