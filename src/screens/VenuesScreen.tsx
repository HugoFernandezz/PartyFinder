import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  TouchableOpacity,
  Image,
  Linking,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Venue } from '../types';
import { apiService } from '../services/api';
import { ConnectionStatus } from '../components/ConnectionStatus';

interface VenueCardProps {
  venue: Venue;
  onPress: () => void;
}

const VenueCard: React.FC<VenueCardProps> = ({ venue, onPress }) => {
  const handleCall = () => {
    Linking.openURL(`tel:${venue.phone}`);
  };

  const handleWebsite = () => {
    Linking.openURL(venue.website);
  };

  return (
    <TouchableOpacity style={styles.venueCard} onPress={onPress}>
      <Image
        source={{ uri: venue.imageUrl || 'https://via.placeholder.com/300x150' }}
        style={styles.venueImage}
        resizeMode="cover"
      />
      
      <View style={styles.venueContent}>
        <View style={styles.venueHeader}>
          <Text style={styles.venueName}>{venue.name}</Text>
          <View style={styles.categoryBadge}>
            <Ionicons name={venue.category.icon as any} size={12} color="#6366f1" />
            <Text style={styles.categoryText}>{venue.category.name}</Text>
          </View>
        </View>
        
        <Text style={styles.venueDescription} numberOfLines={2}>
          {venue.description}
        </Text>
        
        <View style={styles.venueAddress}>
          <Ionicons name="location-outline" size={16} color="#666" />
          <Text style={styles.addressText}>{venue.address}</Text>
        </View>
        
        <View style={styles.venueActions}>
          <TouchableOpacity style={styles.actionButton} onPress={handleCall}>
            <Ionicons name="call-outline" size={16} color="#6366f1" />
            <Text style={styles.actionText}>Llamar</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton} onPress={handleWebsite}>
            <Ionicons name="globe-outline" size={16} color="#6366f1" />
            <Text style={styles.actionText}>Web</Text>
          </TouchableOpacity>
          
          <View style={styles.statusContainer}>
            <View style={[styles.statusDot, { backgroundColor: venue.isActive ? '#10b981' : '#ef4444' }]} />
            <Text style={styles.statusText}>
              {venue.isActive ? 'Abierto' : 'Cerrado'}
            </Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );
};

export const VenuesScreen: React.FC = () => {
  const [venues, setVenues] = useState<Venue[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadVenues();
  }, []);

  const loadVenues = async () => {
    try {
      setLoading(true);
      
      const response = await apiService.getActiveVenues();
      if (response.success) {
        setVenues(response.data);
      } else {
        Alert.alert('Error', response.error || 'Error al cargar los locales');
        setVenues([]);
      }
      
    } catch (error) {
      Alert.alert('Error', 'Error al conectar con el servidor');
      console.error('Error loading venues:', error);
      setVenues([]);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadVenues();
    setRefreshing(false);
  };

  const handleVenuePress = (venue: Venue) => {
    Alert.alert(
      venue.name,
      `${venue.description}\n\nDirección: ${venue.address}\nTeléfono: ${venue.phone}\nCategoría: ${venue.category.name}`,
      [
        { text: 'Cerrar', style: 'cancel' },
        { text: 'Ver Fiestas', onPress: () => {} },
        { text: 'Llamar', onPress: () => Linking.openURL(`tel:${venue.phone}`) }
      ]
    );
  };

  const renderVenueCard = ({ item }: { item: Venue }) => (
    <VenueCard 
      venue={item} 
      onPress={() => handleVenuePress(item)}
    />
  );

  const renderHeader = () => (
    <View style={styles.header}>
      <Text style={styles.title}>Locales de Murcia</Text>
      <Text style={styles.subtitle}>
        Descubre todos los lugares de ocio nocturno
      </Text>
      <ConnectionStatus />
    </View>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="business-outline" size={64} color="#ccc" />
      <Text style={styles.emptyTitle}>No hay locales disponibles</Text>
      <Text style={styles.emptySubtitle}>
        Vuelve más tarde para ver nuevos locales
      </Text>
    </View>
  );

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#6366f1" />
          <Text style={styles.loadingText}>Cargando locales...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={venues}
        renderItem={renderVenueCard}
        keyExtractor={(item) => item.id}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={renderEmptyState}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={['#6366f1']}
            tintColor="#6366f1"
          />
        }
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
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
  },
  mockDataBanner: {
    backgroundColor: '#fef3c7',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    marginTop: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#f59e0b',
  },
  mockDataText: {
    fontSize: 14,
    color: '#92400e',
    fontWeight: '500',
  },
  listContent: {
    paddingBottom: 20,
  },
  venueCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  venueImage: {
    width: '100%',
    height: 150,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  venueContent: {
    padding: 16,
  },
  venueHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  venueName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    flex: 1,
  },
  categoryBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f9ff',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  categoryText: {
    fontSize: 12,
    color: '#6366f1',
    marginLeft: 4,
    fontWeight: '500',
  },
  venueDescription: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
    marginBottom: 12,
  },
  venueAddress: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  addressText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
    flex: 1,
  },
  venueActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#f0f9ff',
  },
  actionText: {
    fontSize: 12,
    color: '#6366f1',
    marginLeft: 4,
    fontWeight: '500',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    color: '#6b7280',
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