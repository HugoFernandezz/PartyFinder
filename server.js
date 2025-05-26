const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const PORT = 3001;

// Habilitar CORS para todas las rutas
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Cache-Control'],
    credentials: false
}));

// Middleware para evitar cache del navegador
app.use((req, res, next) => {
    res.set({
        'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Surrogate-Control': 'no-store'
    });
    next();
});

// Middleware para parsear JSON
app.use(express.json());

// Variable para almacenar datos en memoria
let cachedData = null;
let lastUpdateTime = null;

// Función para ejecutar el scraper y obtener datos frescos
function runScraperAndGetData() {
    return new Promise((resolve, reject) => {
        console.log('🔄 Ejecutando scraper para obtener datos frescos...');
        
        // Configurar opciones para manejar mejor la codificación
        const execOptions = {
            timeout: 120000, // Aumentar timeout a 2 minutos
            encoding: 'utf8',
            maxBuffer: 1024 * 1024 * 10, // 10MB buffer para salida grande
            env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
        };
        
        exec('python fourvenues_scraper.py --json-only', execOptions, (error, stdout, stderr) => {
            if (error) {
                console.error('❌ Error ejecutando scraper:', error.message);
                if (stderr) console.error('❌ Stderr:', stderr);
                reject(error);
                return;
            }
            
            if (stderr) {
                console.log('⚠️ Scraper warnings:', stderr);
            }
            
            try {
                // Limpiar la salida antes de parsear
                let cleanOutput = stdout.trim();
                
                if (!cleanOutput) {
                    throw new Error('Scraper devolvió salida vacía');
                }
                
                console.log(`📊 Salida del scraper: ${cleanOutput.length} caracteres`);
                
                // Buscar el JSON válido en la salida - buscar desde el final hacia atrás
                const lastBraceIndex = cleanOutput.lastIndexOf('}');
                if (lastBraceIndex === -1) {
                    throw new Error('No se encontró JSON válido en la salida del scraper');
                }
                
                // Buscar el primer { antes del último }
                let jsonStart = -1;
                let braceCount = 0;
                for (let i = lastBraceIndex; i >= 0; i--) {
                    if (cleanOutput[i] === '}') {
                        braceCount++;
                    } else if (cleanOutput[i] === '{') {
                        braceCount--;
                        if (braceCount === 0) {
                            jsonStart = i;
                            break;
                        }
                    }
                }
                
                if (jsonStart === -1) {
                    throw new Error('No se encontró JSON válido completo en la salida del scraper');
                }
                
                const jsonString = cleanOutput.substring(jsonStart, lastBraceIndex + 1);
                console.log(`📊 JSON extraído: ${jsonString.length} caracteres`);
                
                const jsonData = JSON.parse(jsonString);
                
                if (jsonData.parties && jsonData.parties.length > 0) {
                    console.log(`✅ Scraper completado: ${jsonData.parties.length} eventos, ${jsonData.venues.length} venues`);
                    
                    // Guardar datos frescos en cache
                    fs.writeFileSync(path.join(__dirname, 'cached_data.json'), JSON.stringify(jsonData, null, 2));
                    console.log('💾 Datos frescos guardados en cached_data.json');
                    
                    resolve(jsonData);
                } else {
                    throw new Error('No se encontraron eventos en los datos del scraper');
                }
            } catch (parseError) {
                console.error('❌ Error parseando datos del scraper:', parseError.message);
                console.error('❌ Primeros 500 caracteres de salida:', stdout.substring(0, 500));
                console.error('❌ Últimos 500 caracteres de salida:', stdout.substring(Math.max(0, stdout.length - 500)));
                reject(parseError);
            }
        });
    });
}

