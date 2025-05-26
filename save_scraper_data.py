#!/usr/bin/env python3
"""
Script para ejecutar el scraper y guardar solo el JSON limpio
"""

import subprocess
import sys
import json
import re

def extract_and_save_json():
    """Ejecutar scraper y extraer solo el JSON"""
    try:
        print("Ejecutando scraper...")
        
        # Ejecutar el scraper
        result = subprocess.run([
            sys.executable, 'fourvenues_scraper.py'
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            output = result.stdout
            print(f"Scraper ejecutado exitosamente. Output: {len(output)} caracteres")
            
            # Buscar el JSON en la salida
            json_start = output.find('{\n  "venues":')
            if json_start == -1:
                print("No se encontró el JSON en la salida")
                return False
            
            # Extraer desde el inicio del JSON hasta el final
            json_content = output[json_start:]
            
            # Buscar el final del JSON contando llaves
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
                return False
            
            # Extraer solo el JSON válido
            clean_json = json_content[:json_end]
            
            # Validar que es JSON válido
            try:
                data = json.loads(clean_json)
                print(f"JSON válido encontrado:")
                print(f"  - Venues: {len(data.get('venues', []))}")
                print(f"  - Eventos: {len(data.get('parties', []))}")
                
                # Guardar el JSON limpio
                with open('cached_data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print("✅ Datos guardados exitosamente en cached_data.json")
                return True
                
            except json.JSONDecodeError as e:
                print(f"Error: JSON inválido - {e}")
                return False
                
        else:
            print(f"Error ejecutando scraper: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = extract_and_save_json()
    if success:
        print("🎉 Proceso completado exitosamente")
    else:
        print("❌ Error en el proceso") 