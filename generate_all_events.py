#!/usr/bin/env python3
"""
Script para generar datos con todos los eventos de FourVenues
"""

import json
import subprocess
import sys

def run_scraper():
    """Ejecutar el scraper y capturar solo el JSON"""
    try:
        # Ejecutar el scraper con --json-only
        result = subprocess.run([
            sys.executable, 'fourvenues_scraper.py', '--json-only'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            # El JSON está en stderr cuando usamos --json-only
            json_output = result.stdout.strip()
            
            # Buscar el JSON en la salida
            lines = json_output.split('\n')
            json_start = -1
            
            for i, line in enumerate(lines):
                if line.strip().startswith('{'):
                    json_start = i
                    break
            
            if json_start >= 0:
                json_text = '\n'.join(lines[json_start:])
                try:
                    data = json.loads(json_text)
                    return data
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    print(f"JSON text: {json_text[:500]}...")
                    return None
            else:
                print("No se encontró JSON en la salida")
                print(f"Salida completa: {json_output}")
                return None
        else:
            print(f"Error ejecutando scraper: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Generar datos completos"""
    print("Generando datos completos de FourVenues...")
    
    data = run_scraper()
    
    if data and data.get('parties'):
        # Guardar datos
        with open('cached_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos generados exitosamente:")
        print(f"   - Venues: {len(data.get('venues', []))}")
        print(f"   - Eventos: {len(data.get('parties', []))}")
        
        # Mostrar eventos por venue
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
        print("❌ No se pudieron generar los datos")
        return False

if __name__ == "__main__":
    main() 