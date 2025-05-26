#!/usr/bin/env python3
"""
Script para analizar la estructura específica de páginas de eventos de FourVenues
"""

from fourvenues_scraper import fetch_html
from bs4 import BeautifulSoup
import re

def analyze_event_page(url):
    """Analizar una página específica de evento"""
    print(f"=== ANALIZANDO: {url} ===")
    
    html = fetch_html(url)
    if not html:
        print("No se pudo obtener HTML")
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Buscar sección de entradas
    print('\n1. BUSCANDO SECCIÓN DE ENTRADAS')
    entradas_h2 = soup.find('h2', string=re.compile(r'Entradas', re.IGNORECASE))
    if entradas_h2:
        print('✅ Encontrado h2 "Entradas"')
        
        # Obtener el siguiente elemento
        next_element = entradas_h2.find_next_sibling()
        if next_element:
            print(f'Elemento siguiente: {next_element.name} - Classes: {next_element.get("class", [])}')
            
            # Buscar elementos de entrada dentro
            ticket_containers = next_element.find_all(['div', 'article', 'section'])
            print(f'Contenedores encontrados: {len(ticket_containers)}')
            
            # Analizar los primeros 3 contenedores
            for i, container in enumerate(ticket_containers[:3]):
                print(f'\n--- Contenedor {i+1} ---')
                text = container.get_text().strip()
                if len(text) > 20:  # Solo contenedores con contenido
                    print(f'Texto: {text[:150]}...')
                    
                    # Buscar precios en este contenedor
                    prices = container.find_all(string=re.compile(r'\d+€'))
                    if prices:
                        print(f'Precios: {[p.strip() for p in prices]}')
                    
                    # Buscar estados (agotado, disponible, etc.)
                    states = container.find_all(string=re.compile(r'agotad|disponible|quedan', re.IGNORECASE))
                    if states:
                        print(f'Estados: {[s.strip() for s in states]}')
    else:
        print('❌ No se encontró h2 "Entradas"')
    
    # 2. Buscar todos los precios en la página
    print('\n2. TODOS LOS PRECIOS EN LA PÁGINA')
    price_elements = soup.find_all(string=re.compile(r'\d+€'))
    print(f'Total precios encontrados: {len(price_elements)}')
    
    for i, price in enumerate(price_elements[:10]):  # Solo primeros 10
        container = price.parent
        if container:
            # Buscar hacia arriba para obtener más contexto
            for _ in range(3):
                if container.parent:
                    container = container.parent
                else:
                    break
            
            context = container.get_text().strip()
            # Limpiar el contexto
            context = re.sub(r'\s+', ' ', context)[:200]
            print(f'{i+1}. {price.strip()} - Contexto: {context}')
    
    # 3. Buscar patrones específicos de FourVenues
    print('\n3. PATRONES ESPECÍFICOS DE FOURVENUES')
    
    # Buscar scripts que contengan información de entradas
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'ticket' in script.string.lower():
            # Buscar patrones de datos de entradas
            ticket_data = re.findall(r'ticket[^}]*}', script.string, re.IGNORECASE)
            if ticket_data:
                print(f'Datos de tickets en script: {ticket_data[:2]}')  # Solo primeros 2
                break

def main():
    """Analizar diferentes páginas de eventos"""
    
    # URLs de ejemplo para analizar
    test_urls = [
        "https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2",
        "https://www.fourvenues.com/es/el-club-by-odiseo/events/passion-fruit-x-kybba-30-05-2025-RCWR",
        "https://www.fourvenues.com/es/hugo-fernandez-gil/events/mar-menor-fest-05-06-2025-CZ7W"
    ]
    
    for url in test_urls:
        analyze_event_page(url)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main() 