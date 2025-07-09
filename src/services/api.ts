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
  private cache = new Map<string, { data: any; timestamp: number }>();
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

  private getCachedData<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      console.log(`📊 Usando datos cacheados para: ${key}`);
      return cached.data;
    }
    return null;
  }

  private setCachedData(key: string, data: any): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  public clearCache(): void {
    this.cache.clear();
    console.log('🗑️ Cache del API limpiada');
  }

  private async makeRequest<T>(useCache: boolean = true): Promise<ApiResponse<T>> {
    const cacheKey = API_BASE_URL;
    
    // Intentar usar cache para GET requests
    if (useCache) {
      const cachedData = this.getCachedData<ApiResponse<T>>(cacheKey);
      if (cachedData) {
        return cachedData;
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

      console.log(`🌐 Haciendo petición a: ${API_BASE_URL}`);
      const response = await fetch(API_BASE_URL, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      
      // Transformar los datos crudos al formato que la app espera
      const transformedData = transformData(data.record);

      const result: ApiResponse<T> = {
        success: true,
        data: transformedData as any, // Hacemos un cast aquí
      };

      // Cachear solo respuestas exitosas
      if (useCache) {
        this.setCachedData(cacheKey, result);
      }

      return result;
    } catch (error) {
      console.error('API Error:', error);
      const errorResult: ApiResponse<T> = {
        success: false,
        data: {} as T,
        error: error instanceof Error ? error.message : 'Error desconocido',
      };
      return errorResult;
    }
  }

  // Obtener datos completos (venues + parties)
  async getCompleteData(): Promise<ApiResponse<{ venues: Venue[], parties: Party[] }>> {
    // Este es ahora el método principal para obtener todos los datos.
    return this.makeRequest<{ venues: Venue[], parties: Party[] }>();
  }

  // Obtener datos frescos sin cache
  async getFreshData(): Promise<ApiResponse<{ venues: Venue[], parties: Party[] }>> {
    this.clearCache();
    return this.makeRequest<{ venues: Venue[], parties: Party[] }>(false);
  }

  // Las siguientes funciones se dejan por compatibilidad, pero todas obtienen los mismos datos.
  // En una futura refactorización, podrían eliminarse si no se usan en la UI.

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