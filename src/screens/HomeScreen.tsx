import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SectionList,
  ActivityIndicator,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { PartyCard } from '../components/PartyCard';
import { Party } from '../types';
import { apiService } from '../services/api';
import { RootStackParamList } from '../components/Navigation';
import { StackNavigationProp } from '@react-navigation/stack';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

interface HomeScreenProps {
  navigation: HomeScreenNavigationProp;
}

interface SectionData {
  title: string;
  data: Party[];
}

export const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [parties, setParties] = useState<Party[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedVenue, setSelectedVenue] = useState<string>('Todas');
  const [availableVenues, setAvailableVenues] = useState<string[]>(['Todas']);
  
  // Usar useRef para mantener referencia actual de parties sin re-renders
  const partiesRef = useRef<Party[]>(parties);
  
  // Actualizar la referencia cuando parties cambie
  useEffect(() => {
    partiesRef.current = parties;
  }, [parties]);

  useEffect(() => {
    loadParties();
    
    // Timer para verificar nuevos datos automáticamente cada hora
    const backgroundUpdateInterval = setInterval(async () => {
      try {
        const response = await apiService.getCompleteData();
        if (response.success && response.data.parties.length > 0) {
          // Comparación más eficiente: verificar longitud y IDs usando la ref
          const newParties = response.data.parties;
          const currentParties = partiesRef.current;
          const hasChanges = newParties.length !== currentParties.length || 
                           newParties.some((party, index) => 
                             !currentParties[index] || currentParties[index].id !== party.id
                           );
          
          if (hasChanges) {
            setParties(newParties);
          }
        }
      } catch (error) {
        // Error silenciado para no spam en producción
      }
    }, 3600000); // Cada hora

    return () => clearInterval(backgroundUpdateInterval);
  }, []); // Sin dependencias para evitar bucle infinito

  useEffect(() => {
    // Extraer todas las discotecas únicas de los eventos
    const allVenues = new Set<string>();
    parties.forEach(party => {
      allVenues.add(party.venueName);
    });
    
    const sortedVenues = ['Todas', ...Array.from(allVenues).sort()];
    setAvailableVenues(sortedVenues);
  }, [parties]);

  // Optimizar processParties usando useMemo
  const partySections = useMemo((): SectionData[] => {
    let filtered = parties;

    // Filtrar por discoteca seleccionada
    if (selectedVenue !== 'Todas') {
      filtered = filtered.filter(party => party.venueName === selectedVenue);
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
  }, [selectedVenue, parties]);

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

  const handleVenueSelect = useCallback((venue: string) => {
    setSelectedVenue(venue);
  }, []);

  const handlePartyPress = useCallback((party: Party) => {
    navigation.navigate('EventDetail', { party });
  }, [navigation]);

  const renderPartyCard = useCallback(({ item }: { item: Party }) => (
    <PartyCard 
      party={item} 
      onPress={() => handlePartyPress(item)}
    />
  ), [handlePartyPress]);

  const renderSectionHeader = useCallback(({ section: { title } }: { section: SectionData }) => {
    // Separar el día de la semana del resto de la fecha
    const parts = title.split(', ');
    const dayOfWeek = parts[0];
    const fullDate = parts.slice(1).join(', ');
    
    return (
      <View style={styles.sectionHeader}>
        <View style={styles.dateContainer}>
          <Ionicons name="calendar" size={22} color="#6366f1" style={styles.dateIcon} />
          <View style={styles.dateTextContainer}>
            <Text style={styles.dayOfWeek}>{dayOfWeek}</Text>
            <Text style={styles.fullDate}>{fullDate}</Text>
          </View>
        </View>
      </View>
    );
  }, []);

  const renderHeader = () => (
    <View>
      <View style={styles.header}>
        <Text style={styles.title}>PartyFinder Murcia</Text>
        <Text style={styles.subtitle}>
          Descubre las mejores fiestas de esta noche
        </Text>
      </View>
      
      {/* Selector de discotecas */}
      <View style={styles.venueSelector}>
        <Text style={styles.venueSelectorTitle}>Discotecas</Text>
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.venueScrollContainer}
        >
          {availableVenues.map((venue, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.venueButton,
                selectedVenue === venue && styles.venueButtonSelected
              ]}
              onPress={() => handleVenueSelect(venue)}
            >
              <Text style={[
                styles.venueButtonText,
                selectedVenue === venue && styles.venueButtonTextSelected
              ]}>
                {venue}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
    </View>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons 
        name="calendar-outline" 
        size={64} 
        color="#ccc" 
      />
      {selectedVenue !== 'Todas' ? (
        <>
          <Text style={styles.emptyTitle}>No hay eventos en {selectedVenue}</Text>
          <Text style={styles.emptySubtitle}>
            Selecciona otra discoteca o "Todas" para ver más eventos
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
    <SafeAreaView style={styles.safeArea} edges={['top', 'left', 'right']}>
      <SectionList
        sections={partySections}
        renderItem={renderPartyCard}
        keyExtractor={(item) => item.id}
        renderSectionHeader={renderSectionHeader}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={renderEmptyState}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
        style={styles.sectionList}
        stickySectionHeadersEnabled={true}
        bounces={false}
        overScrollMode="never"
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
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
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 15,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
  },
  listContent: {
    paddingBottom: 20,
    flexGrow: 1,
  },
  sectionHeader: {
    backgroundColor: '#ffffff',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionHeaderText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
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
  venueSelector: {
    paddingHorizontal: 20,
    paddingTop: 15,
    paddingBottom: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  venueSelectorTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 12,
    textAlign: 'center',
  },
  venueScrollContainer: {
    alignItems: 'center',
    paddingHorizontal: 10,
  },
  venueButton: {
    backgroundColor: '#f3f4f6',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginHorizontal: 6,
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  venueButtonSelected: {
    backgroundColor: '#6366f1',
    borderColor: '#6366f1',
  },
  venueButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#475569',
  },
  venueButtonTextSelected: {
    color: '#fff',
    fontWeight: '600',
  },
  dateContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dateIcon: {
    marginRight: 10,
  },
  dateTextContainer: {
    marginLeft: 10,
  },
  dayOfWeek: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  fullDate: {
    fontSize: 14,
    color: '#6b7280',
  },
  safeArea: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  sectionList: {
    backgroundColor: '#ffffff',
  },
}); 