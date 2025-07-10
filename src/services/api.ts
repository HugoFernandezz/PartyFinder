import { ApiResponse, Party, Venue, TicketType } from '../types';

// URL del bin de JSONBin que contiene los datos de eventos
const API_BASE_URL = 'https://api.jsonbin.io/v3/b/686d49718960c979a5b94ce1/latest';

// Clave de acceso para JSONBin. 
// Es más seguro almacenarla en una variable de entorno en una aplicación real.
const API_MASTER_KEY = '$2a$10$h64fSgvYbJKKoITgCHExTOqLoX6KlNaeNoN0VJAHHgcf9SJ9pDRUq';

// Función para transformar los datos de la API al formato que la app espera
const transformData = (apiData: any[]): { venues: Venue[], parties: Party[] } => {
  const venues: Venue[] = [];
  const parties: Party[] = [];
  const venueMap = new Map<string, Venue>();

  apiData.forEach((item, index) => {
    // Comprobación de seguridad mejorada para la nueva estructura
    if (!item || !item.evento || !item.evento.lugar) {
      console.warn(`Saltando item con datos incompletos en el índice ${index}:`, item);
      return;
    }

    const eventoData = item.evento;
    const lugarData = eventoData.lugar;

    // 1. Procesar y añadir el Venue (si no existe ya)
    let venue: Venue | undefined = venueMap.get(lugarData.nombre);
    if (!venue) {
      venue = {
        id: `v${venueMap.size + 1}`,
        name: lugarData.nombre,
        description: lugarData.descripcion || `Eventos en ${lugarData.nombre}`,
        address: lugarData.direccion,
        imageUrl: lugarData.imagen_url || 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=600&fit=crop&crop=center',
        website: lugarData.sitio_web || '',
        phone: lugarData.telefono || '',
        isActive: true,
        category: {
          id: '1',
          name: lugarData.categoria || 'Discoteca',
          icon: 'musical-notes',
        },
      };
      venueMap.set(venue.id, venue);
      venues.push(venue);
    }

    // 2. Procesar los Tipos de Entrada
    const ticketTypes: TicketType[] = (eventoData.entradas || []).map((t: any, i: number) => ({
      id: `t${index}-${i}`,
      name: t.tipo, // <-- CORREGIDO: de 'nombre' a 'tipo'
      description: t.descripcion || '',
      price: parseFloat(t.precio) || 0,
      isAvailable: !t.agotadas, // <-- CORREGIDO: de 'agotado' a 'agotadas'
      isSoldOut: t.agotadas,   // <-- CORREGIDO: de 'agotado' a 'agotadas'
      fewLeft: t.quedan_pocas || false, // <-- CORREGIDO: de 'fewLeft' a 'quedan_pocas'
      restrictions: t.restricciones,
      purchaseUrl: t.link_compra, // <-- AÑADIDO
    }));

    // 3. Procesar y añadir la Party
    const party: Party = {
      id: `p${index + 1}`,
      venueId: venue.id,
      venueName: venue.name,
      title: eventoData.nombreEvento,
      description: eventoData.descripcion || `Únete a la fiesta en ${venue.name}`,
      date: eventoData.fecha,
      startTime: eventoData.hora_inicio,
      endTime: eventoData.hora_fin,
      price: Math.min(...ticketTypes.map(t => t.price).filter(p => p > 0), Infinity),
      imageUrl: eventoData.imagen_url || venue.imageUrl,
      ticketUrl: eventoData.url_entradas || '', // <-- AÑADIDO: Valor por defecto
      isAvailable: ticketTypes.some(t => t.isAvailable),
      fewLeft: ticketTypes.some(t => t.fewLeft && t.isAvailable), // <-- AÑADIDO
      capacity: eventoData.aforo || 500,
      soldTickets: eventoData.entradas_vendidas || 0,
      tags: eventoData.tags || ['Fiestas'],
      venueAddress: venue.address,
      ticketTypes: ticketTypes,
    };
    parties.push(party);
  });

  return { venues, parties };
};


class ApiService {
  private cache = new Map<string, { data: any; timestamp: number; lastUpdateDate: string }>();
  private readonly UPDATE_HOUR = 20; // 20:30 Madrid
  private readonly UPDATE_MINUTE = 30;

