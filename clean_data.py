#!/usr/bin/env python3
"""
Script para limpiar y extraer solo el JSON válido del scraper
"""

import json
import re

def extract_json_from_file(filename):
    """Extraer solo el JSON válido del archivo"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Buscar el inicio del JSON de manera más flexible
        json_patterns = [
            '{\n  "venues":',
            '{"venues":',
            '{ "venues":',
            '"venues":'
        ]
        
        json_start = -1
        for pattern in json_patterns:
            json_start = content.find(pattern)
            if json_start != -1:
                # Si encontramos "venues": pero no está al inicio, buscar el { anterior
                if not pattern.startswith('{'):
                    # Buscar hacia atrás para encontrar el {
                    for i in range(json_start, -1, -1):
                        if content[i] == '{':
                            json_start = i
                            break
                break
        
        if json_start == -1:
            print("No se encontró el JSON en el archivo")
            print("Primeras 500 caracteres del archivo:")
            print(content[:500])
            return None
        
        # Extraer solo la parte JSON
        json_content = content[json_start:]
        
        # Buscar el final del JSON (último })
        brace_count = 0
        json_end = -1
        
        for i, char in enumerate(json_content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        
        if json_end == -1:
            print("No se encontró el final del JSON")
            return None
        
        # Extraer solo el JSON válido
        clean_json = json_content[:json_end]
        
        # Limpiar caracteres problemáticos
        clean_json = clean_json.replace('Ç', '€')
        clean_json = clean_json.replace('Ë', 'Ó')
        clean_json = clean_json.replace('ß', 'á')
        clean_json = clean_json.replace('·', 'ú')
        clean_json = clean_json.replace('±', 'ñ')
        clean_json = clean_json.replace('¾', 'ó')
        
        # Intentar parsear el JSON
        try:
            data = json.loads(clean_json)
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            # Guardar el JSON problemático para debug
            with open('debug_json.txt', 'w', encoding='utf-8') as f:
                f.write(clean_json)
            return None
            
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return None

def main():
    """Limpiar los datos y generar JSON válido"""
    print("Limpiando datos del scraper...")
    
    data = extract_json_from_file('cached_data.json')
    
    if data:
        # Guardar datos limpios
        with open('cached_data_clean.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos limpiados exitosamente:")
        print(f"   - Venues: {len(data.get('venues', []))}")
        print(f"   - Eventos: {len(data.get('parties', []))}")
        
        # Mostrar resumen por venue
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
        
        return True
    else:
        print("❌ No se pudieron limpiar los datos")
        return False

if __name__ == "__main__":
    main() 