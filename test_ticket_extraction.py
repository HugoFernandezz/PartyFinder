#!/usr/bin/env python3
"""
Script de prueba para la extracción de tipos de entrada de eventos específicos
Prueba con el evento de Luminata: viernes-reggaetoncomercial-30-05-2025-ZMZ2
"""

import json
import re
from bs4 import BeautifulSoup
from fourvenues_scraper import (
    fetch_html, 
    extract_ticket_types, 
    extract_ticket_types_fallback,
    fix_special_characters
)

def test_luminata_ticket_extraction():
    """Probar la extracción de tipos de entrada del evento específico de Luminata"""
    
    print("=== PRUEBA DE EXTRACCIÓN DE TIPOS DE ENTRADA ===")
    print("Evento: Viernes REGGAETÓN/COMERCIAL - Luminata Disco")
    print("URL: https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2")
    print()
    
    # URL del evento específico
    event_url = "https://www.fourvenues.com/es/luminata-disco/events/viernes-reggaetoncomercial-30-05-2025-ZMZ2"
    
    # Obtener HTML del evento
    print("📥 Descargando HTML del evento...")
    html = fetch_html(event_url)
    
    if not html:
        print("❌ Error: No se pudo obtener el HTML del evento")
        return
    
    print(f"✅ HTML obtenido: {len(html)} caracteres")
    
    # Parsear HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extraer tipos de entrada
    print("\n🎫 Extrayendo tipos de entrada...")
    ticket_types = extract_ticket_types(soup)
    
    if not ticket_types:
        print("⚠️  No se encontraron tipos de entrada con el método principal")
        print("🔄 Intentando método alternativo...")
        ticket_types = extract_ticket_types_fallback(soup)
    
    if ticket_types:
        print(f"✅ Encontrados {len(ticket_types)} tipos de entrada:")
        print()
        
        for i, ticket in enumerate(ticket_types, 1):
            print(f"{i}. {ticket['name']}")
            print(f"   💰 Precio: {ticket['price']}€")
            print(f"   📝 Descripción: {ticket['description']}")
            print(f"   🟢 Disponible: {'Sí' if ticket['isAvailable'] else 'No'}")
            print(f"   🔴 Agotado: {'Sí' if ticket['isSoldOut'] else 'No'}")
            if ticket.get('isPromotion'):
                print(f"   🏷️  Promoción: Sí")
            if ticket.get('isVip'):
                print(f"   ⭐ VIP: Sí")
            if ticket.get('restrictions'):
                print(f"   ⚠️  Restricciones: {ticket['restrictions']}")
            print()
    else:
        print("❌ No se pudieron extraer tipos de entrada")
        print("🔍 Analizando HTML para encontrar patrones...")
        analyze_html_patterns(html)

def analyze_html_patterns(html):
    """Analizar patrones en el HTML para entender la estructura"""
    
    print("\n=== ANÁLISIS DE PATRONES HTML ===")
    
    # Buscar secciones que contengan "entrada" o "precio"
    soup = BeautifulSoup(html, 'html.parser')
    
    # Buscar elementos con texto "ENTRADA"
    entrada_elements = soup.find_all(string=re.compile(r'ENTRADA', re.IGNORECASE))
    print(f"Elementos con 'ENTRADA': {len(entrada_elements)}")
    
    for i, element in enumerate(entrada_elements[:5]):  # Mostrar solo los primeros 5
        parent = element.parent if element.parent else element
        print(f"  {i+1}. {element.strip()}")
        print(f"     Contexto: {parent.get_text()[:100]}...")
        print()
    
    # Buscar elementos con precios (€)
    price_elements = soup.find_all(string=re.compile(r'\d+€'))
    print(f"Elementos con precios: {len(price_elements)}")
    
    for i, element in enumerate(price_elements[:10]):  # Mostrar solo los primeros 10
        parent = element.parent if element.parent else element
        print(f"  {i+1}. {element.strip()}")
        print(f"     Contexto: {parent.get_text()[:80]}...")
        print()
    
    # Buscar secciones específicas
    sections = soup.find_all(['h2', 'h3'], string=re.compile(r'entrada|ticket|precio', re.IGNORECASE))
    print(f"Secciones relacionadas: {len(sections)}")
    
    for section in sections:
        print(f"  - {section.get_text().strip()}")
        # Mostrar contenido siguiente
        next_sibling = section.find_next_sibling()
        if next_sibling:
            print(f"    Contenido: {next_sibling.get_text()[:100]}...")
        print()

def test_manual_extraction():
    """Prueba manual con HTML conocido para verificar la lógica"""
    
    print("\n=== PRUEBA MANUAL CON HTML SIMULADO ===")
    
    # HTML simulado basado en la estructura de FourVenues
    test_html = """
    <div class="tickets-section">
        <h2>Entradas</h2>
        <div class="ticket-item">
            <span class="ticket-name">PROMOCIÓN ENTRADA 1 COPA</span>
            <span class="ticket-price">8€</span>
            <span class="ticket-status">Agotadas</span>
            <p>1 copa de alcohol estándar para consumir antes de las 2:30.</p>
        </div>
        <div class="ticket-item">
            <span class="ticket-name">ENTRADA VIP 1 COPA SIN COLAS Y SIN HORA</span>
            <span class="ticket-price">16€</span>
            <span class="ticket-status">Disponible</span>
            <p>1 copa de alcohol estándar.</p>
        </div>
        <div class="ticket-item">
            <span class="ticket-name">ENTRADA VIP 2 COPAS SIN COLAS Y SIN HORA</span>
            <span class="ticket-price">20€</span>
            <span class="ticket-status">Quedan pocas</span>
            <p>2 Copas de alcohol estándar.</p>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(test_html, 'html.parser')
    ticket_types = extract_ticket_types(soup)
    
    print(f"Tipos de entrada extraídos: {len(ticket_types)}")
    
    for ticket in ticket_types:
        print(f"- {ticket['name']}: {ticket['price']}€ ({'Disponible' if ticket['isAvailable'] else 'Agotado'})")

if __name__ == "__main__":
    test_luminata_ticket_extraction()
    test_manual_extraction() 