#!/usr/bin/env python3
"""
Script para extraer solo el JSON del output del scraper
"""

import subprocess
import json
import sys

def extract_json_from_scraper():
    """Ejecutar scraper y extraer solo el JSON"""
    try:
        # Ejecutar el scraper
        result = subprocess.run([
            sys.executable, 'fourvenues_scraper.py', '--json-only'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            output = result.stdout
            
            # Buscar el inicio del JSON
            json_start = output.find('{\n  "venues":')
            if json_start == -1:
                print("No se encontró el JSON en la salida")
                return None
            
            # Extraer solo la parte JSON
            json_content = output[json_start:]
            
            # Buscar el final del JSON
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
            
            # Parsear y validar el JSON
            try:
                data = json.loads(clean_json)
                return data
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return None
                
        else:
            print(f"Error ejecutando scraper: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Extraer JSON y guardarlo"""
    print("Extrayendo JSON del scraper...")
    
    data = extract_json_from_scraper()
    
    if data:
        # Guardar datos
        with open('cached_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON extraído exitosamente:")
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
        
        return True
    else:
        print("❌ No se pudo extraer el JSON")
        return False

if __name__ == "__main__":
    main() 