#!/usr/bin/env python3
"""Analizar HTML de Firecrawl para entender estructura"""

from bs4 import BeautifulSoup

html = open('data/firecrawl_actions.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

# Buscar enlaces con aria-label
links = soup.find_all('a', attrs={'aria-label': True})
print(f"Links con aria-label: {len(links)}")

for i, link in enumerate(links[:8]):
    label = link.get('aria-label', '')
    href = link.get('href', '')
    if 'evento' in label.lower() or 'events' in href.lower():
        print(f"\n[{i}] {label[:100]}...")
        print(f"    href: {href}")

# También buscar elementos con href que contenga events
event_links = soup.find_all('a', href=lambda x: x and '/events/' in x)
print(f"\nLinks a /events/: {len(event_links)}")

for i, link in enumerate(event_links[:5]):
    print(f"  - {link.get('href', '')}")
