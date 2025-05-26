#!/usr/bin/env python3
"""
Script para extraer JSON limpio del scraper original
"""

import subprocess
import re
import json

def extract_json_from_scraper():
    """Ejecutar el scraper original y extraer solo el JSON"""
    try:
        # Ejecutar el scraper original
        result = subprocess.run(['python', 'fourvenues_scraper.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"Error ejecutando scraper: {result.stderr}")
            return None
        
        output = result.stdout
        
        # Buscar el JSON en la salida (empieza con { y termina con })
        json_match = re.search(r'\{[\s\S]*\}', output)
        
        if json_match:
            json_str = json_match.group(0)
            try:
                # Validar que es JSON válido
                data = json.loads(json_str)
                
                # Guardar JSON limpio
                with open('data/events_real.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Datos reales extraídos exitosamente:")
                print(f"   - Venues: {len(data.get('venues', []))}")
                print(f"   - Parties: {len(data.get('parties', []))}")
                print(f"   - Archivo guardado: data/events_real.json")
                
                return data
                
            except json.JSONDecodeError as e:
                print(f"Error parseando JSON: {e}")
                return None
        else:
            print("No se encontró JSON válido en la salida del scraper")
            return None
            
    except Exception as e:
        print(f"Error ejecutando script: {e}")
        return None

if __name__ == "__main__":
    extract_json_from_scraper() 