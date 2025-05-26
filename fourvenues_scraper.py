#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import http.client
import ssl
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import sys
import os

# Configurar codificación para Windows de forma más compatible
if sys.platform.startswith('win'):
    # No forzar UTF-8 en Windows PowerShell, usar la codificación nativa
    pass
else:
    # Solo en sistemas Unix usar UTF-8
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Deshabilitar advertencias SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SCRAPER DINAMICO PARA FOURVENUES - EXTRAE EVENTOS DE MULTIPLES VENUES

# Configuración SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# CONFIGURACION DE VENUES - Lista de venues a scrapear
FOURVENUES_VENUES = [
    {
        'name': 'Hugo Fernandez Gil',
        'url': 'https://www.fourvenues.com/es/hugo-fernandez-gil',
        'venue_info': {
            'name': 'MACCAO OPEN AIR CLUB',
            'address': 'Paraje Los Valencianos, s/n, 30730 San Javier, Murcia, España',
            'category': 'Club'
        }
    },
    {
        'name': 'Luminata Disco',
        'url': 'https://www.fourvenues.com/es/luminata-disco',
        'venue_info': {
            'name': 'LUMINATA DISCO',
            'address': 'Centrofama, Calle Teniente General Gutierrez Mellado, 9, 30008 Murcia (Murcia), España',
            'category': 'Discoteca',
            'default_hours': {'start': '23:30', 'end': '07:00'}
        }
    },
    {
        'name': 'El Club by Odiseo',
        'url': 'https://www.fourvenues.com/es/el-club-by-odiseo',
        'venue_info': {
            'name': 'EL CLUB by ODISEO',
            'address': 'Centro de Ocio ODISEO, Murcia, España',
            'category': 'Discoteca',
            'default_hours': {'start': '23:00', 'end': '06:00'}
        }
    }
]

def fetch_html(url, retry_count=0, max_retries=3):
    """Obtener HTML de una URL con reintentos automáticos usando requests"""
    try:
        # Esperar entre requests para evitar rate limiting
        import time
        
        if retry_count > 0:
            wait_time = retry_count * 10  # 10, 20, 30 segundos
            print(f"Esperando {wait_time} segundos antes del reintento {retry_count}...")
            time.sleep(wait_time)
        else:
            # Delay inicial para evitar rate limiting
            time.sleep(3)  # 3 segundos entre cada request inicial
        
        # Headers simplificados que funcionan
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Usar requests con timeout
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 429:  # Rate limited
            print(f"Rate limited (429) para {url}")
            if retry_count < max_retries:
                return fetch_html(url, retry_count + 1, max_retries)
            else:
                print(f"Máximo de reintentos alcanzado para {url}")
                return ""
        elif response.status_code != 200:
            print(f"Error HTTP {response.status_code} para {url}")
            if retry_count < max_retries and response.status_code >= 500:  # Server errors
                return fetch_html(url, retry_count + 1, max_retries)
            return ""
        
        # Obtener el contenido como texto
        html_content = response.text
        print(f"HTML obtenido: {len(html_content)} caracteres")
        
        return html_content
            
    except Exception as e:
        print(f"Error obteniendo {url}: {e}")
        if retry_count < max_retries:
            return fetch_html(url, retry_count + 1, max_retries)
        return ""

def extract_events_from_venue(venue_config):
    """Extraer eventos de un venue específico"""
    print(f"\nProcesando venue: {venue_config['name']}")
    print(f"URL: {venue_config['url']}")
    
    html = fetch_html(venue_config['url'])
    if not html:
        print(f"No se pudo obtener HTML de {venue_config['name']}")
        return []
    
    print(f"HTML obtenido: {len(html)} caracteres")
    
    # Extraer eventos usando la estrategia dinámica
    events = extract_event_data_from_html(html, venue_config['url'], venue_config['venue_info'])
    
    print(f"Encontrados {len(events)} eventos en {venue_config['name']}")
    return events

def extract_event_data_from_html(html, base_url, venue_info):
    """ESTRATEGIA COMPLETAMENTE DINAMICA: Extraer TODOS los eventos automáticamente sin definiciones manuales"""
    
    events_found = []
    
    print(f"Analizando HTML de {len(html)} caracteres...")
    
    # PASO 1: Encontrar todos los eventos usando el patrón onClickEvent que SÍ FUNCIONA
    # Este patrón contiene: slug del evento, código de 4 caracteres, venue, y timestamp
    event_pattern = r"onClickEvent\(\s*'([^']+)'\s*,\s*'([A-Z0-9]{4})'\s*,\s*'([^']+)'\s*,\s*'[^']*'\s*,\s*'(\d+)'\s*\)"
    
    matches = re.findall(event_pattern, html)
    print(f"Eventos detectados con onClickEvent: {len(matches)}")
    
    if not matches:
        print("No se encontraron eventos con el patrón onClickEvent")
        return []
    
    # PASO 2: Procesar cada evento encontrado dinámicamente
    for i, (slug, code, venue_slug, timestamp) in enumerate(matches):
        try:
            print(f"\nProcesando evento {i+1}/{len(matches)}: {slug}")
            print(f"  Código: {code}")
            print(f"  Venue: {venue_slug}")
            print(f"  Timestamp: {timestamp}")
            
            # Construir el slug completo del evento
            full_slug = f"{slug}-{code}"
            
            # Construir URL del evento basada en el venue detectado
            event_url = f"https://www.fourvenues.com/es/{venue_slug}/events/{full_slug}"
            print(f"  URL del evento: {event_url}")
            
            # Extraer información completa del evento
            event_info = extract_complete_event_info(event_url, slug, code, timestamp, venue_info)
            
            if event_info:
                # Verificar si el evento está en el rango de fechas válido
                if is_event_in_date_range(event_info['date']):
                    events_found.append(event_info)
                    print(f"  [OK] Evento agregado: {event_info['title']} - {event_info['date']}")
                else:
                    print(f"  [SKIP] Evento fuera de rango: {event_info['title']} - {event_info['date']}")
            else:
                print(f"  [ERROR] No se pudo extraer información del evento")
                
        except Exception as e:
            print(f"  [ERROR] Error procesando evento {slug}: {e}")
            continue
    
    print(f"\nTotal de eventos válidos encontrados: {len(events_found)}")
    return events_found

