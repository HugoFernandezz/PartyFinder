#!/usr/bin/env python3
"""
Script para generar datos JSON limpios directamente
"""

import json
import sys
import io
from fourvenues_scraper import scrape_all_venues

def generate_clean_data():
    """Generar datos limpios sin texto de debug"""
    
    # Redirigir stdout temporalmente para capturar solo el JSON
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        # Ejecutar el scraper
        data = scrape_all_venues()
        
        # Restaurar stdout
        sys.stdout = old_stdout
        
        if data:
            # Guardar JSON limpio
            with open('data/events_clean.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos generados exitosamente:")
            print(f"   - Venues: {len(data.get('venues', []))}")
            print(f"   - Parties: {len(data.get('parties', []))}")
            print(f"   - Archivo guardado: data/events_clean.json")
            
            return data
        else:
            print("❌ No se pudieron generar datos")
            return None
            
    except Exception as e:
        # Restaurar stdout en caso de error
        sys.stdout = old_stdout
        print(f"❌ Error generando datos: {e}")
        return None

if __name__ == "__main__":
    generate_clean_data() 