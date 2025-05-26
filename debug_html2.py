import requests
import re

# Obtener HTML
print("Obteniendo HTML de FourVenues...")
response = requests.get('https://www.fourvenues.com/es/hugo-fernandez-gil')
html = response.text

print(f"HTML obtenido: {len(html)} caracteres")

# Buscar específicamente las fechas que vimos en la página web
print("\nBuscando fechas específicas que vimos en la web...")

# Según la información que vimos, los eventos son:
# - Jue. 05 Jun. - GRADUACIÓN 5 JUNIO
# - Jue. 05 Jun. - TICKET BUS - MAR MENOR FEST  
# - Jue. 05 Jun. - MAR MENOR FEST
# - Vie. 06 Jun. - GRADUACIÓN 6 JUNIO
# - Vie. 06 Jun. - GRADUACIÓN 6 JUNIO / NUESTRA SÑRA L.A
# - Sáb. 07 Jun. - THE GRAND OPENING MACCÄO OPEN AIR 2025
# - Vie. 13 Jun. - GRADUACIÓN 13 JUNIO ALQUERÍAS

# Buscar patrones de fecha más específicos
date_patterns = [
    r'Jue\.\s*05\s*Jun\.',
    r'Vie\.\s*06\s*Jun\.',
    r'Sáb\.\s*07\s*Jun\.',
    r'Vie\.\s*13\s*Jun\.',
    r'05\s*Jun',
    r'06\s*Jun',
    r'07\s*Jun',
    r'13\s*Jun',
]

for pattern in date_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    print(f"Patrón '{pattern}': {len(matches)} matches")
    if matches:
        print(f"  Encontrados: {matches}")

# Buscar eventos específicos
print("\nBuscando eventos específicos...")
events = [
    'GRADUACIÓN 5 JUNIO',
    'GRADUACIÓN 6 JUNIO',
    'GRADUACIÓN 13 JUNIO',
    'MAR MENOR FEST',
    'TICKET BUS',
    'GRAND OPENING'
]

for event in events:
    if event in html:
        print(f"✓ Encontrado: {event}")
        # Buscar contexto más amplio
        pos = html.find(event)
        context = html[max(0, pos-200):pos+300]
        print(f"  Contexto: ...{context}...")
        print()
    else:
        print(f"✗ NO encontrado: {event}")

# Buscar todas las ocurrencias de "Jun" para ver el formato
print("\nTodas las ocurrencias de 'Jun':")
jun_matches = re.finditer(r'.{20}Jun.{20}', html, re.IGNORECASE)
for i, match in enumerate(jun_matches):
    if i < 10:  # Solo mostrar las primeras 10
        print(f"  {match.group()}") 