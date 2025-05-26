#!/usr/bin/env python3
"""
Script de debug para encontrar códigos de evento en FourVenues
"""

import re
import requests

def debug_event_codes():
    """Debug para encontrar códigos de evento"""
    
    try:
        # Obtener HTML
        response = requests.get('https://www.fourvenues.com/es/hugo-fernandez-gil')
        html = response.text
        
        print(f"HTML obtenido: {len(html)} caracteres")
        
        # Buscar todos los patrones que podrían contener códigos de evento
        patterns = [
            r'events/([^"\'>\s]+)',  # Cualquier cosa después de events/
            r'href="[^"]*events/([^"]+)"',  # Enlaces a eventos
            r'graduacion-[^"\'>\s]+',  # Eventos de graduación específicos
            r'mar-menor-fest-[^"\'>\s]+',  # Eventos de Mar Menor específicos
            r'ticket-bus-[^"\'>\s]+',  # Eventos de ticket bus específicos
            r'the-grand-opening-[^"\'>\s]+',  # Eventos de grand opening específicos
        ]
        
        print("\n=== BUSCANDO CÓDIGOS DE EVENTO ===")
        
        for i, pattern in enumerate(patterns):
            print(f"\nPatrón {i+1}: {pattern}")
            matches = re.findall(pattern, html, re.IGNORECASE)
            
            # Filtrar y mostrar matches únicos
            unique_matches = list(set(matches))
            print(f"Encontrados {len(unique_matches)} matches únicos:")
            
            for match in unique_matches[:10]:  # Mostrar solo los primeros 10
                print(f"  - {match}")
        
        # Buscar específicamente los eventos que conocemos
        known_events = [
            'graduacion-5-junio--05-06-2025',
            'ticket-bus---mar-menor-fest-05-06-2025',
            'mar-menor-fest-05-06-2025',
            'graduacion-6-junio--06-06-2025',
            'graduacion-6-junio--nuestra-snra-la-06-06-2025',
            'the-grand-opening-maccao-open-air-2025-07-06-2025',
            'graduacion-13-junio-alquerias--13-06-2025'
        ]
        
        print("\n=== BUSCANDO EVENTOS CONOCIDOS CON CÓDIGOS ===")
        
        for event in known_events:
            print(f"\nBuscando códigos para: {event}")
            
            # Buscar con diferentes patrones
            search_patterns = [
                rf'{re.escape(event)}-([A-Z0-9]{{4}})',
                rf'events/{re.escape(event)}-([A-Z0-9]{{4}})',
                rf'href="[^"]*{re.escape(event)}-([A-Z0-9]{{4}})',
            ]
            
            found = False
            for pattern in search_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    print(f"  ✅ Código encontrado: {matches[0]} (patrón: {pattern})")
                    found = True
                    break
            
            if not found:
                print(f"  ❌ No se encontró código")
                
                # Buscar cualquier mención del evento
                if event in html:
                    print(f"  ℹ️  El evento SÍ aparece en el HTML")
                    
                    # Buscar contexto alrededor del evento
                    pos = html.find(event)
                    if pos != -1:
                        start = max(0, pos - 100)
                        end = min(len(html), pos + len(event) + 100)
                        context = html[start:end]
                        print(f"  📝 Contexto: ...{context}...")
                else:
                    print(f"  ❌ El evento NO aparece en el HTML")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_event_codes() 