def extract_complete_event_info(event_url, slug, code, timestamp, venue_info):
    """Extraer información completa del evento de forma completamente dinámica"""
    
    print(f"    Descargando página del evento...")
    
    # Descargar HTML de la página del evento
    event_html = fetch_html(event_url)
    if not event_html:
        print(f"    [ERROR] No se pudo descargar la página del evento")
        return None
    
    print(f"    HTML descargado: {len(event_html)} caracteres")
    
    # Usar BeautifulSoup para parsing más robusto
    soup = BeautifulSoup(event_html, 'html.parser')
    
    # Extraer información básica del evento
    event_info = {
        'event_url': event_url,
        'slug': slug,
        'code': code,
        'timestamp': timestamp
    }
    
    # 1. TÍTULO - Extraer dinámicamente
    title = extract_dynamic_title(soup, event_html)
    if not title:
        # Fallback: generar título desde el slug
        title = generate_title_from_slug(slug)
    event_info['title'] = title
    
    # 2. FECHA - Extraer del timestamp o del HTML
    date_str = extract_dynamic_date(soup, event_html, timestamp)
    event_info['date'] = date_str
    
    # 3. HORARIOS - Extraer dinámicamente o usar defaults del venue
    start_time, end_time = extract_dynamic_times(soup, event_html, venue_info)
    event_info['start_time'] = start_time
    event_info['end_time'] = end_time
    
    # 4. IMAGEN - Extraer dinámicamente
    image_url = extract_dynamic_image(soup, event_html, event_url)
    event_info['image_url'] = image_url
    
    # 5. TIPOS DE ENTRADA Y PRECIOS - Extraer dinámicamente
    ticket_types = extract_dynamic_ticket_types(soup, event_html)
    event_info['ticket_types'] = ticket_types
    
    # 6. PRECIO MÍNIMO - Calcular del precio más bajo disponible
    min_price = extract_minimum_price(ticket_types)
    event_info['price'] = min_price
    
    # 7. INFORMACIÓN DEL VENUE
    event_info['venue_name'] = venue_info.get('name', 'Venue Murcia')
    event_info['venue_address'] = venue_info.get('address', 'Murcia, España')
    
    # 8. DESCRIPCIÓN - Generar dinámicamente
    event_info['description'] = generate_dynamic_description(event_info['title'], venue_info.get('name', ''))
    
    # 9. URL DE TICKETS - Usar la URL del evento como fallback
    event_info['ticket_url'] = event_url
    
    # 10. TAGS - Generar dinámicamente
    event_info['tags'] = generate_dynamic_tags(event_info['title'])
    
    # Limpiar caracteres especiales SOLO en campos específicos, NO en títulos
    for key in ['description', 'venue_name', 'venue_address']:
        if event_info.get(key):
            event_info[key] = fix_special_characters(event_info[key])
    
    print(f"    [OK] Información extraída: {event_info['title']} - {event_info['date']} - {event_info['price']}€")
    
    return event_info

def generate_title_from_slug(slug):
    """Generar un título legible desde el slug del evento"""
    if not slug:
        return "Evento"
    
    # Remover códigos y limpiar el slug
    title = slug.replace('-', ' ').replace('_', ' ')
    
    # Remover fechas del final (formato DD-MM-YYYY)
    title = re.sub(r'\s+\d{1,2}\s+\d{1,2}\s+\d{4}$', '', title)
    
    # Capitalizar palabras importantes
    words = title.split()
    capitalized_words = []
    
    for word in words:
        word_lower = word.lower()
        
        # Palabras que deben ir en mayúsculas
        if word_lower in ['reggaeton', 'reggaetón', 'vip', 'dj', 'you', 'by', 'odiseo', 'play', 'on']:
            if word_lower == 'reggaeton':
                capitalized_words.append('REGGAETÓN')
            elif word_lower == 'reggaetón':
                capitalized_words.append('REGGAETÓN')
            else:
                capitalized_words.append(word.upper())
        # Días de la semana
        elif word_lower in ['jueves', 'viernes', 'sabado', 'sábado', 'domingo', 'lunes', 'martes', 'miercoles', 'miércoles']:
            capitalized_words.append(word_lower.capitalize())
        # Palabras comunes
        elif word_lower in ['comercial', 'especial', 'examenes', 'exámenes', 'passion', 'fruit', 'kybba', 'fest', 'festival', 'opening', 'grand', 'maccao', 'air', 'club', 'ticket', 'bus', 'mar', 'menor']:
            capitalized_words.append(word_lower.capitalize())
        # Números y códigos
        elif word.isdigit() or len(word) <= 2:
            capitalized_words.append(word.upper())
        else:
            capitalized_words.append(word.capitalize())
    
    title = ' '.join(capitalized_words)
    
    # Correcciones específicas
    corrections = {
        'Reggaetoncomercial': 'REGGAETÓN COMERCIAL',
        'Playonreggaeton': 'PLAY ON REGGAETÓN',
        'Playonreggaetón': 'PLAY ON REGGAETÓN',
        'You By Odiseo': 'YOU by ODISEO',
        'Passion Fruit X Kybba': 'Passion Fruit x Kybba',
        'Mar Menor Fest': 'Mar Menor Fest',
        'The Grand Opening Maccao Open Air': 'The Grand Opening MACCAO Open Air',
        'Ticket Bus': 'Ticket Bus',
    }
    
    for wrong, correct in corrections.items():
        title = title.replace(wrong, correct)
    
    return title.strip() or "Evento"

