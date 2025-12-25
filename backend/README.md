# PartyFinder Backend

Backend para scrapear eventos de discotecas y servirlos a la app móvil usando Firebase Firestore.

## 🎯 Discotecas Configuradas

- **Luminata Disco**: https://site.fourvenues.com/es/luminata-disco/events
- **El Club by Odiseo**: https://site.fourvenues.com/es/el-club-by-odiseo/events
- **Dodo Club**: https://site.fourvenues.com/es/dodo-club/events

## 📦 Instalación

### 1. Crear entorno virtual (recomendado)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Firebase

1. Descarga `serviceAccountKey.json` desde Firebase Console
2. Colócalo en el directorio `backend/`
3. Asegúrate de que está en `.gitignore` (no subirlo a Git)

## 🚀 Uso

### Ejecutar scraper

**Solo scraping (sin subir a Firebase):**
```bash
python scraper_firecrawl.py
```

**Scraping + subir a Firebase:**
```bash
python scraper_firecrawl.py --upload
```

**Test de conexión:**
```bash
python scraper_firecrawl.py --test
```

### Ejecución automática

El scraper se ejecuta automáticamente mediante **GitHub Actions** 3 veces al día.

## 🔧 Configuración

### Añadir más venues

Edita `scraper_firecrawl.py` y añade URLs al array `VENUE_URLS`:

```python
VENUE_URLS = [
    "https://site.fourvenues.com/es/luminata-disco/events",
    "https://site.fourvenues.com/es/el-club-by-odiseo/events",
    "https://site.fourvenues.com/es/dodo-club/events",
    "https://site.fourvenues.com/es/NUEVO-VENUE/events"  # Nueva discoteca
]
```

## 📁 Estructura de archivos

```
backend/
├── data/                      # Datos generados (JSON, HTML de debug)
├── scraper_firecrawl.py       # Scraper principal (usando Firecrawl API)
├── push_notifications.py      # Servicio de notificaciones push
├── firebase_config.py         # Configuración de Firebase
├── requirements.txt           # Dependencias Python
└── serviceAccountKey.json     # Credenciales de Firebase (no en Git)
```

## ⚠️ Notas importantes

1. **Firecrawl API**: Necesitas una API key de Firecrawl configurada en la variable de entorno `FIRECRAWL_API_KEY`
2. **Firebase**: El scraper sube los datos directamente a Firestore
3. **Notificaciones**: Después de cada scraping, se envían notificaciones push si hay nuevos eventos
4. **Producción**: El scraper se ejecuta automáticamente 3 veces al día mediante GitHub Actions

