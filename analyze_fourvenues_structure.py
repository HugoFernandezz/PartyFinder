#!/usr/bin/env python3
"""
Script para analizar la estructura HTML específica de FourVenues
y entender cómo extraer correctamente los tipos de entrada
"""

import re
from bs4 import BeautifulSoup
from fourvenues_scraper import fetch_html

def analyze_fourvenues_structure():
    """Analizar la estructura específica de FourVenues para tipos de entrada"""
    
    print("=== ANÁLISIS DE ESTRUCTURA FOURVENUES ===")
    
    # URL del evento específico
    event_url = "https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2"
    
    print(f"Analizando: {event_url}")
    print()
    
    # Obtener HTML
    html = fetch_html(event_url)
    if not html:
        print("❌ Error obteniendo HTML")
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Buscar la sección de "Entradas"
    print("1. BUSCANDO SECCIÓN DE ENTRADAS")
    print("-" * 40)
    
    # Buscar h2 con texto "Entradas"
    entradas_h2 = soup.find('h2', string=re.compile(r'Entradas', re.IGNORECASE))
    if entradas_h2:
        print(f"✅ Encontrado h2: {entradas_h2.get_text()}")
        
        # Buscar el contenedor siguiente
        next_element = entradas_h2.find_next_sibling()
        if next_element:
            print(f"Elemento siguiente: {next_element.name} - {next_element.get('class', [])}")
            
            # Buscar elementos de entrada dentro
            ticket_elements = next_element.find_all(['div', 'article', 'section'])
            print(f"Elementos encontrados: {len(ticket_elements)}")
            
            # Analizar los primeros 3 elementos
            for i, element in enumerate(ticket_elements[:3]):
                print(f"\n--- Elemento {i+1} ---")
                print(f"Tag: {element.name}")
                print(f"Classes: {element.get('class', [])}")
                print(f"Texto: {element.get_text()[:200]}...")
                
                # Buscar precios en este elemento
                prices = element.find_all(string=re.compile(r'\d+€'))
                print(f"Precios encontrados: {[p.strip() for p in prices]}")
                
                # Buscar texto "ENTRADA" o "PROMOCIÓN"
                entrada_text = element.find_all(string=re.compile(r'ENTRADA|PROMOCIÓN|VIP', re.IGNORECASE))
                print(f"Texto de entrada: {[t.strip() for t in entrada_text[:3]]}")
    else:
        print("❌ No se encontró h2 con 'Entradas'")
    
    print("\n" + "="*60)
    
    # 2. Buscar patrones específicos de FourVenues
    print("2. BUSCANDO PATRONES ESPECÍFICOS")
    print("-" * 40)
    
    # Buscar todos los elementos que contengan "ENTRADA"
    entrada_elements = soup.find_all(string=re.compile(r'ENTRADA', re.IGNORECASE))
    print(f"Total elementos con 'ENTRADA': {len(entrada_elements)}")
    
    # Analizar los primeros 5
    for i, element in enumerate(entrada_elements[:5]):
        print(f"\n--- ENTRADA {i+1} ---")
        print(f"Texto: {element.strip()}")
        
        # Obtener el contenedor padre
        parent = element.parent
        if parent:
            print(f"Padre: {parent.name} - {parent.get('class', [])}")
            
            # Buscar precio en el mismo contenedor
            price_in_parent = parent.find(string=re.compile(r'\d+€'))
            if price_in_parent:
                print(f"Precio en padre: {price_in_parent.strip()}")
            
            # Buscar estado (Agotadas, Disponible, etc.)
            status_keywords = ['agotad', 'disponible', 'quedan', 'completa']
            for keyword in status_keywords:
                status = parent.find(string=re.compile(keyword, re.IGNORECASE))
                if status:
                    print(f"Estado encontrado: {status.strip()}")
                    break
            
            # Buscar descripción (copas, alcohol, etc.)
            desc_keywords = ['copa', 'alcohol', 'consumir', 'antes']
            for keyword in desc_keywords:
                desc = parent.find(string=re.compile(keyword, re.IGNORECASE))
                if desc:
                    print(f"Descripción: {desc.strip()}")
                    break
    
    print("\n" + "="*60)
    
    # 3. Buscar estructura de datos JavaScript
    print("3. BUSCANDO DATOS JAVASCRIPT")
    print("-" * 40)
    
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and ('ticket' in script.string.lower() or 'entrada' in script.string.lower()):
            print("Script con datos de tickets encontrado:")
            # Mostrar solo una parte del script
            script_text = script.string[:500]
            print(script_text)
            print("...")
            break
    
    print("\n" + "="*60)
    
    # 4. Buscar por clases CSS específicas
    print("4. BUSCANDO CLASES CSS ESPECÍFICAS")
    print("-" * 40)
    
    # Buscar elementos con clases que podrían contener tickets
    possible_classes = ['ticket', 'entrada', 'price', 'item', 'card', 'product']
    
    for class_name in possible_classes:
        elements = soup.find_all(class_=re.compile(class_name, re.IGNORECASE))
        if elements:
            print(f"Elementos con clase '{class_name}': {len(elements)}")
            
            # Mostrar el primero
            first_element = elements[0]
            print(f"  Primer elemento: {first_element.name} - {first_element.get('class', [])}")
            print(f"  Texto: {first_element.get_text()[:100]}...")
            print()

if __name__ == "__main__":
    analyze_fourvenues_structure() 