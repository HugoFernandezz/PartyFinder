# API Generador de Imágenes Instagram

API web para generar imágenes personalizadas estilo Instagram Stories de 1080x1920 píxeles.

**📍 Ubicación del proyecto:** `C:\Users\hugaz\Documents\Proyectos Cursor\WEB-Images_Instagram`

## 🚀 Características

- Genera imágenes PNG de alta calidad (1080x1920)
- Personalización completa de textos
- Soporte para imágenes de perfil personalizadas
- API REST simple y fácil de usar
- Interfaz web incluida para pruebas

## 📋 Requisitos

- Node.js 14 o superior
- npm o yarn

## 🛠️ Instalación

1. El proyecto ya está instalado en: `C:\Users\hugaz\Documents\Proyectos Cursor\WEB-Images_Instagram`
2. Las dependencias ya están instaladas y listas
3. El servidor está configurado y funcionando

## 🏃‍♂️ Ejecutar el proyecto

### Modo producción:
```bash
npm start
```

### Modo desarrollo (con auto-reload):
```bash
npm run dev
```

### Inicio rápido con script:
```bash
# Doble clic en start.bat
```

El servidor estará disponible en `http://localhost:3000`

## 📖 Uso de la API

### Endpoints disponibles

#### POST /api/generate-image
Genera una imagen con todos los parámetros personalizables.

**Parámetros:**
- `userName` (string, requerido): Nombre del usuario
- `user` (string, requerido): Handle del usuario (ej: @usuario)
- `message` (string, requerido): Mensaje a mostrar
- `profileImage` (file, opcional): Imagen de perfil

**Ejemplo con cURL:**
```bash
curl -X POST http://localhost:3000/api/generate-image \
  -F "userName=UDIA" \
  -F "user=@udia.es" \
  -F "message=Aquí va tu texto de ejemplo" \
  -F "profileImage=@/ruta/a/imagen.jpg" \
  --output imagen-generada.png
```

#### GET /api/generate-image
Versión simplificada sin imagen de perfil.

**Ejemplo:**
```
http://localhost:3000/api/generate-image?userName=UDIA&user=@udia.es&message=Tu%20mensaje%20aquí
```

## 🎨 Interfaz Web

Accede a `http://localhost:3000` para usar la interfaz web interactiva que incluye:
- Formulario para generar imágenes
- Vista previa en tiempo real
- Descarga directa de imágenes
- Documentación completa

## 🔧 Configuración

Puedes cambiar el puerto del servidor creando un archivo `.env`:

```env
PORT=3001
```

## 📝 Notas

- Las imágenes se generan en memoria, no se guardan en el servidor
- El límite de tamaño para imágenes de perfil es de 5MB
- Los formatos de imagen soportados son: JPG, PNG, GIF, WebP

## ✅ Estado del Proyecto

**🎉 PROYECTO MOVIDO Y FUNCIONAL 🎉**

- ✅ Ubicación actualizada: `WEB-Images_Instagram`
- ✅ Dependencias instaladas correctamente
- ✅ Servidor funcionando en puerto 3000
- ✅ API generando imágenes correctamente
- ✅ Imagen de verificación creada: `verificacion.png`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📄 Licencia

MIT 