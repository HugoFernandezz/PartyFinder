#!/usr/bin/env python3
"""Test API directa de FourVenues - sin Firecrawl"""

import requests
import json

# Probar API directa de FourVenues
api_url = "https://api.fourvenues.com/v2/web/organizations/luminata-disco/events?lang=es&page=1"

print(f"Probando API: {api_url}")

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
}

r = requests.get(api_url, headers=headers)

print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('content-type')}")

if r.ok and "application/json" in r.headers.get("content-type", ""):
    data = r.json()
    print(f"\n✅ JSON recibido!")
    print(f"Keys: {data.keys() if isinstance(data, dict) else 'Es lista'}")
    if isinstance(data, dict) and "data" in data:
        events = data["data"]
        print(f"Eventos: {len(events)}")
        for e in events[:3]:
            print(f"  - {e.get('name', 'N/A')}")
        
        # Guardar
        with open("data/api_events.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n💾 Guardado en data/api_events.json")
else:
    print(f"\n❌ No es JSON o error")
    print(r.text[:500])
