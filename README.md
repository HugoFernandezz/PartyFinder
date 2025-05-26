# PartyFinder Murcia 🎉

Una aplicación móvil para descubrir y comprar entradas de eventos nocturnos en Murcia, España.

## 🚀 Características

- **Lista de Fiestas**: Visualiza todos los eventos disponibles para hoy
- **Información de Locales**: Explora los mejores lugares de ocio nocturno
- **Búsqueda Inteligente**: Encuentra eventos por nombre, local o categoría
- **Compra de Entradas**: Enlaces directos para comprar entradas
- **Datos en Tiempo Real**: Información actualizada automáticamente desde FourVenues

## 🛠️ Tecnologías

- **Frontend**: React Native con Expo
- **Lenguaje**: TypeScript
- **Navegación**: React Navigation (Bottom Tabs)
- **Iconos**: Expo Vector Icons
- **Backend**: Servidor Node.js local
- **Scraping**: Python con BeautifulSoup4

## 📱 Estructura del Proyecto

```
src/
├── components/
│   ├── Navigation.tsx      # Navegación por pestañas
│   ├── PartyCard.tsx      # Tarjeta de evento
│   └── ConnectionStatus.tsx # Estado del servidor
├── screens/
│   ├── HomeScreen.tsx     # Lista de fiestas
│   └── VenuesScreen.tsx   # Lista de locales
├── services/
│   └── api.ts            # Cliente API
└── types/
    └── index.ts          # Definiciones de tipos
```

## 🔧 Instalación y Configuración

### Prerrequisitos

- Node.js (v16 o superior)
- Python 3.7+
- Expo CLI
- npm o yarn

## 🚀 Instalación y Despliegue Rápido

### Opción 1: Despliegue Automático (Recomendado)

```bash
# Ejecuta el script de despliegue automático
deploy.bat
```

Este script:
1. ✅ Limpia toda la caché automáticamente
2. ✅ Verifica y inicia el servidor si es necesario
3. ✅ Inicia la aplicación con Expo
4. ✅ Maneja errores automáticamente

### Opción 2: Instalación Manual

#### 1. Limpiar Caché (Importante)

```bash
# Limpiar toda la caché del proyecto
clear-cache.bat

# O manualmente:
npm run clear-cache
```

#### 2. Instalar Dependencias

```bash
# Instalar dependencias de la app
npm install

# Instalar dependencias de Python
pip install beautifulsoup4 requests

# Instalar dependencias del servidor
npm install express cors
```

#### 3. Iniciar Aplicación

```bash
# Opción A: Iniciar todo junto
npm run dev

# Opción B: Iniciar por separado
# Terminal 1:
npm run server

# Terminal 2:
npm start
```

### Scripts Disponibles

#### Desarrollo
- `npm start` - Inicia la app con Expo
- `npm run start:fresh` - Inicia con caché limpia
- `npm run dev` - Inicia servidor + app simultáneamente
- `npm run server` - Solo el servidor backend

#### Caché y Limpieza
- `npm run clear-cache` - Limpia caché de Expo
- `npm run reset` - Reset completo con caché limpia
- `clear-cache.bat` - Limpia toda la caché del sistema (Windows)

## 🛠️ Solución de Problemas de Caché

### Problema: La app no refleja cambios

**Solución 1: Limpieza Automática**
```bash
clear-cache.bat
```

**Solución 2: Limpieza Manual**
```bash
# Limpiar caché de npm
npm cache clean --force

# Limpiar caché de Expo
expo start --clear

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

### Problema: Error de conexión al servidor

**Verificar servidor:**
```bash
# Verificar si el servidor está corriendo
curl http://localhost:3001/api/health

# Si no responde, iniciar servidor
npm run server
```

### Problema: Datos no se actualizan

**Forzar actualización:**
```bash
# Limpiar caché del servidor
curl -X POST http://localhost:3001/api/clear-cache

