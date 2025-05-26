import requests
import re

# Obtener HTML
print("Obteniendo HTML de FourVenues...")
response = requests.get('https://www.fourvenues.com/es/hugo-fernandez-gil')
html = response.text

print(f"HTML obtenido: {len(html)} caracteres")

# Buscar todos los identificadores de eventos
print("\nBuscando todos los identificadores de eventos...")

# Patrón para encontrar identificadores de eventos
# Formato: Event('identificador-del-evento', ...)
event_pattern = r"Event\('([^']+)'"

matches = re.findall(event_pattern, html)

print(f"Encontrados {len(matches)} identificadores de eventos:")
for i, match in enumerate(matches, 1):
    print(f"{i}. {match}")

# Buscar también patrones específicos que sabemos que existen
print("\nBuscando patrones específicos...")
specific_patterns = [
    r'mar-menor[^"\']*',
    r'ticket-bus[^"\']*',
    r'grand-opening[^"\']*',
    r'graduacion[^"\']*',
]

for pattern in specific_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"Patrón '{pattern}': {len(matches)} matches")
        for match in set(matches):  # Eliminar duplicados
            print(f"  - {match}")
    else:
        print(f"Patrón '{pattern}': No encontrado")

# Buscar en el contexto de los títulos que sabemos que existen
print("\nBuscando contexto de títulos conocidos...")
titles = ['MAR MENOR FEST', 'TICKET BUS', 'GRAND OPENING']
for title in titles:
    if title in html:
        pos = html.find(title)
        context = html[max(0, pos-200):pos+200]
        print(f"\nTítulo: {title}")
        print(f"Contexto: {context}")
        
        # Buscar identificadores en el contexto
        event_ids = re.findall(r"Event\('([^']+)'", context)
        if event_ids:
            print(f"IDs encontrados en contexto: {event_ids}") 