// Función para obtener datos (con cache inteligente)
async function getData() {
    // Si tenemos datos en memoria y son recientes (menos de 30 minutos), usarlos
    const now = Date.now();
    const cacheValidTime = 30 * 60 * 1000; // 30 minutos
    
    if (cachedData && lastUpdateTime && (now - lastUpdateTime) < cacheValidTime) {
        console.log('📊 Usando datos en memoria (cache válido)');
        return cachedData;
    }
    
    // Primero intentar cargar datos cacheados válidos
    const cachedDataPath = path.join(__dirname, 'cached_data.json');
    let hasCachedData = false;
    let cachedJsonData = null;
    
    if (fs.existsSync(cachedDataPath)) {
        try {
            const data = fs.readFileSync(cachedDataPath, 'utf8');
            cachedJsonData = JSON.parse(data);
            
            if (cachedJsonData.parties && cachedJsonData.parties.length > 0) {
                hasCachedData = true;
                console.log(`📊 Datos cacheados disponibles: ${cachedJsonData.parties.length} eventos`);
            }
        } catch (error) {
            console.log('❌ Error leyendo cached_data.json:', error.message);
        }
    }
    
    try {
        // Intentar obtener datos frescos del scraper
        const freshData = await runScraperAndGetData();
        cachedData = freshData;
        lastUpdateTime = now;
        return freshData;
    } catch (scraperError) {
        console.log('⚠️ Scraper falló, usando datos cacheados como fallback...');
        
        // Si tenemos datos cacheados válidos, usarlos
        if (hasCachedData && cachedJsonData) {
            console.log('📊 Usando datos de cached_data.json (datos válidos encontrados)');
            cachedData = cachedJsonData;
            lastUpdateTime = now;
            return cachedJsonData;
        }
        
        // Último fallback: datos de ejemplo
        console.log('📊 Usando datos de ejemplo (todos los métodos fallaron)');
        const exampleData = {
            venues: [
                {
                    id: "1",
                    name: "LUMINATA DISCO",
                    description: "Discoteca en Murcia",
                    address: "Murcia, España",
                    imageUrl: "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
                    website: "https://www.fourvenues.com",
                    phone: "+34 968 000 000",
                    isActive: true,
                    category: {
                        id: "1",
                        name: "Discoteca",
                        icon: "musical-notes"
                    }
                }
            ],
            parties: [
                {
                    id: "1",
                    venueId: "1",
                    venueName: "LUMINATA DISCO",
                    title: "Evento de Ejemplo",
                    description: "Evento de ejemplo mientras se cargan los datos reales",
                    date: "2025-05-30",
                    startTime: "23:30",
                    endTime: "07:00",
                    price: 15,
                    imageUrl: "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center",
                    ticketUrl: "https://www.fourvenues.com",
                    isAvailable: true,
                    capacity: 300,
                    soldTickets: 150,
                    tags: ["Fiestas"],
                    venueAddress: "Murcia, España",
                    ticketTypes: [
                        {
                            id: "ticket_1",
                            name: "ENTRADA GENERAL",
                            description: "Entrada al evento",
                            price: 15,
                            isAvailable: true,
                            isSoldOut: false,
                            isPromotion: false,
                            isVip: false,
                            restrictions: ""
                        }
                    ]
                }
            ]
        };
        
        cachedData = exampleData;
        return exampleData;
    }
}

// Endpoint para datos completos (usado por la app)
app.get('/api/data/complete', async (req, res) => {
    try {
        const data = await getData();
        console.log(`✅ Sirviendo datos completos: ${data.parties?.length || 0} eventos, ${data.venues?.length || 0} venues`);
        res.json({
            success: true,
            data: data
        });
    } catch (error) {
        console.error('❌ Error sirviendo datos completos:', error);
        res.status(500).json({ 
            success: false,
            error: 'Error interno del servidor' 
        });
    }
});

// Endpoint para fiestas de hoy
app.get('/api/parties/today', async (req, res) => {
    try {
        const data = await getData();
        console.log(`✅ Sirviendo fiestas de hoy: ${data.parties?.length || 0} eventos`);
        res.json({
            success: true,
            data: data.parties || []
        });
    } catch (error) {
        console.error('❌ Error sirviendo fiestas:', error);
        res.status(500).json({ 
            success: false,
            error: 'Error interno del servidor' 
        });
    }
});

// Endpoint para venues activos
app.get('/api/venues/active', async (req, res) => {
    try {
        const data = await getData();
        console.log(`✅ Sirviendo venues activos: ${data.venues?.length || 0} venues`);
        res.json({
            success: true,
            data: data.venues || []
        });
    } catch (error) {
        console.error('❌ Error sirviendo venues:', error);
        res.status(500).json({ 
            success: false,
            error: 'Error interno del servidor' 
        });
    }
});