def extract_dynamic_title(soup, html):
    """Extraer título del evento de forma dinámica con mejor manejo de caracteres especiales"""
    
    # Método 1: Buscar títulos específicos en elementos H1, H2 que contengan el nombre real del evento
    for tag in ['h1', 'h2', 'h3']:
        headers = soup.find_all(tag)
        for header in headers:
            title_text = header.get_text().strip()
            # Filtrar títulos que parezcan reales (no genéricos)
            if (title_text and len(title_text) > 3 and 
                not title_text.lower().startswith('fourvenues') and
                not title_text.lower().startswith('información') and
                not title_text.lower().startswith('ubicación') and
                not title_text.lower().startswith('entradas') and
                # Buscar títulos que parezcan nombres de eventos
                (any(word in title_text.upper() for word in ['FEST', 'PARTY', 'NIGHT', 'REGGAETON', 'REGGAETÓN', 'COMERCIAL', 'VIP', 'OPENING', 'CLUB']) or
                 len(title_text.split()) >= 2)):
                return clean_title(title_text)
    
    # Método 2: headerComponent.setTitle en JavaScript (más confiable)
    title_match = re.search(r'headerComponent\.setTitle\(\s*["\'](.+?)["\']\s*\)', html)
    if title_match:
        title = title_match.group(1).strip()
        if title and len(title) > 3:
            return clean_title(title)
    
    # Método 3: Buscar en el contenido de scripts por patrones específicos de eventos
    scripts = soup.find_all("script")
    for script in scripts:
        if not script.string:
            continue
        
        # Buscar patrones específicos de títulos de eventos
        title_patterns = [
            r'"title"\s*:\s*"([^"]+)"',  # "title": "TITULO"
            r'"name"\s*:\s*"([^"]+)"',   # "name": "TITULO"
            r'title:\s*"([^"]+)"',       # title: "TITULO"
            r'eventTitle:\s*"([^"]+)"',  # eventTitle: "TITULO"
            r'"eventName"\s*:\s*"([^"]+)"',  # "eventName": "TITULO"
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, script.string)
            for match in matches:
                # Filtrar títulos que parezcan reales (no genéricos)
                if (len(match) > 5 and 
                    not match.lower().startswith('fourvenues') and
                    not match.lower().startswith('luminata fourvenues') and
                    not match.lower().startswith('el club by odiseo fourvenues') and
                    not match.lower().startswith('hugo fernandez gil fourvenues')):
                    return clean_title(match)
    
    # Método 4: Meta tags Open Graph
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        title = og_title['content'].strip()
        if title and len(title) > 3:
            # Limpiar texto común de FourVenues del meta tag
            title = re.sub(r'\s*[-|]\s*FourVenues.*$', '', title, flags=re.IGNORECASE)
            if title and not title.lower().startswith('fourvenues'):
                return clean_title(title)
    
    # Método 5: Título de la página
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text().strip()
        # Limpiar texto común de FourVenues
        title = re.sub(r'\s*[-|]\s*FourVenues.*$', '', title, flags=re.IGNORECASE)
        if title and len(title) > 3 and not title.lower().startswith('fourvenues'):
            return clean_title(title)
    
    # Método 6: Buscar en elementos con clases específicas de eventos
    event_selectors = [
        '.event-title',
        '.event-name', 
        '.title',
        '.name',
        '[class*="title"]',
        '[class*="name"]',
        '[class*="event"]'
    ]
    
    for selector in event_selectors:
        elements = soup.select(selector)
        for element in elements:
            title_text = element.get_text().strip()
            if (title_text and len(title_text) > 3 and 
                not title_text.lower().startswith('fourvenues') and
                not title_text.lower().startswith('información') and
                not title_text.lower().startswith('ubicación')):
                return clean_title(title_text)
    
    # Método 7: Buscar texto que parezca título de evento en todo el HTML
    # Buscar líneas que contengan palabras clave de eventos
    text_lines = soup.get_text().split('\n')
    for line in text_lines:
        line = line.strip()
        if (line and len(line) > 5 and len(line) < 100 and
            any(word in line.upper() for word in ['FEST', 'FESTIVAL', 'PARTY', 'NIGHT', 'REGGAETON', 'REGGAETÓN', 'COMERCIAL', 'OPENING', 'CLUB']) and
            not any(word in line.lower() for word in ['información', 'ubicación', 'entradas', 'precio', 'hora', 'fecha'])):
            return clean_title(line)
    
    return None

def clean_title(title):
    """Limpiar y normalizar títulos manteniendo caracteres especiales"""
    if not title:
        return title
    
    # NO aplicar fix_special_characters aquí para mantener tildes y ñ
    
    # Limpiar títulos duplicados
    words = title.split()
    if len(words) > 2:
        mid = len(words) // 2
        first_half = ' '.join(words[:mid])
        second_half = ' '.join(words[mid:mid*2])
        if first_half == second_half:
            title = first_half
    
    # Correcciones específicas manteniendo caracteres especiales
    corrections = {
        'REGGAETÓNCOMERCIAL': 'REGGAETÓN COMERCIAL',
        'REGGAETONCOMERCIAL': 'REGGAETÓN COMERCIAL',
        'PLAYONREGGAETON': 'PLAY ON REGGAETON',
        'PLAYONREGGAETÓN': 'PLAY ON REGGAETÓN',
    }
    
    for wrong, correct in corrections.items():
        title = title.replace(wrong, correct)
    
    return title.strip()