# Forzar actualización de datos
curl -X POST http://localhost:3001/api/update
```

## 🌐 API del Servidor Local

El servidor local proporciona los siguientes endpoints:

### Datos de Eventos
- `GET /api/status` - Estado del servidor y caché
- `GET /api/parties/today` - Fiestas de hoy
- `GET /api/venues/active` - Locales activos
- `GET /api/data/complete` - Datos completos
- `GET /api/parties/search?q=term` - Buscar fiestas

### Gestión y Caché
- `POST /api/update` - Forzar actualización de datos
- `POST /api/clear-cache` - Limpiar caché del servidor
- `GET /api/health` - Salud del sistema
- `GET /api/test-scraper` - Probar scraper directamente

## 🔄 Sistema de Scraping

### Fuente de Datos
- **FourVenues**: https://www.fourvenues.com/es/hugo-fernandez-gil

### Proceso de Extracción
1. El script Python (`fourvenues_scraper.py`) extrae datos de FourVenues
2. Los datos se procesan y estructuran en formato JSON
3. El servidor Node.js sirve los datos a través de la API
4. La app móvil consume los datos y los muestra al usuario

### Datos Extraídos
- **Eventos**: Título, descripción, fecha, horarios, precios, imágenes
- **Locales**: Nombre, dirección, categoría, estado
- **Entradas**: URLs de compra, disponibilidad

## 📊 Tipos de Datos

### Party (Fiesta)
```typescript
interface Party {
  id: string;
  venueId: string;
  venueName: string;
  title: string;
  description: string;
  date: string;
  startTime: string;
  endTime: string;
  price: number;
  imageUrl: string;
  ticketUrl: string;
  isAvailable: boolean;
  capacity: number;
  soldTickets: number;
  tags: string[];
}
```

### Venue (Local)
```typescript
interface Venue {
  id: string;
  name: string;
  description: string;
  address: string;
  imageUrl: string;
  website: string;
  phone: string;
  isActive: boolean;
  category: VenueCategory;
}
```

## 🎨 Características de la UI

- **Diseño Moderno**: Interfaz limpia y atractiva
- **Tarjetas de Eventos**: Información completa con imágenes
- **Estado de Conexión**: Indicador visual del servidor
- **Pull-to-Refresh**: Actualización manual de datos
- **Búsqueda en Tiempo Real**: Filtrado instantáneo
- **Navegación Intuitiva**: Pestañas inferiores

## 🔧 Configuración del Servidor

### Puerto
El servidor funciona en `http://localhost:3001`

### Cache
- Los datos se actualizan automáticamente cada 6 horas
- Cache persistente en `cached_data.json`
- Actualización manual disponible vía API

### Manejo de Errores
- Fallbacks automáticos en caso de error
- Logs detallados para debugging
- Recuperación automática de conexión

## 📱 Uso de la Aplicación

### Pantalla Principal (Fiestas)
- Lista de eventos disponibles para hoy
- Búsqueda por nombre, local o tags
- Información de precios y horarios
- Botones de compra de entradas

### Pantalla de Locales
- Lista de todos los locales activos
- Información de contacto
- Categorías de locales
- Enlaces a sitios web

## 🚀 Desarrollo

### Modo Desarrollo
La aplicación se conecta automáticamente al servidor local en `localhost:3001`.

### Estructura de Archivos del Servidor
```
├── server.js              # Servidor Express
├── fourvenues_scraper.py  # Script de scraping
├── cached_data.json       # Cache de datos
├── start-server.bat       # Script de inicio (Windows)
└── start-server.sh        # Script de inicio (Linux/Mac)
```

## 🔍 Debugging

### Verificar Estado del Servidor
```bash
curl http://localhost:3001/api/status
```

### Forzar Actualización
```bash
curl -X POST http://localhost:3001/api/update
```

### Ver Logs del Servidor
Los logs se muestran en la consola donde se ejecuta `node server.js`

## 📝 Próximas Características

- [ ] Notificaciones push para nuevos eventos
- [ ] Favoritos y lista de deseos
- [ ] Integración con calendario
- [ ] Compartir eventos en redes sociales
- [ ] Sistema de reseñas y valoraciones
- [ ] Mapa de locales
- [ ] Filtros avanzados por precio, fecha, categoría

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

Para preguntas o sugerencias, puedes contactar al equipo de desarrollo.

---

**¡Disfruta descubriendo la mejor vida nocturna de Murcia! 🌙🎵** 