import React, { useState, useEffect, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SectionList,
  TextInput,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { PartyCard } from '../components/PartyCard';
import { Party } from '../types';
import { apiService } from '../services/api';
import { RootStackParamList } from '../components/Navigation';
import { StackNavigationProp } from '@react-navigation/stack';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'HomeMain'>;

interface HomeScreenProps {
  navigation: HomeScreenNavigationProp;
}

interface SectionData {
  title: string;
  data: Party[];
}

export const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [parties, setParties] = useState<Party[]>([]);
  // El estado ahora será para las secciones
  const [partySections, setPartySections] = useState<SectionData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadParties();
    
    // Timer para verificar nuevos datos automáticamente cada hora
    const backgroundUpdateInterval = setInterval(async () => {
      try {
        console.log('🔄 Verificando nuevos datos en segundo plano...');
        const response = await apiService.getCompleteData();
        if (response.success && response.data.parties.length > 0) {
          // Solo actualizar si hay cambios en los datos
          if (JSON.stringify(response.data.parties) !== JSON.stringify(parties)) {
            console.log('✅ Nuevos datos encontrados, actualizando...');
            setParties(response.data.parties);
          }
        }
      } catch (error) {
        console.log('⚠️ Error en actualización automática:', error);
      }
    }, 3600000); // Cada hora

    return () => clearInterval(backgroundUpdateInterval);
  }, []);

  useEffect(() => {
    // La función que procesa ahora se llamará desde un useMemo
    const processedParties = processParties();
    setPartySections(processedParties);
  }, [searchQuery, parties]);

  const loadParties = async () => {
    try {
      setLoading(true);
      
      const response = await apiService.getCompleteData();
      
      if (response.success) {
        setParties(response.data.parties);
      } else {
        // Si no hay datos disponibles aún, mantener lista vacía sin mostrar error
        setParties([]);
      }
      
    } catch (error) {
      console.error('Error loading parties:', error);
      setParties([]);
    } finally {
      setLoading(false);
    }
  };

  const processParties = (): SectionData[] => {
    let filtered = parties;

    // Filtrar por búsqueda de texto
    if (searchQuery.trim()) {
      filtered = filtered.filter(party =>
        party.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        party.venueName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        party.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        party.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    // Ordenar por fecha cronológica ascendente
    filtered.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    // Agrupar en secciones por día
    const sections: { [key: string]: Party[] } = {};
    filtered.forEach(party => {
      const partyDate = new Date(party.date);
      const dayKey = new Date(partyDate.getFullYear(), partyDate.getMonth(), partyDate.getDate()).toISOString();
      
      if (!sections[dayKey]) {
        sections[dayKey] = [];
      }
      sections[dayKey].push(party);
    });

    // Formatear para SectionList
    const locale = 'es-ES';
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    return Object.keys(sections).map(dateKey => ({
      title: new Date(dateKey).toLocaleDateString(locale, options),
      data: sections[dateKey],
    }));
  };

  const handlePartyPress = (party: Party) => {
    navigation.navigate('EventDetail', { party });
  };

  const renderPartyCard = ({ item }: { item: Party }) => (
    <PartyCard 
      party={item} 
      onPress={() => handlePartyPress(item)}
    />
  );

  const renderSectionHeader = ({ section: { title } }: { section: SectionData }) => (
    <View style={styles.sectionHeader}>
      <Text style={styles.sectionHeaderText}>{title}</Text>
    </View>
  );

  const renderHeader = () => (
    <View>
      <View style={styles.header}>
        <Text style={styles.title}>PartyFinder Murcia</Text>
        <Text style={styles.subtitle}>
          Descubre las mejores fiestas de esta noche
        </Text>
        
        {/* Removed update info banner */}
        
        <View style={styles.searchContainer}>
          <Ionicons name="search-outline" size={20} color="#666" style={styles.searchIcon} />
          <TextInput
            style={styles.searchInput}
            placeholder="Buscar fiestas, locales..."
            value={searchQuery}
            onChangeText={setSearchQuery}
            placeholderTextColor="#999"
          />
          {searchQuery.length > 0 && (
            <Ionicons 
              name="close-circle" 
              size={20} 
              color="#666" 
              style={styles.clearIcon}
              onPress={() => setSearchQuery('')}
            />
          )}
        </View>
      </View>
      
      {/* Filtros de etiquetas */}
      {/* Removed TagFilter component */}
    </View>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons 
        name="calendar-outline" 
        size={64} 
        color="#ccc" 
      />
      {searchQuery ? (
        <>
          <Text style={styles.emptyTitle}>No se encontraron fiestas</Text>
          <Text style={styles.emptySubtitle}>
            Intenta con otros términos de búsqueda
          </Text>
        </>
      ) : (
        <>
          <Text style={styles.emptyTitle}>No hay fiestas disponibles</Text>
          <Text style={styles.emptySubtitle}>
            Vuelve más tarde para ver nuevos eventos
          </Text>
        </>
      )}
    </View>
  );

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#6366f1" />
          <Text style={styles.loadingText}>Cargando fiestas...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <SectionList
        sections={partySections}
        renderItem={renderPartyCard}
        keyExtractor={(item) => item.id}
        renderSectionHeader={renderSectionHeader}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={renderEmptyState}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
        stickySectionHeadersEnabled={true}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  header: {
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    marginBottom: 20,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f3f4f6',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  searchIcon: {
    marginRight: 12,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#1f2937',
  },
  clearIcon: {
    marginLeft: 12,
  },
  listContent: {
    paddingBottom: 20,
  },
  sectionHeader: {
    backgroundColor: '#f1f5f9',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
  },
  sectionHeaderText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#475569',
    textTransform: 'capitalize',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
    paddingVertical: 60,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#374151',
    marginTop: 16,
    marginBottom: 8,
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 24,
  },
}); 