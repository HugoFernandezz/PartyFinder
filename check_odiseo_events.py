#!/usr/bin/env python3
"""
Script para verificar eventos específicos de El Club by Odiseo
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_html(url):
    """Obtener HTML de una URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error obteniendo HTML de {url}: {e}")
        return None

def analyze_odiseo_page():
    """Analizar la página de El Club by Odiseo"""
    url = "https://www.fourvenues.com/es/el-club-by-odiseo"
    
    print("=== ANÁLISIS DE EL CLUB BY ODISEO ===")
    print(f"URL: {url}")
    print()
    
    html = fetch_html(url)
    if not html:
        print("❌ No se pudo obtener el HTML")
        return
    
    print(f"✅ HTML obtenido: {len(html)} caracteres")
    print()
    
    # 1. Buscar todos los slugs de eventos
    print("1. BUSCANDO SLUGS DE EVENTOS")
    print("-" * 40)
    
    event_pattern = r"Event\('([^']+)'"
    event_slugs = re.findall(event_pattern, html)
    
    print(f"Slugs encontrados: {len(event_slugs)}")
    for i, slug in enumerate(event_slugs, 1):
        print(f"  {i}. {slug}")
    print()
    
    # 2. Filtrar eventos reales (excluyendo graduaciones y funciones del sistema)
    print("2. FILTRANDO EVENTOS REALES")
    print("-" * 40)
    
    real_event_slugs = []
    for slug in event_slugs:
        # Excluir graduaciones y funciones del sistema
        if any(exclude in slug.lower() for exclude in ['graduacion', 'select_content', 'page_view']):
            print(f"  ❌ EXCLUIDO: {slug} (graduación/sistema)")
            continue
            
        if any(keyword in slug.lower() for keyword in [
            'fest', 'party', 'fiesta', 'opening', 'ticket', 'bus',
            'concierto', 'evento', 'show', 'night', 'noche', 'club', 'disco',
            'reggaeton', 'comercial', 'play', 'jueves', 'viernes', 'sabado',
            'you', 'odiseo', 'passion', 'fruit', 'kybba', 'examenes'
        ]) and len(slug) > 10:
            real_event_slugs.append(slug)
            print(f"  ✅ INCLUIDO: {slug}")
        else:
            print(f"  ❌ EXCLUIDO: {slug} (no coincide con criterios)")
    
    print(f"\nEventos reales encontrados: {len(real_event_slugs)}")
    print()
    
    # 3. Buscar códigos de eventos
    print("3. BUSCANDO CÓDIGOS DE EVENTOS")
    print("-" * 40)
    
    events_with_codes = []
    for slug in real_event_slugs:
        # Buscar código del evento
        onclick_pattern = rf"onClickEvent\(\s*'{re.escape(slug)}'\s*,\s*'([A-Z0-9]{{4}})'"
        matches = re.findall(onclick_pattern, html, re.IGNORECASE)
        
        if matches:
            code = matches[0]
            events_with_codes.append((slug, code))
            print(f"  ✅ {slug} -> {code}")
        else:
            # Fallback: buscar slug-CODE en cualquier lugar del HTML
            fallback_pattern = rf"{re.escape(slug)}-([A-Z0-9]{{4}})"
            matches = re.findall(fallback_pattern, html)
            if matches:
                code = matches[0]
                events_with_codes.append((slug, code))
                print(f"  ✅ {slug} -> {code} (fallback)")
            else:
                print(f"  ❌ {slug} -> NO CODE FOUND")
    
    print(f"\nEventos con código: {len(events_with_codes)}")
    print()
    
    # 4. Verificar URLs de eventos
    print("4. VERIFICANDO URLs DE EVENTOS")
    print("-" * 40)
    
    for slug, code in events_with_codes:
        full_slug = f"{slug}-{code}"
        event_url = f"https://www.fourvenues.com/es/el-club-by-odiseo/events/{full_slug}"
        
        print(f"Verificando: {event_url}")
        
        # Verificar si la URL existe
        try:
            response = requests.head(event_url, timeout=10, verify=False)
            if response.status_code == 200:
                print(f"  ✅ URL válida (200)")
                
                # Obtener detalles básicos
                event_html = fetch_html(event_url)
                if event_html:
                    soup = BeautifulSoup(event_html, 'html.parser')
                    
                    # Extraer título
                    title_elem = soup.find('h1')
                    title = title_elem.get_text().strip() if title_elem else "Sin título"
                    
                    # Extraer fecha del slug
                    date_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', slug)
                    if date_match:
                        day, month, year = date_match.groups()
                        event_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        event_date = "Fecha no encontrada"
                    
                    print(f"    Título: {title}")
                    print(f"    Fecha: {event_date}")
                    
                    # Verificar si está en el rango de fechas del scraper
                    try:
                        event_datetime = datetime.strptime(event_date, "%Y-%m-%d")
                        today = datetime.now()
                        days_diff = (event_datetime - today).days
                        
                        if -7 <= days_diff <= 30:  # Rango típico del scraper
                            print(f"    ✅ En rango de fechas (días desde hoy: {days_diff})")
                        else:
                            print(f"    ⚠️  Fuera de rango de fechas (días desde hoy: {days_diff})")
                    except:
                        print(f"    ❌ Error procesando fecha")
                        
            else:
                print(f"  ❌ URL no válida ({response.status_code})")
        except Exception as e:
            print(f"  ❌ Error verificando URL: {e}")
        
        print()
    
    # 5. Resumen
    print("5. RESUMEN")
    print("-" * 40)
    print(f"Total slugs encontrados: {len(event_slugs)}")
    print(f"Eventos reales filtrados: {len(real_event_slugs)}")
    print(f"Eventos con código: {len(events_with_codes)}")
    print()
    
    print("Eventos que deberían ser scrapeados:")
    for slug, code in events_with_codes:
        print(f"  - {slug} ({code})")

if __name__ == "__main__":
    analyze_odiseo_page() 