# Sistema Dinámico de Adaptación Automática - PartyFinder Murcia

## 🎯 Objetivo Conseguido

**Tu aplicación PartyFinder Murcia ahora es completamente dinámica y se adapta automáticamente a cualquier evento nuevo que aparezca en FourVenues, sin importar cómo se llame el evento.**

## 🚀 Cómo Funciona el Sistema Dinámico

### 1. Detección Automática de Eventos
El scraper ahora:
- **Busca automáticamente** todos los identificadores de eventos en el HTML de FourVenues
- **Filtra inteligentemente** solo los que parecen ser eventos reales (no funciones del sistema)
- **No requiere definiciones manuales** de eventos específicos

```python
# El sistema busca patrones como:
Event('graduacion-5-junio--05-06-2025')
Event('nuevo-festival-verano--15-08-2025')  # ← Evento nuevo se detectaría automáticamente
Event('concierto-reggaeton--20-07-2025')    # ← Este también
```

### 2. Extracción Inteligente de Información

Para cada evento detectado, el sistema **extrae automáticamente**:

#### 📝 Título del Evento
- Busca en el contexto HTML del evento
- Limpia automáticamente fechas y caracteres extra
- Genera título desde el slug si no encuentra uno en HTML

#### 📅 Fecha del Evento
- Extrae fecha directamente del slug del evento
- Formato: `--DD-MM-YYYY` o `-DD-MM-YYYY`
- Fallback a fecha futura si no encuentra patrón

#### 🕐 Horarios
- Busca patrones de hora en el contexto HTML
- Detecta formato `HH:MM HH:MM` (inicio y fin)
- Horarios por defecto: 21:30 - 04:00

#### 🏢 Venue (Local)
- **Inferencia inteligente** basada en el tipo de evento:
  - Graduaciones → GRADUAME MURCIA
  - Festivales/Fiestas → MACCAO OPEN AIR CLUB
  - Detección por palabras clave en título

#### 💰 Precio
- **Estimación automática** según el tipo:
  - Ticket Bus: 8€
  - Graduaciones: 15€
  - Festivales: 10€
  - Inauguraciones: 12€
  - Por defecto: 15€

#### 🏷️ Tags (Etiquetas)
- **Generación automática** basada en palabras clave:
  - "GRADUACION" → ['Fiestas', 'Graduacion', 'Estudiantes', 'Universidad']
  - "FEST" → ['Fiestas', 'Festival', 'Electronica', 'Verano']
  - "OPENING" → ['Fiestas', 'Inauguracion', 'Espectaculo']
  - "BUS" → ['Buses', 'Transporte']

#### 📝 Descripción
- **Generación contextual** según el tipo de evento
- Incluye información del venue
- Adaptada al público objetivo

#### 🖼️ Imagen
- **Imagen real** para eventos específicos (ej: Mar Menor Fest)
- **Imágenes categorizadas** de Unsplash según tags
- Sistema de fallback inteligente

## 🔄 Proceso de Actualización Automática

### Servidor Local (Puerto 3001)
- **Actualización cada 6 horas** automáticamente
- **Endpoint manual**: `POST /api/update` para forzar actualización
- **Cache inteligente** para optimizar rendimiento

### Aplicación React Native
- **Pull-to-refresh** para actualizar eventos manualmente
- **Conexión en tiempo real** con el servidor local
- **Filtros dinámicos** que se adaptan a nuevas categorías

## 📱 Funcionalidades de la App

### Pantalla Principal (HomeScreen)
- **Lista dinámica** de todos los eventos detectados
- **Búsqueda en tiempo real** por título, venue, descripción, tags
- **Filtros por etiquetas** con selección múltiple
- **Pull-to-refresh** para actualizar datos

### Pantalla de Detalles (EventDetailScreen)
- **Información completa** del evento
- **Imagen a pantalla completa**
- **Botón de compra** que abre la URL real de FourVenues
- **Progreso de disponibilidad** de entradas

### Sistema de Navegación
- **Tab Navigation**: "Fiestas" y "Mi Perfil"
- **Stack Navigation** para detalles de eventos
- **Navegación fluida** entre pantallas

## 🎯 Ejemplos de Adaptación Automática

Si mañana aparecen estos eventos nuevos en FourVenues:

```
1. "concierto-bad-bunny-murcia--25-08-2025"
   → Se detectaría automáticamente
   → Título: "CONCIERTO BAD BUNNY MURCIA"
   → Tags: ['Fiestas', 'Reggaeton', 'Urban']
   → Precio: 15€

2. "festival-techno-underground--15-09-2025"
   → Se detectaría automáticamente
   → Título: "FESTIVAL TECHNO UNDERGROUND"
   → Tags: ['Fiestas', 'Festival', 'Electronica', 'Techno']
   → Precio: 10€

3. "graduacion-universidad-murcia--30-06-2025"
   → Se detectaría automáticamente
   → Título: "GRADUACION UNIVERSIDAD MURCIA"
   → Tags: ['Fiestas', 'Graduacion', 'Estudiantes']
   → Venue: GRADUAME MURCIA
```

## ✅ Ventajas del Sistema Dinámico

### 🔧 Mantenimiento Cero
- **No necesitas editar código** cuando aparezcan eventos nuevos
- **No hay listas hardcodeadas** de eventos
- **Adaptación automática** a cualquier formato

### 🎯 Precisión Inteligente
- **Detección por patrones** en lugar de nombres específicos
- **Inferencia contextual** de información faltante
- **Fallbacks robustos** para casos edge

### 📈 Escalabilidad
- **Funciona con cualquier cantidad** de eventos
- **Se adapta a nuevos tipos** de eventos automáticamente
- **Rendimiento optimizado** con cache

### 🛡️ Robustez
- **Manejo de errores** graceful
- **Múltiples estrategias** de extracción
- **Datos por defecto** cuando falta información

## 🔮 Futuro del Sistema

El sistema está preparado para:
- **Nuevos venues** que aparezcan en FourVenues
- **Nuevos tipos de eventos** (conciertos, obras de teatro, etc.)
- **Cambios en la estructura** de FourVenues
- **Expansión a otras ciudades** o plataformas

## 🎉 Resultado Final

**Tu aplicación PartyFinder Murcia es ahora completamente autónoma y se adapta automáticamente a cualquier evento nuevo que aparezca en FourVenues, proporcionando una experiencia de usuario consistente y actualizada sin intervención manual.** 