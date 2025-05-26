#!/usr/bin/env python3
"""
Análisis profundo de la estructura de entradas en FourVenues
"""

from fourvenues_scraper import fetch_html
from bs4 import BeautifulSoup
import re
import json

def deep_analyze_tickets(url):
    """Análisis profundo de la estructura de entradas"""
    print(f"=== ANÁLISIS PROFUNDO: {url} ===")
    
    html = fetch_html(url)
    if not html:
        print("No se pudo obtener HTML")
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Buscar en scripts por datos JSON
    print('\n1. BUSCANDO DATOS JSON EN SCRIPTS')
    scripts = soup.find_all('script')
    for i, script in enumerate(scripts):
        if script.string:
            # Buscar objetos que contengan información de tickets
            if 'price' in script.string.lower() and 'ticket' in script.string.lower():
                print(f'Script {i} contiene datos de tickets y precios')
                
                # Buscar patrones JSON
                json_patterns = [
                    r'\{[^{}]*"price"[^{}]*\}',
                    r'\{[^{}]*"ticket"[^{}]*\}',
                    r'\{[^{}]*"name"[^{}]*"price"[^{}]*\}',
                ]
                
                for pattern in json_patterns:
                    matches = re.findall(pattern, script.string, re.IGNORECASE)
                    if matches:
                        print(f'Patrones JSON encontrados: {len(matches)}')
                        for j, match in enumerate(matches[:3]):  # Solo primeros 3
                            print(f'  {j+1}. {match}')
                        break
    
    # 2. Buscar elementos con clases específicas de tickets
    print('\n2. BUSCANDO ELEMENTOS CON CLASES DE TICKETS')
    
    # Buscar elementos que podrían contener información de tickets
    ticket_selectors = [
        '[class*="ticket"]',
        '[class*="entry"]',
        '[class*="entrada"]',
        '[class*="price"]',
        '[class*="cost"]',
        '[data-price]',
        '[data-ticket]'
    ]
    
    for selector in ticket_selectors:
        elements = soup.select(selector)
        if elements:
            print(f'Selector "{selector}": {len(elements)} elementos')
            for i, elem in enumerate(elements[:3]):  # Solo primeros 3
                text = elem.get_text().strip()[:100]
                classes = elem.get('class', [])
                print(f'  {i+1}. Classes: {classes} - Texto: {text}')
    
    # 3. Buscar estructura de lista/grid de entradas
    print('\n3. BUSCANDO ESTRUCTURA DE LISTA DE ENTRADAS')
    
    # Buscar contenedores que podrían tener múltiples entradas
    container_selectors = [
        'ul', 'ol', '.grid', '.list', '.tickets', '.entries',
        '[class*="grid"]', '[class*="list"]', '[class*="container"]'
    ]
    
    for selector in container_selectors:
        containers = soup.select(selector)
        for container in containers:
            # Contar cuántos precios hay en este contenedor
            prices_in_container = container.find_all(string=re.compile(r'\d+€'))
            if len(prices_in_container) >= 2:  # Al menos 2 precios = posible lista de entradas
                print(f'Contenedor "{selector}" con {len(prices_in_container)} precios:')
                text = container.get_text().strip()[:200]
                print(f'  Texto: {text}')
                
                # Buscar elementos hijos que podrían ser entradas individuales
                children = container.find_all(['li', 'div', 'article', 'section'])
                ticket_children = []
                for child in children:
                    child_prices = child.find_all(string=re.compile(r'\d+€'))
                    if child_prices:  # Si tiene precio, podría ser una entrada
                        ticket_children.append(child)
                
                if ticket_children:
                    print(f'  Posibles entradas individuales: {len(ticket_children)}')
                    for i, ticket in enumerate(ticket_children[:3]):
                        ticket_text = ticket.get_text().strip()
                        ticket_text = re.sub(r'\s+', ' ', ticket_text)[:150]
                        print(f'    {i+1}. {ticket_text}')
    
    # 4. Buscar patrones específicos de texto
    print('\n4. BUSCANDO PATRONES DE TEXTO ESPECÍFICOS')
    
    page_text = soup.get_text()
    
    # Buscar secciones que contengan múltiples entradas
    lines = page_text.split('\n')
    ticket_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        # Buscar líneas que contengan información de entrada
        if re.search(r'(entrada|ticket|promoción|vip)', line, re.IGNORECASE) and re.search(r'\d+€', line):
            ticket_lines.append((i, line))
    
    if ticket_lines:
        print(f'Líneas con información de entradas: {len(ticket_lines)}')
        for i, (line_num, line) in enumerate(ticket_lines[:5]):
            print(f'  {i+1}. Línea {line_num}: {line[:100]}')

def main():
    """Analizar una página específica en detalle"""
    
    # Analizar una página que sabemos que tiene entradas
    url = "https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2"
    deep_analyze_tickets(url)

if __name__ == "__main__":
    main() 