  // Obtener la fecha/hora actual en zona horaria de Madrid
  private getMadridTime(): Date {
    return new Date(new Date().toLocaleString("en-US", {timeZone: "Europe/Madrid"}));
  }

  // Verificar si necesitamos hacer una nueva petición
  private shouldFetchNewData(): boolean {
    const madridTime = this.getMadridTime();
    const currentHour = madridTime.getHours();
    const currentMinute = madridTime.getMinutes();
    const currentDate = madridTime.toDateString();

    console.log(`🕐 Hora actual Madrid: ${currentHour}:${currentMinute.toString().padStart(2, '0')} - ${currentDate}`);

    // TEMPORAL: Permitir peticiones siempre para diagnosticar
    console.log(`🔧 MODO DEBUG: Permitiendo peticiones siempre`);
    return true;

    // Código original comentado temporalmente
    /*
    // Obtener información del caché
    const cached = this.cache.get(API_BASE_URL);
    
    // Si no hay caché, necesitamos datos
    if (!cached) {
      console.log(`📭 No hay caché disponible`);
      // Solo si ya es después de las 20:30
      const shouldFetch = currentHour > this.UPDATE_HOUR || 
             (currentHour === this.UPDATE_HOUR && currentMinute >= this.UPDATE_MINUTE);
      console.log(`🔄 Debería hacer petición? ${shouldFetch}`);
      return shouldFetch;
    }

    console.log(`💾 Caché disponible del: ${cached.lastUpdateDate}`);

    // Si ya tenemos datos de hoy después de las 20:30, no necesitamos más
    if (cached.lastUpdateDate === currentDate) {
      console.log(`✅ Ya tenemos datos de hoy`);
      return false;
    }

    // Si es un día nuevo y ya es después de las 20:30
    const shouldFetch = currentHour > this.UPDATE_HOUR || 
           (currentHour === this.UPDATE_HOUR && currentMinute >= this.UPDATE_MINUTE);
    console.log(`🔄 Día nuevo - Debería hacer petición? ${shouldFetch}`);
    return shouldFetch;
    */
  }

  // Verificar si hay datos válidos en caché (aunque sean del día anterior)
  private hasValidCachedData(): boolean {
    const cached = this.cache.get(API_BASE_URL);
    return cached != null && cached.data != null;
  }