def extract_dynamic_date(soup, html, timestamp):
    """Extraer fecha del evento de forma dinámica"""
    
    # Método 1: Convertir timestamp si está disponible
    if timestamp and timestamp.isdigit():
        try:
            from datetime import datetime
            event_date = datetime.fromtimestamp(int(timestamp))
            return event_date.strftime("%Y-%m-%d")
        except:
            pass
    
    # Método 2: Buscar patrones de fecha en JavaScript
    date_patterns = [
        r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
        r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            try:
                if len(match[0]) == 4:  # YYYY-MM-DD
                    year, month, day = match
                else:  # DD-MM-YYYY o DD/MM/YYYY
                    day, month, year = match
                
                # Validar fecha
                date_obj = datetime(int(year), int(month), int(day))
                return date_obj.strftime("%Y-%m-%d")
            except:
                continue
    
    # Método 3: Buscar en elementos HTML
    date_selectors = [
        'time[datetime]',
        '.date',
        '.event-date',
        '[class*="date"]'
    ]
    
    for selector in date_selectors:
        element = soup.select_one(selector)
        if element:
            # Buscar en atributo datetime
            datetime_attr = element.get('datetime')
            if datetime_attr:
                try:
                    date_obj = datetime.fromisoformat(datetime_attr.split('T')[0])
                    return date_obj.strftime("%Y-%m-%d")
                except:
                    pass
            
            # Buscar en texto del elemento
            text = element.get_text().strip()
            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    try:
                        if len(match.group(1)) == 4:
                            year, month, day = match.groups()
                        else:
                            day, month, year = match.groups()
                        
                        date_obj = datetime(int(year), int(month), int(day))
                        return date_obj.strftime("%Y-%m-%d")
                    except:
                        continue
    
    # Fallback: fecha de mañana
    from datetime import datetime, timedelta
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

def extract_dynamic_times(soup, html, venue_info):
    """Extraer horarios del evento de forma dinámica"""
    
    # Usar horarios por defecto del venue si están disponibles
    if venue_info.get('default_hours'):
        return venue_info['default_hours']['start'], venue_info['default_hours']['end']
    
    # Buscar horarios en el HTML
    time_patterns = [
        r'(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})',  # HH:MM - HH:MM
        r'(\d{1,2}):(\d{2})',  # HH:MM individual
    ]
    
    times_found = []
    for pattern in time_patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if len(match) == 4:  # Rango de tiempo
                start_hour, start_min, end_hour, end_min = match
                start_time = f"{start_hour.zfill(2)}:{start_min}"
                end_time = f"{end_hour.zfill(2)}:{end_min}"
                return start_time, end_time
            elif len(match) == 2:  # Tiempo individual
                hour, minute = match
                time_str = f"{hour.zfill(2)}:{minute}"
                times_found.append(time_str)
    
    # Si encontramos tiempos individuales, usar el primero como inicio
    if times_found:
        return times_found[0], "07:00"
    
    # Fallback: horarios típicos de discoteca
    return "23:30", "07:00"

def extract_dynamic_image(soup, html, event_url):
    """Extraer imagen del evento de forma dinámica desde el CDN de FourVenues"""
    
    # Método 1: Buscar imágenes del CDN de FourVenues en el HTML (más específico)
    # Patrón para el CDN de FourVenues con diferentes tamaños
    cdn_patterns = [
        r'https://fourvenues\.com/cdn-cgi/imagedelivery/[^/]+/([^/]+)/w=\d+',  # Con tamaño específico
        r'https://fourvenues\.com/cdn-cgi/imagedelivery/[^/]+/([^/]+)',        # Sin tamaño
        r'fourvenues\.com/cdn-cgi/imagedelivery/[^/]+/([^/]+)/w=\d+',         # Sin https
        r'fourvenues\.com/cdn-cgi/imagedelivery/[^/]+/([^/]+)',               # Sin https ni tamaño
    ]
    
    for pattern in cdn_patterns:
        matches = re.findall(pattern, html)
        if matches:
            # Tomar la primera imagen encontrada y construir URL con tamaño w=550
            image_id = matches[0]
            # Construir URL completa con el tamaño estándar para la app
            cdn_url = f"https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/{image_id}/w=550"
            print(f"    [OK] Imagen CDN encontrada: {cdn_url}")
            return cdn_url
    
    # Método 2: Buscar en meta tags Open Graph
    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        image_url = og_image['content']
        # Si es del CDN de FourVenues, asegurar que tenga el tamaño correcto
        if 'fourvenues.com/cdn-cgi/imagedelivery' in image_url:
            # Extraer el ID de la imagen y reconstruir con tamaño w=550
            match = re.search(r'/([^/]+)/w=\d+$', image_url)
            if match:
                image_id = match.group(1)
                return f"https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/{image_id}/w=550"
            else:
                # Si no tiene tamaño, agregarlo
                match = re.search(r'/([^/]+)$', image_url)
                if match:
                    image_id = match.group(1)
                    return f"https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/{image_id}/w=550"
        return image_url
    
    # Método 3: Buscar en background-image CSS
    bg_pattern = r'background-image\s*:\s*url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)'
    bg_matches = re.findall(bg_pattern, html, re.IGNORECASE)
    for match in bg_matches:
        if 'fourvenues.com/cdn-cgi/imagedelivery' in match:
            # Extraer ID y reconstruir URL
            id_match = re.search(r'/([^/]+)(?:/w=\d+)?$', match)
            if id_match:
                image_id = id_match.group(1)
                return f"https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/{image_id}/w=550"
            return match
    
    # Método 4: Buscar en elementos img con src del CDN
    img_elements = soup.find_all('img')
    for img in img_elements:
        src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if src and 'fourvenues.com/cdn-cgi/imagedelivery' in src:
            # Extraer ID y reconstruir URL
            id_match = re.search(r'/([^/]+)(?:/w=\d+)?$', src)
            if id_match:
                image_id = id_match.group(1)
                return f"https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/{image_id}/w=550"
            return src
    
    # Método 5: Buscar patrones específicos en scripts JavaScript
    # Buscar asignaciones de imágenes en JavaScript
    js_image_patterns = [
        r'image["\']?\s*[:=]\s*["\']([^"\']+fourvenues\.com/cdn-cgi/imagedelivery/[^"\']+)["\']',
        r'src["\']?\s*[:=]\s*["\']([^"\']+fourvenues\.com/cdn-cgi/imagedelivery/[^"\']+)["\']',
        r'url["\']?\s*[:=]\s*["\']([^"\']+fourvenues\.com/cdn-cgi/imagedelivery/[^"\']+)["\']',
    ]
    
    for pattern in js_image_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            image_url = matches[0]
            # Extraer ID y reconstruir URL
            id_match = re.search(r'/([^/]+)(?:/w=\d+)?$', image_url)
            if id_match:
                image_id = id_match.group(1)
                return f"https://fourvenues.com/cdn-cgi/imagedelivery/kWuoTchaMsk7Xnc_FNem7A/{image_id}/w=550"
            return image_url
    
    # Método 6: Buscar cualquier imagen como fallback
    img_selectors = [
        'img[src*="event"]',
        'img[src*="banner"]',
        '.hero-image img',
        '.event-image img',
        'img'
    ]
    
    for selector in img_selectors:
        img = soup.select_one(selector)
        if img:
            src = img.get('src') or img.get('data-src')
            if src:
                # Convertir a URL absoluta
                if src.startswith('//'):
                    return 'https:' + src
                elif src.startswith('/'):
                    return urljoin("https://www.fourvenues.com", src)
                elif not src.startswith('http'):
                    return urljoin(event_url, src)
                return src
    
    print(f"    [WARNING] No se encontró imagen del CDN de FourVenues")
    return None

def extract_dynamic_ticket_types(soup, html):
    """Extraer tipos de entrada de forma completamente dinámica"""
    
    ticket_types = []
    
    # Método 1: Datos JSON estructurados (Schema.org)
    ticket_types = extract_tickets_from_json_ld(soup, html)
    
    # Método 2: Si no hay JSON, buscar en el HTML
    if not ticket_types:
        ticket_types = extract_tickets_from_html_structure(soup, html)
    
    # Método 3: Fallback con patrones de texto
    if not ticket_types:
        ticket_types = extract_tickets_from_text_patterns(soup, html)
    
    return ticket_types

def extract_tickets_from_json_ld(soup, html):
    """Extraer tickets desde datos JSON-LD estructurados"""
    ticket_types = []
    
    # Buscar scripts con JSON-LD
    json_scripts = soup.find_all('script', type='application/ld+json')
    
    for script in json_scripts:
        try:
            import json
            data = json.loads(script.string)
            
            # Buscar ofertas en los datos estructurados
            if isinstance(data, dict) and 'offers' in data:
                offers = data['offers']
                if not isinstance(offers, list):
                    offers = [offers]
                
                for i, offer in enumerate(offers):
                    if isinstance(offer, dict):
                        name = offer.get('name', f'Entrada {i+1}')
                        price = offer.get('price', 0)
                        availability = offer.get('availability', 'InStock')
                        
                        if price and isinstance(price, (int, float, str)):
                            try:
                                price_num = float(str(price))
                                if price_num > 0:
                                    ticket_types.append({
                                        'id': f'ticket_{i}',
                                        'name': fix_special_characters(name),
                                        'description': generate_ticket_description(name),
                                        'price': int(price_num),
                                        'isAvailable': 'InStock' in availability,
                                        'isSoldOut': 'OutOfStock' in availability,
                                        'isPromotion': 'promoción' in name.lower(),
                                        'isVip': 'vip' in name.lower(),
                                        'restrictions': extract_ticket_restrictions_from_name(name)
                                    })
                            except:
                                continue
        except:
            continue
    
    # También buscar patrones JSON en scripts regulares
    if not ticket_types:
        scripts = soup.find_all('script')
        for script in scripts:
            if not script.string:
                continue
            
            # Buscar patrón de ofertas JSON
            offer_pattern = r'\{"@type":"Offer","priceCurrency":"EUR","price":(\d+),"name":"([^"]+)"[^}]*"availability":"([^"]+)"[^}]*\}'
            matches = re.findall(offer_pattern, script.string)
            
            for i, (price, name, availability) in enumerate(matches):
                ticket_types.append({
                    'id': f'ticket_{i}',
                    'name': fix_special_characters(name),
                    'description': generate_ticket_description(name),
                    'price': int(price),
                    'isAvailable': 'InStock' in availability,
                    'isSoldOut': 'OutOfStock' in availability,
                    'isPromotion': 'promoción' in name.lower(),
                    'isVip': 'vip' in name.lower(),
                    'restrictions': extract_ticket_restrictions_from_name(name)
                })
    
    return ticket_types

def extract_tickets_from_html_structure(soup, html):
    """Extraer tickets desde la estructura HTML"""
    ticket_types = []
    
    # Buscar contenedores de tickets
    ticket_selectors = [
        '.ticket',
        '.entry',
        '.entrada',
        '[class*="ticket"]',
        '[class*="entry"]',
        '[class*="entrada"]'
    ]
    
    for selector in ticket_selectors:
        elements = soup.select(selector)
        for i, element in enumerate(elements):
            try:
                # Extraer nombre
                name_elem = element.find(['h1', 'h2', 'h3', 'h4', '.name', '.title'])
                name = name_elem.get_text().strip() if name_elem else f'Entrada {i+1}'
                
                # Extraer precio
                price_elem = element.find(string=re.compile(r'\d+€'))
                price = 0
                if price_elem:
                    price_match = re.search(r'(\d+)€', price_elem)
                    if price_match:
                        price = int(price_match.group(1))
                
                # Extraer disponibilidad
                text_content = element.get_text().lower()
                is_sold_out = any(word in text_content for word in ['agotad', 'sold out', 'completa'])
                is_available = not is_sold_out
                
                if price > 0:
                    ticket_types.append({
                        'id': f'ticket_{i}',
                        'name': fix_special_characters(name),
                        'description': generate_ticket_description(name),
                        'price': price,
                        'isAvailable': is_available,
                        'isSoldOut': is_sold_out,
                        'isPromotion': 'promoción' in name.lower(),
                        'isVip': 'vip' in name.lower(),
                        'restrictions': extract_ticket_restrictions_from_name(name)
                    })
            except:
                continue
    
    return ticket_types

def extract_tickets_from_text_patterns(soup, html):
    """Extraer tickets usando patrones de texto como último recurso"""
    ticket_types = []
    
    # Obtener todo el texto
    page_text = soup.get_text()
    lines = page_text.split('\n')
    
    # Buscar líneas con precios
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Buscar líneas con precios
        price_match = re.search(r'(\d+)€', line)
        if price_match:
            price = int(price_match.group(1))
            
            # Buscar nombre en líneas cercanas
            name = line
            for j in range(max(0, i-3), min(len(lines), i+4)):
                nearby_line = lines[j].strip()
                if any(word in nearby_line.lower() for word in ['entrada', 'ticket', 'promoción', 'vip']):
                    name = nearby_line
                    break
            
            # Verificar disponibilidad
            context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)]).lower()
            is_sold_out = any(word in context for word in ['agotad', 'sold out', 'completa'])
            
            if 5 <= price <= 500:  # Filtro de precios razonables
                ticket_types.append({
                    'id': f'ticket_{len(ticket_types)}',
                    'name': fix_special_characters(name),
                    'description': generate_ticket_description(name),
                    'price': price,
                    'isAvailable': not is_sold_out,
                    'isSoldOut': is_sold_out,
                    'isPromotion': 'promoción' in name.lower(),
                    'isVip': 'vip' in name.lower(),
                    'restrictions': extract_ticket_restrictions_from_name(name)
                })
    
    # Eliminar duplicados
    unique_tickets = []
    seen_combinations = set()
    for ticket in ticket_types:
        key = (ticket['name'][:20], ticket['price'])
        if key not in seen_combinations:
            seen_combinations.add(key)
            unique_tickets.append(ticket)
    
    return unique_tickets