// Endpoint para buscar fiestas
app.get('/api/parties/search', async (req, res) => {
    try {
        const { q } = req.query;
        const data = await getData();
        let parties = data.parties || [];
        
        if (q) {
            const searchTerm = q.toLowerCase();
            parties = parties.filter(party => 
                party.title.toLowerCase().includes(searchTerm) ||
                party.description.toLowerCase().includes(searchTerm) ||
                party.tags.some(tag => tag.toLowerCase().includes(searchTerm))
            );
        }
        
        console.log(`✅ Búsqueda "${q}": ${parties.length} resultados`);
        res.json({
            success: true,
            data: parties
        });
    } catch (error) {
        console.error('❌ Error en búsqueda:', error);
        res.status(500).json({ 
            success: false,
            error: 'Error interno del servidor' 
        });
    }
});

// Endpoint para forzar actualización
app.post('/api/update', async (req, res) => {
    try {
        console.log('🔄 Actualización forzada solicitada');
        
        // Forzar actualización limpiando el cache
        cachedData = null;
        lastUpdateTime = null;
        
        const data = await getData();
        res.json({
            success: true,
            message: 'Datos actualizados exitosamente',
            data: data
        });
    } catch (error) {
        console.error('❌ Error en actualización:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Endpoint para limpiar cache
app.post('/api/clear-cache', (req, res) => {
    try {
        console.log('🗑️ Limpiando cache del servidor...');
        
        // Limpiar cache en memoria
        cachedData = null;
        lastUpdateTime = null;
        
        // Eliminar archivos de cache
        const fs = require('fs');
        const path = require('path');
        
        const cacheFiles = ['cached_data.json', 'fresh_data.json', 'backup_data.json'];
        let deletedFiles = [];
        
        cacheFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            if (fs.existsSync(filePath)) {
                fs.unlinkSync(filePath);
                deletedFiles.push(file);
            }
        });
        
        console.log(`✅ Cache limpiada. Archivos eliminados: ${deletedFiles.join(', ')}`);
        
        res.json({
            success: true,
            message: 'Cache limpiada exitosamente',
            deletedFiles: deletedFiles
        });
    } catch (error) {
        console.error('❌ Error limpiando cache:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Endpoint de estado
app.get('/api/status', async (req, res) => {
    try {
        const data = await getData();
        res.json({
            success: true,
            data: {
                status: 'running',
                lastUpdate: lastUpdateTime ? new Date(lastUpdateTime).toISOString() : new Date().toISOString(),
                hasData: !!(data.parties && data.venues),
                eventsCount: data.parties?.length || 0,
                venuesCount: data.venues?.length || 0,
                needsUpdate: false,
                cacheAge: lastUpdateTime ? Math.floor((Date.now() - lastUpdateTime) / 1000 / 60) : 0 // minutos
            }
        });
    } catch (error) {
        console.error('❌ Error en estado:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Ruta para servir los datos de eventos (legacy)
app.get('/api/events', async (req, res) => {
    try {
        const data = await getData();
        console.log(`✅ Sirviendo datos legacy: ${data.parties?.length || 0} eventos`);
        res.json(data);
    } catch (error) {
        console.error('❌ Error sirviendo datos legacy:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Ruta de salud
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Endpoint para probar el scraper directamente
app.get('/api/test-scraper', async (req, res) => {
    try {
        console.log('🧪 Probando scraper directamente...');
        const freshData = await runScraperAndGetData();
        res.json({
            success: true,
            message: 'Scraper funcionando correctamente',
            data: freshData
        });
    } catch (error) {
        console.error('❌ Error en test del scraper:', error);
        res.status(500).json({
            success: false,
            error: error.message,
            details: 'El scraper no está funcionando correctamente'
        });
    }
});

// Función para inicializar datos al arrancar el servidor
async function initializeData() {
    console.log('🔄 Inicializando datos al arrancar el servidor...');
    try {
        await getData(); // Esto ejecutará el scraper y cargará datos frescos
        console.log('✅ Datos inicializados correctamente');
    } catch (error) {
        console.error('⚠️ Error inicializando datos:', error.message);
        console.log('📊 El servidor funcionará con datos de fallback');
    }
}

// Iniciar servidor
app.listen(PORT, '0.0.0.0', async () => {
    console.log(`🚀 Servidor API iniciado en http://localhost:${PORT}`);
    console.log(`📡 Endpoint de eventos: http://localhost:${PORT}/api/events`);
    console.log(`💚 Endpoint de salud: http://localhost:${PORT}/api/health`);
    
    // Inicializar datos frescos
    await initializeData();
});

module.exports = app; 