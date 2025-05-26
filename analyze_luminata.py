import requests
from bs4 import BeautifulSoup
import re
import json

def analyze_luminata():
    url = 'https://www.fourvenues.com/es/luminata-disco'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        print(f'Status: {response.status_code}')
        print(f'Content length: {len(response.text)}')
        
        # Buscar patrones de eventos
        event_patterns = re.findall(r'Event\(\'([^\']+)\'', response.text)
        print(f'Eventos encontrados: {len(event_patterns)}')
        for i, pattern in enumerate(event_patterns[:10]):
            print(f'  {i+1}. {pattern}')
            
        # Buscar información del venue
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title')
        if title:
            print(f'Título de la página: {title.get_text().strip()}')
            
        # Buscar información específica de eventos en el HTML
        print('\n--- Analizando estructura HTML ---')
        
        # Buscar elementos con fechas
        date_elements = soup.find_all(text=re.compile(r'\d{1,2}\s+(May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)'))
        print(f'Elementos con fechas encontrados: {len(date_elements)}')
        for elem in date_elements[:5]:
            print(f'  - {elem.strip()}')
            
        # Buscar elementos con horarios
        time_elements = soup.find_all(text=re.compile(r'\d{2}:\d{2}'))
        print(f'Elementos con horarios encontrados: {len(time_elements)}')
        for elem in time_elements[:5]:
            print(f'  - {elem.strip()}')
            
        # Buscar títulos de eventos
        event_titles = soup.find_all(['h1', 'h2', 'h3'], text=re.compile(r'(REGGAETON|COMERCIAL|PLAY)'))
        print(f'Títulos de eventos encontrados: {len(event_titles)}')
        for title in event_titles:
            print(f'  - {title.get_text().strip()}')
            
        # Buscar información del venue
        venue_info = soup.find('h1')
        if venue_info:
            print(f'Nombre del venue: {venue_info.get_text().strip()}')
            
        # Guardar HTML para análisis posterior
        with open('luminata_html.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print('HTML guardado en luminata_html.txt')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    analyze_luminata() 