def generate_dynamic_description(title, venue_name):
    """Generar descripción dinámica basada en el título"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['fest', 'festival']):
        return f"Festival de música electrónica en {venue_name}. Una experiencia única con los mejores DJs."
    elif any(word in title_lower for word in ['opening', 'inauguración']):
        return f"Gran inauguración en {venue_name}. Una noche épica para dar comienzo a la temporada."
    elif any(word in title_lower for word in ['reggaeton', 'reggaetón']):
        return f"Noche de reggaetón en {venue_name}. La mejor música urbana y ambiente de fiesta."
    elif any(word in title_lower for word in ['comercial']):
        return f"Música comercial en {venue_name}. Los éxitos del momento en una noche inolvidable."
    elif any(word in title_lower for word in ['bus', 'transporte']):
        return f"Transporte al evento. Viaja cómodo y seguro con ida y vuelta incluida."
    else:
        return f"Evento exclusivo en {venue_name}. Una noche única con la mejor música y ambiente."

def generate_dynamic_tags(title):
    """Generar tags dinámicamente basados en el título"""
    title_upper = title.upper()
    
    if any(word in title_upper for word in ['BUS', 'TRANSPORTE']):
        return ['Buses']
    else:
        return ['Fiestas']

def fix_special_characters(text):
    """Corregir caracteres especiales mal codificados manteniendo UTF-8 correcto"""
    if not text:
        return text
    
    # Primero limpiar códigos Unicode problemáticos
    text = clean_unicode_codes(text)
    
    # Mapeo de caracteres mal codificados comunes (solo los realmente problemáticos)
    replacements = {
        # Caracteres UTF-8 mal interpretados específicos
        'Ã±': 'ñ',
        'Ã¡': 'á',
        'Ã©': 'é',
        'Ã­': 'í',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã': 'Ñ',
        # Caracteres de reemplazo Unicode problemáticos
        '': '',  # Eliminar caracteres de reemplazo
        '\ufffd': '',  # Eliminar caracteres de reemplazo Unicode
        # Correcciones específicas para palabras mal codificadas
        'España': 'España',
        'españa': 'españa',
        'ESPAÑA': 'ESPAÑA',
        'Murcia, España': 'Murcia, España',
        'año': 'año',
        'AÑO': 'AÑO',
        'niño': 'niño',
        'NIÑO': 'NIÑO',
        'sueño': 'sueño',
        'SUEÑO': 'SUEÑO',
        # Correcciones específicas de venues
        'MACCAO': 'MACCAO',
        'MACCAÑO': 'MACCAO',  # Corregir codificación incorrecta
    }
    
    result = text
    for wrong, correct in replacements.items():
        result = result.replace(wrong, correct)
    
    # NO eliminar emojis ni caracteres especiales válidos
    # Solo limpiar caracteres de control problemáticos
    result = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', result)
    
    # Limpiar espacios múltiples
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def clean_unicode_codes(text):
    """Limpiar códigos Unicode específicos que aparecen en los nombres de entradas"""
    if not text:
        return text
    
    # Mapeo específico de códigos Unicode mal interpretados
    unicode_replacements = {
        # Códigos Unicode con backslash
        '\\u00c1': 'Á', '\\u00e1': 'á',  # A con acento
        '\\u00c9': 'É', '\\u00e9': 'é',  # E con acento
        '\\u00cd': 'Í', '\\u00ed': 'í',  # I con acento
        '\\u00d3': 'Ó', '\\u00f3': 'ó',  # O con acento
        '\\u00da': 'Ú', '\\u00fa': 'ú',  # U con acento
        '\\u00d1': 'Ñ', '\\u00f1': 'ñ',  # Ñ
        # Códigos Unicode sin backslash
        'u00c1': 'Á', 'u00e1': 'á',
        'u00c9': 'É', 'u00e9': 'é',
        'u00cd': 'Í', 'u00ed': 'í',
        'u00d3': 'Ó', 'u00f3': 'ó',
        'u00da': 'Ú', 'u00fa': 'ú',
        'u00d1': 'Ñ', 'u00f1': 'ñ',
        # Emojis específicos - ELIMINAR en lugar de reemplazar
        'ud83cudfd6ufe0f': '',  # Emoji de playa -> eliminar
        'ud83dudd25': '',  # Emoji de fuego -> eliminar
        'ud83cudf86': '',  # Emoji de fuegos artificiales -> eliminar
        'ud83cudf89': '',  # Emoji de fiesta -> eliminar
        'ud83cudfb5': '',  # Emoji de música -> eliminar
        # Palabras específicas
        'u00daLTIMAS': 'ÚLTIMAS',
        'LTIMAS': 'ÚLTIMAS',  # Fallback si se pierde la U
        'u00daLTIMAS ENTRADAS': 'ÚLTIMAS ENTRADAS',
        'PRIMERAS ENTRADASud83dudd25': 'PRIMERAS ENTRADAS',
        'PRIMER TRAMOud83cudfd6ufe0f': 'PRIMER TRAMO',
    }
    
    result = text
    for code, replacement in unicode_replacements.items():
        result = result.replace(code, replacement)
    
    # Limpiar códigos Unicode restantes más agresivamente
    # Patrón para códigos Unicode de 4 dígitos
    result = re.sub(r'\\?u[0-9a-fA-F]{4}', '', result)
    # Patrón para códigos Unicode de emojis (más largos) - más específico
    result = re.sub(r'ud83[a-fA-F0-9]{6,12}', '', result)
    # Patrón para códigos Unicode con prefijo u seguido de números/letras
    result = re.sub(r'u[0-9a-fA-F]{4,12}', '', result)
    # Patrón específico para el emoji de playa problemático
    result = re.sub(r'ud83cudfd6ufe0f', '', result)
    # Patrón específico para el emoji de fuego problemático  
    result = re.sub(r'ud83dudd25', '', result)
    
    # Limpiar espacios múltiples que puedan quedar después de eliminar códigos
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def is_event_in_date_range(event_date_str):
    """Verificar si el evento está en el rango de fechas (próximos 30 días)"""
    try:
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        today = datetime.now()
        max_date = today + timedelta(days=30)  # Extendido a 30 días para incluir eventos de junio
        return today.date() <= event_date.date() <= max_date.date()
    except:
        return True  # Si no podemos parsear la fecha, incluir el evento

def extract_minimum_price(ticket_types):
    """Extraer el precio mínimo de los tipos de entrada disponibles (no agotadas)"""
    if not ticket_types:
        return 0  # Si no hay tipos de entrada, precio 0
    
    # Filtrar solo entradas disponibles (no agotadas) con precio > 0
    available_tickets = [
        ticket for ticket in ticket_types 
        if ticket.get('isAvailable', True) and not ticket.get('isSoldOut', False) and ticket.get('price', 0) > 0
    ]
    
    if available_tickets:
        # Obtener el precio más bajo de las entradas disponibles
        min_price = min(ticket['price'] for ticket in available_tickets)
        print(f"Precio mínimo encontrado (disponible): {min_price}€")
        return min_price
    
    # Si no hay entradas disponibles, buscar el precio más bajo de todas las entradas
    all_prices = [ticket['price'] for ticket in ticket_types if ticket.get('price', 0) > 0]
    if all_prices:
        min_price = min(all_prices)
        print(f"Precio mínimo encontrado (todas las entradas): {min_price}€")
        return min_price
    
    # Fallback: intentar extraer precio del HTML directamente
    print("No se encontraron precios en ticket_types, usando precio por defecto")
    return 0  # Precio 0 si no se encuentra nada

def generate_ticket_description(name):
    """Generar descripción basada en el nombre de la entrada"""
    name_lower = name.lower()
    
    if "1 copa" in name_lower:
        if "sin hora" in name_lower:
            return "1 copa de alcohol estándar sin restricción de horario."
        else:
            return "1 copa de alcohol estándar para consumir antes de las 2:30."
    elif "2 copas" in name_lower:
        if "sin hora" in name_lower:
            return "2 copas de alcohol estándar sin restricción de horario."
        else:
            return "2 copas de alcohol estándar (1 copa para consumir antes de las 2:30 y la otra a la hora que quieras)."
    elif "super reducida" in name_lower:
        return "Entrada con precio especial reducido."
    elif "reducida" in name_lower:
        return "Entrada con precio reducido."
    else:
        return "Entrada al evento."

def extract_ticket_restrictions_from_name(name):
    """Extraer restricciones específicas del nombre de la entrada"""
    restrictions = []
    name_lower = name.lower()
    
    # Buscar características VIP
    if 'sin colas' in name_lower:
        restrictions.append("Acceso sin colas")
    
    if 'sin hora' in name_lower:
        restrictions.append("Sin restricción de horario")
    elif '1 copa' in name_lower and 'sin hora' not in name_lower:
        restrictions.append("Para consumir antes de las 2:30")
    
    return " - ".join(restrictions)

def create_party_object(event_data, index, venue_id):
    """Crear objeto Party para la API"""
    
    # Determinar si el evento está disponible basándose en los tipos de entrada
    ticket_types = event_data.get('ticket_types', [])
    is_available = True
    
    if ticket_types:
        # Si hay tipos de entrada, verificar si al menos uno está disponible
        available_tickets = [ticket for ticket in ticket_types if ticket.get('isAvailable', True)]
        is_available = len(available_tickets) > 0
    
    return {
        "id": str(index + 1),
        "venueId": venue_id,
        "venueName": fix_special_characters(event_data['venue_name']),
        "title": fix_special_characters(event_data['title']),
        "description": fix_special_characters(event_data['description']),
        "date": event_data['date'],
        "startTime": event_data['start_time'],
        "endTime": event_data['end_time'],
        "price": event_data['price'],
        "imageUrl": event_data['image_url'],
        "ticketUrl": event_data['ticket_url'],
        "isAvailable": is_available,
        "capacity": 300,
        "soldTickets": 150,
        "tags": event_data['tags'],
        "venueAddress": fix_special_characters(event_data.get('venue_address', 'Murcia, España')),
        "ticketTypes": ticket_types
    }

def get_venue_image(category):
    """Obtener imagen apropiada para el venue según su categoría"""
    if category.lower() == 'club':
        return "https://images.unsplash.com/photo-1571266028243-d220c9c3b31f?w=800&h=600&fit=crop&crop=center"
    elif category.lower() == 'discoteca':
        return "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center"
    else:
        return "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop&crop=center"

def main():
    """Función principal - Procesar todos los venues configurados"""
    try:
        print("Iniciando scraper dinámico de FourVenues...")
        print(f"Venues configurados: {len(FOURVENUES_VENUES)}")
        
        all_events = []
        all_venues = []
        
        # Procesar cada venue
        for i, venue_config in enumerate(FOURVENUES_VENUES):
            try:
                # Extraer eventos del venue
                venue_events = extract_events_from_venue(venue_config)
                
                # Crear objeto venue
                venue_obj = {
                    "id": str(i + 1),
                    "name": venue_config['venue_info']['name'],
                    "description": f"Eventos de {venue_config['venue_info']['name']} en Murcia",
                    "address": venue_config['venue_info']['address'],
                    "imageUrl": get_venue_image(venue_config['venue_info']['category']),
                    "website": venue_config['url'],
                    "phone": "+34 968 000 000",
                    "isActive": len(venue_events) > 0,
                    "category": {
                        "id": str(i + 1),
                        "name": venue_config['venue_info']['category'],
                        "icon": "musical-notes"
                    }
                }
                all_venues.append(venue_obj)
                
                # Añadir eventos con venueId correcto
                for j, event in enumerate(venue_events):
                    party_obj = create_party_object(event, len(all_events), str(i + 1))
                    all_events.append(party_obj)
                    
            except Exception as e:
                print(f"Error procesando venue {venue_config['name']}: {e}")
                continue
        
        if not all_events:
            print("No se encontraron eventos")
            # Crear respuesta vacía pero válida
            result = {
                "venues": [{
                    "id": "1",
                    "name": "FourVenues Murcia",
                    "description": "Plataforma de eventos de Murcia",
                    "address": "Murcia, España",
                    "imageUrl": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
                    "website": "https://www.fourvenues.com",
                    "phone": "+34 968 000 000",
                    "isActive": True,
                    "category": {
                        "id": "1",
                        "name": "Discoteca",
                        "icon": "musical-notes"
                    }
                }],
                "parties": []
            }
        else:
            # Ordenar TODOS los eventos por fecha - los más cercanos primero
            all_events_sorted = sorted(all_events, key=lambda event: {
                'date_obj': datetime.strptime(event['date'], "%Y-%m-%d"),
                'diff': abs(datetime.strptime(event['date'], "%Y-%m-%d").timestamp() - datetime.now().timestamp())
            }['diff'])
            
            result = {
                "venues": all_venues,
                "parties": all_events_sorted
            }
        
        print(f"\nRESUMEN FINAL:")
        print(f"   Venues procesados: {len(all_venues)}")
        print(f"   Eventos encontrados: {len(all_events)}")
        
        # Verificar si estamos en modo --json-only
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == "--json-only":
            # Usar print original para el JSON (no el redirigido)
            import builtins
            json_output = json.dumps(result, ensure_ascii=False, indent=2)
            
            # Configurar salida UTF-8 para Windows
            if sys.platform.startswith('win'):
                import codecs
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            
            builtins.print(json_output)
        else:
            # Imprimir resultado como JSON con codificación UTF-8
            json_output = json.dumps(result, ensure_ascii=False, indent=2)
            print(json_output)
        
        # Asegurar que el JSON se escriba completamente
        sys.stdout.flush()
        
    except Exception as e:
        print(f"Error en main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    # Si se pasa --json-only como argumento, suprimir prints de debug
    if len(sys.argv) > 1 and sys.argv[1] == "--json-only":
        # Redirigir prints a stderr para que solo el JSON vaya a stdout
        import sys
        original_print = print
        def silent_print(*args, **kwargs):
            kwargs['file'] = sys.stderr
            original_print(*args, **kwargs)
        print = silent_print
        
        try:
            # Ejecutar main y capturar solo el JSON
            main()
        except Exception as e:
            # En caso de error, imprimir a stderr
            original_print(f"Error en scraper: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Comportamiento normal
        main() 