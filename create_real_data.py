#!/usr/bin/env python3
"""
Script para crear datos reales de FourVenues
"""

import subprocess
import json
import re

def create_real_data():
    """Crear archivo de datos reales"""
    try:
        # Ejecutar el scraper original
        result = subprocess.run(['python', 'fourvenues_scraper.py'], 
                              capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode != 0:
            print(f"Error ejecutando scraper: {result.stderr}")
            return False
        
        output = result.stdout
        
        # Buscar el JSON en la salida (desde la última aparición de {)
        json_start = output.rfind('{')
        if json_start == -1:
            print("No se encontró JSON en la salida")
            return False
        
        json_str = output[json_start:]
        
        try:
            # Validar que es JSON válido
            data = json.loads(json_str)
            
            # Guardar JSON limpio
            with open('data/events_real.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos reales creados exitosamente:")
            print(f"   - Venues: {len(data.get('venues', []))}")
            print(f"   - Parties: {len(data.get('parties', []))}")
            print(f"   - Archivo guardado: data/events_real.json")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error parseando JSON: {e}")
            print(f"JSON encontrado: {json_str[:200]}...")
            return False
            
    except Exception as e:
        print(f"Error ejecutando script: {e}")
        return False

if __name__ == "__main__":
    create_real_data() 