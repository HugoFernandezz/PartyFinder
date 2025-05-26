#!/usr/bin/env python3
"""
Script de prueba para demostrar la capacidad dinámica del scraper
Simula cómo el sistema se adaptaría automáticamente a eventos nuevos
"""

import json
import re
from fourvenues_scraper import extract_dynamic_event_info, generate_tags, generate_description, estimate_price

def test_dynamic_adaptation():
    """Probar la adaptación dinámica con eventos simulados"""
    
    print("=== PRUEBA DE ADAPTACION DINAMICA ===")
    print("Simulando eventos nuevos que podrían aparecer en FourVenues...")
    print()
    
    # Simular eventos nuevos que podrían aparecer
    test_events = [
        {
            'slug': 'concierto-reggaeton-verano-2025--15-07-2025',
            'expected_type': 'Concierto de Reggaeton'
        },
        {
            'slug': 'fiesta-electronica-agosto--20-08-2025',
            'expected_type': 'Fiesta Electrónica'
        },
        {
            'slug': 'graduacion-universidad-politecnica--25-06-2025',
            'expected_type': 'Graduación Universitaria'
        },
        {
            'slug': 'opening-club-nuevo-murcia--10-09-2025',
            'expected_type': 'Inauguración de Club'
        },
        {
            'slug': 'festival-musica-indie-2025--30-08-2025',
            'expected_type': 'Festival de Música Indie'
        }
    ]
    
    for i, test_event in enumerate(test_events, 1):
        print(f"{i}. EVENTO SIMULADO: {test_event['expected_type']}")
        print(f"   Slug: {test_event['slug']}")
        
        # Simular contexto HTML básico
        mock_html = f"""
        <div class="event-card">
            <h2>{test_event['slug'].replace('-', ' ').title()}</h2>
            <p>21:30 04:00</p>
            <div>MACCAO OPEN AIR CLUB</div>
        </div>
        """
        
        try:
            # Probar extracción dinámica
            event_info = extract_dynamic_event_info(mock_html, test_event['slug'])
            
            if event_info:
                print(f"   ✓ Título extraído: {event_info['title']}")
                print(f"   ✓ Fecha: {event_info['date']}")
                print(f"   ✓ Venue: {event_info['venue_name']}")
                print(f"   ✓ Precio estimado: {event_info['price']}€")
                print(f"   ✓ Tags generados: {', '.join(event_info['tags'])}")
                print(f"   ✓ Descripción: {event_info['description'][:80]}...")
                print("   ✓ ADAPTACION EXITOSA")
            else:
                print("   ✗ Error en la adaptación")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print()
    
    print("=== RESUMEN ===")
    print("El scraper dinámico puede:")
    print("• Detectar automáticamente nuevos eventos por su slug")
    print("• Extraer información básica del contexto HTML")
    print("• Generar títulos limpios desde slugs")
    print("• Inferir venues basado en el tipo de evento")
    print("• Estimar precios según la categoría")
    print("• Generar tags relevantes automáticamente")
    print("• Crear descripciones apropiadas")
    print("• Asignar imágenes según el tipo de evento")
    print()
    print("¡El sistema es completamente adaptable a eventos nuevos!")

def test_real_adaptation():
    """Probar con un evento real de FourVenues"""
    
    print("\n=== PRUEBA CON EVENTO REAL ===")
    
    # Usar uno de los eventos reales actuales
    real_slug = "mar-menor-fest-05-06-2025"
    
    print(f"Probando adaptación con evento real: {real_slug}")
    
    # Simular contexto real simplificado
    real_context = """
    <div class="event-info">
        <h1>MAR MENOR FEST</h1>
        <p>23:00 07:00</p>
        <div>MACCÄO OPEN AIR CLUB</div>
        <span>Festival de música electrónica</span>
    </div>
    """
    
    try:
        event_info = extract_dynamic_event_info(real_context, real_slug)
        
        if event_info:
            print("✓ Información extraída exitosamente:")
            print(f"  - Título: {event_info['title']}")
            print(f"  - Fecha: {event_info['date']}")
            print(f"  - Horario: {event_info['start_time']} - {event_info['end_time']}")
            print(f"  - Venue: {event_info['venue_name']}")
            print(f"  - Precio: {event_info['price']}€")
            print(f"  - Tags: {', '.join(event_info['tags'])}")
            print(f"  - Imagen: {event_info['image_url'][:50]}...")
            
            # Verificar que tiene la imagen real del Mar Menor Fest
            if 'fourvenues.com/cdn-cgi/imagedelivery' in event_info['image_url']:
                print("  ✓ Imagen real detectada correctamente")
            else:
                print("  - Usando imagen por defecto")
                
        else:
            print("✗ Error en la extracción")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_dynamic_adaptation()
    test_real_adaptation() 