#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import urllib3
from bs4 import BeautifulSoup

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_html_like_scraper(url):
    """Usar la misma función que el scraper"""
    import time
    time.sleep(3)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    response = requests.get(url, headers=headers, timeout=30, verify=False)
    return response.text

def analyze_html():
    """Analizar el HTML para encontrar patrones de eventos"""
    
    url = 'https://www.fourvenues.com/es/luminata-disco'
    print(f"Analizando: {url}")
    
    try:
        # Método 1: Como el debug original
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response1 = requests.get(url, headers=headers1, timeout=10)
        html1 = response1.text
        print(f"Método 1 (debug original): {len(html1)} caracteres")
        
        # Método 2: Como el scraper
        html2 = fetch_html_like_scraper(url)
        print(f"Método 2 (como scraper): {len(html2)} caracteres")
        
        # Comparar contenido
        print(f"\n=== COMPARACIÓN ===")
        print(f"Diferencia en tamaño: {len(html1) - len(html2)} caracteres")
        
        # Buscar onClickEvent en ambos
        pattern = r"onClickEvent\(\s*'([^']+)'\s*,\s*'([A-Z0-9]{4})'\s*,\s*'([^']+)'\s*,\s*'[^']*'\s*,\s*'(\d+)'\s*\)"
        
        matches1 = re.findall(pattern, html1)
        matches2 = re.findall(pattern, html2)
        
        print(f"onClickEvent en método 1: {len(matches1)}")
        for match in matches1:
            print(f"  - {match}")
        
        print(f"onClickEvent en método 2: {len(matches2)}")
        for match in matches2:
            print(f"  - {match}")
        
        # Buscar diferencias en el contenido
        if len(html1) > len(html2):
            print(f"\n=== CONTENIDO ADICIONAL EN MÉTODO 1 ===")
            # Buscar scripts que podrían contener los eventos
            soup1 = BeautifulSoup(html1, 'html.parser')
            soup2 = BeautifulSoup(html2, 'html.parser')
            
            scripts1 = soup1.find_all('script')
            scripts2 = soup2.find_all('script')
            
            print(f"Scripts en método 1: {len(scripts1)}")
            print(f"Scripts en método 2: {len(scripts2)}")
            
            # Buscar scripts que contengan onClickEvent
            for i, script in enumerate(scripts1):
                if script.string and 'onClickEvent' in script.string:
                    print(f"Script {i+1} contiene onClickEvent:")
                    print(script.string[:500] + "...")
                    break
        
        # Guardar ambos HTMLs para comparación manual
        with open('html_method1.txt', 'w', encoding='utf-8') as f:
            f.write(html1[:10000])
        
        with open('html_method2.txt', 'w', encoding='utf-8') as f:
            f.write(html2[:10000])
        
        print(f"\nHTMLs guardados para comparación manual")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_html() 