  private getCachedData<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (cached && cached.data) {
      const madridTime = this.getMadridTime();
      const cacheDate = new Date(cached.timestamp);
      
      console.log(`📊 Usando datos cacheados del: ${cacheDate.toLocaleDateString('es-ES')}`);
      return cached.data;
    }
    return null;
  }

  private setCachedData(key: string, data: any): void {
    const madridTime = this.getMadridTime();
    this.cache.set(key, { 
      data, 
      timestamp: Date.now(),
      lastUpdateDate: madridTime.toDateString()
    });
    console.log(`💾 Datos cacheados para el: ${madridTime.toDateString()}`);
  }

  public clearCache(): void {
    this.cache.clear();
    console.log('🗑️ Cache del API limpiada');
  }

  // Obtener información sobre cuándo será la próxima actualización
  public getNextUpdateInfo(): { nextUpdate: Date; hasNewDataAvailable: boolean; usingCacheFrom: string | null } {
    const madridTime = this.getMadridTime();
    const today = new Date(madridTime);
    const tomorrow = new Date(madridTime);
    tomorrow.setDate(tomorrow.getDate() + 1);

    // Calcular próxima actualización
    let nextUpdate: Date;
    if (madridTime.getHours() < this.UPDATE_HOUR || 
        (madridTime.getHours() === this.UPDATE_HOUR && madridTime.getMinutes() < this.UPDATE_MINUTE)) {
      // Hoy a las 20:30
      nextUpdate = new Date(today.setHours(this.UPDATE_HOUR, this.UPDATE_MINUTE, 0, 0));
    } else {
      // Mañana a las 20:30
      nextUpdate = new Date(tomorrow.setHours(this.UPDATE_HOUR, this.UPDATE_MINUTE, 0, 0));
    }

    const cached = this.cache.get(API_BASE_URL);
    const hasNewDataAvailable = this.shouldFetchNewData();
    const usingCacheFrom = cached ? new Date(cached.timestamp).toLocaleDateString('es-ES') : null;

    return { nextUpdate, hasNewDataAvailable, usingCacheFrom };
  }

  private async makeRequest<T>(forceRequest: boolean = false): Promise<ApiResponse<T>> {
    const cacheKey = API_BASE_URL;
    
    console.log(`🚀 makeRequest iniciado - forceRequest: ${forceRequest}`);
    
    // Siempre intentar usar datos en caché primero si están disponibles
    if (this.hasValidCachedData() && !forceRequest) {
      console.log(`📦 Usando datos del caché`);
      const cachedData = this.getCachedData<ApiResponse<T>>(cacheKey);
      if (cachedData) {
        console.log(`✅ Datos del caché devueltos - ${cachedData.data ? Object.keys(cachedData.data).length : 0} propiedades`);
        return cachedData;
      }
    }

    // Solo hacer petición si es momento adecuado o si se fuerza
    if (!forceRequest && !this.shouldFetchNewData()) {
      console.log(`⏰ No es momento de hacer petición`);
      // Si no hay datos en caché y no es momento de hacer petición, devolver vacío
      if (!this.hasValidCachedData()) {
        console.log(`📭 Sin caché y sin petición - devolviendo vacío`);
        return {
          success: true,
          data: { venues: [], parties: [] } as T,
        };
      }
    }

    try {
      const config: RequestInit = {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-Master-Key': API_MASTER_KEY,
        },
      };

      console.log(`🌐 Haciendo petición programada a: ${API_BASE_URL}`);
      const response = await fetch(API_BASE_URL, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      console.log(`📥 Datos recibidos - record existe: ${!!data.record}, items: ${data.record ? data.record.length : 0}`);
      
      // Transformar los datos crudos al formato que la app espera
      const transformedData = transformData(data.record);
      console.log(`🔄 Datos transformados - venues: ${transformedData.venues.length}, parties: ${transformedData.parties.length}`);

      const result: ApiResponse<T> = {
        success: true,
        data: transformedData as any,
      };

      // Cachear la respuesta exitosa
      this.setCachedData(cacheKey, result);

      return result;
    } catch (error) {
      console.error('API Error:', error);
      
      // Si hay error pero tenemos datos en caché, usarlos silenciosamente
      if (this.hasValidCachedData()) {
        console.log('⚠️ Error en petición, usando datos cacheados');
        const cachedData = this.getCachedData<ApiResponse<T>>(cacheKey);
        if (cachedData) {
          return cachedData;
        }
      }

      // Si no hay caché, devolver datos vacíos (no error al usuario)
      console.log(`❌ Error sin caché - devolviendo vacío`);
      return {
        success: true,
        data: { venues: [], parties: [] } as T,
      };
    }
  }

  // Obtener datos completos (venues + parties)
  async getCompleteData(): Promise<ApiResponse<{ venues: Venue[], parties: Party[] }>> {
    return this.makeRequest<{ venues: Venue[], parties: Party[] }>();
  }

  // Forzar obtención de datos frescos (solo si es después de las 20:30)
  async getFreshData(): Promise<ApiResponse<{ venues: Venue[], parties: Party[] }>> {
    // Intentar obtener datos frescos, pero si no es momento, usar caché
    return this.makeRequest<{ venues: Venue[], parties: Party[] }>(this.shouldFetchNewData());
  }

  // Las siguientes funciones se mantienen por compatibilidad
  async getTodaysParties(): Promise<ApiResponse<Party[]>> {
    const response = await this.getCompleteData();
    if (response.success) {
      return { success: true, data: response.data.parties };
    }
    return { success: false, data: [], error: response.error };
  }

  async getActiveVenues(): Promise<ApiResponse<Venue[]>> {
    const response = await this.getCompleteData();
    if (response.success) {
      return { success: true, data: response.data.venues };
    }
    return { success: false, data: [], error: response.error };
  }
}

export const apiService = new ApiService(); 