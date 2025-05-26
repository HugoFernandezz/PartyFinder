import { ApiResponse, Party, Venue } from '../types';

// Configuración del servidor local - detecta automáticamente la IP
const getApiBaseUrl = () => {
  // Detectar si estamos en desarrollo web o móvil
  const isWeb = typeof window !== 'undefined' && window.location;
  
  if (isWeb) {
    // En web, usar localhost
    return `http://localhost:3001`;
  } else {
    // En móvil, usar la IP de la red local
    return `http://192.168.1.49:3001`;
  }
};

const API_BASE_URL = getApiBaseUrl();

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

  private async makeRequest<T>(endpoint: string, method: 'GET' | 'POST' = 'GET', body?: any, useCache: boolean = true): Promise<ApiResponse<T>> {
    const cacheKey = `${method}:${endpoint}:${JSON.stringify(body || {})}`;
    
    // Intentar usar cache para GET requests
    if (method === 'GET' && useCache) {
      const cachedData = this.getCachedData<ApiResponse<T>>(cacheKey);
      if (cachedData) {
        return cachedData;
      }
    }

    try {
      const config: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache', // Evitar cache del navegador
        },
        cache: 'no-store', // Evitar cache del navegador
      };

      if (body && method === 'POST') {
        config.body = JSON.stringify(body);
      }

      console.log(`🌐 Haciendo petición a: ${API_BASE_URL}${endpoint}`);
      const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      const result: ApiResponse<T> = {
        success: true,
        data: data.data || data, // Manejar respuestas con wrapper
      };

      // Cachear solo respuestas exitosas de GET
      if (method === 'GET' && useCache) {
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

  // Obtener todas las fiestas disponibles
  async getTodaysParties(): Promise<ApiResponse<Party[]>> {
    return this.makeRequest<Party[]>('/api/parties/today');
  }

  // Obtener todos los locales activos
  async getActiveVenues(): Promise<ApiResponse<Venue[]>> {
    return this.makeRequest<Venue[]>('/api/venues/active');
  }

  // Obtener datos completos (venues + parties)
  async getCompleteData(): Promise<ApiResponse<{ venues: Venue[], parties: Party[] }>> {
    return this.makeRequest<{ venues: Venue[], parties: Party[] }>('/api/data/complete');
  }

  // Buscar fiestas por término
  async searchParties(searchTerm: string): Promise<ApiResponse<Party[]>> {
    return this.makeRequest<Party[]>(`/api/parties/search?q=${encodeURIComponent(searchTerm)}`);
  }

  // Forzar actualización de datos
  async forceUpdate(): Promise<ApiResponse<any>> {
    this.clearCache(); // Limpiar cache local antes de forzar actualización
    return this.makeRequest<any>('/api/update', 'POST', null, false);
  }

  // Obtener estado del servidor
  async getServerStatus(): Promise<ApiResponse<any>> {
    return this.makeRequest<any>('/api/status', 'GET', null, false); // Sin cache para estado
  }

  // Obtener datos frescos sin cache
  async getFreshData(): Promise<ApiResponse<{ venues: Venue[], parties: Party[] }>> {
    this.clearCache();
    return this.makeRequest<{ venues: Venue[], parties: Party[] }>('/api/data/complete', 'GET', null, false);
  }

  // Limpiar cache del servidor
  async clearServerCache(): Promise<ApiResponse<any>> {
    this.clearCache(); // Limpiar cache local también
    return this.makeRequest<any>('/api/clear-cache', 'POST', null, false);
  }
}

export const apiService = new ApiService(); 