import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Linking,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Party, TicketType } from '../types';
import { TicketCard } from '../components/TicketCard';

const { width } = Dimensions.get('window');

interface EventDetailScreenProps {
  route: {
    params: {
      party: Party;
    };
  };
  navigation: any;
}

const getPartyImageSource = (party: Party) => {
  if (party.venueName.toUpperCase() === 'MACCÄO OPEN AIR CLUB') {
    return require('../../assets/Maccao.jpeg'); 
  }
  return { uri: party.imageUrl };
};

export const EventDetailScreen: React.FC<EventDetailScreenProps> = ({ route, navigation }) => {
  const { party } = route.params;
  
  const isBusEvent = party.title.toUpperCase().includes('BUS');

  const handleBuyTickets = () => {
    // Si la URL principal no existe, intentar abrir la del primer ticket disponible
    const urlToOpen = party.ticketUrl || party.ticketTypes?.find(t => t.isAvailable && t.purchaseUrl)?.purchaseUrl;
    if (urlToOpen) {
      Linking.openURL(urlToOpen);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (time: string) => {
    return time;
  };

  const getPriceDisplay = () => {
    // Si el precio principal es válido, usarlo
    if (party.price !== null && party.price !== undefined && 
        !isNaN(party.price) && isFinite(party.price)) {
      return party.price === 0 ? 'GRATIS' : `${party.price}€`;
    }

    // Si no hay tipos de entrada, mostrar que no hay info
    if (!party.ticketTypes || party.ticketTypes.length === 0) {
      return 'Sin información';
    }

    // Buscar entradas disponibles
    const availableTickets = party.ticketTypes.filter(ticket => 
      ticket.isAvailable && !ticket.isSoldOut
    );

    if (availableTickets.length === 0) {
      return 'Agotado';
    }

    // Obtener el precio más bajo de las entradas disponibles
    const minPrice = Math.min(...availableTickets.map(ticket => ticket.price));
    const maxPrice = Math.max(...availableTickets.map(ticket => ticket.price));

    if (minPrice === maxPrice) {
      return minPrice === 0 ? 'GRATIS' : `${minPrice}€`;
    } else {
      return `Desde ${minPrice}€`;
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header con imagen */}
        <View style={styles.imageContainer}>
          <Image
            source={getPartyImageSource(party)}
            style={styles.eventImage}
            resizeMode="cover"
          />
          <TouchableOpacity 
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          
          {/* Overlay con información básica */}
          <View style={styles.imageOverlay}>
            <Text style={styles.eventTitle}>{party.title}</Text>
            <Text style={styles.venueName}>{party.venueName}</Text>
          </View>
        </View>

        {/* Contenido principal */}
        <View style={styles.content}>
          {/* Información de fecha y hora */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Ionicons name="calendar-outline" size={24} color="#6366f1" />
              <Text style={styles.sectionTitle}>Fecha y Hora</Text>
            </View>
            <Text style={styles.dateText}>{formatDate(party.date)}</Text>
            <View style={styles.timeContainer}>
              <View style={styles.timeItem}>
                <Text style={styles.timeLabel}>Inicio</Text>
                <Text style={styles.timeValue}>{formatTime(party.startTime)}</Text>
              </View>
              <View style={styles.timeSeparator} />
              <View style={styles.timeItem}>
                <Text style={styles.timeLabel}>Fin</Text>
                <Text style={styles.timeValue}>{formatTime(party.endTime)}</Text>
              </View>
            </View>
          </View>

          {/* Precio */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Ionicons name="pricetag-outline" size={24} color="#6366f1" />
              <Text style={styles.sectionTitle}>Precio</Text>
            </View>
            <Text style={styles.priceText}>
              {getPriceDisplay()}
            </Text>
          </View>

          {/* Descripción */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Ionicons name="information-circle-outline" size={24} color="#6366f1" />
              <Text style={styles.sectionTitle}>Descripción</Text>
            </View>
            {party.description.split('\n').map((text, index) => (
              <Text key={index} style={styles.descriptionText}>
                {text}
              </Text>
            ))}
          </View>

          {/* Información de transporte para eventos de bus */}
          {isBusEvent && (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="bus-outline" size={24} color="#f59e0b" />
                <Text style={styles.sectionTitle}>Información de Transporte</Text>
              </View>
              <View style={styles.busInfoContainer}>
                <Ionicons name="alert-circle-outline" size={20} color="#f59e0b" />
                <Text style={styles.busInfoText}>
                  Esta es una reserva de <Text style={styles.busInfoBold}>transporte al evento</Text>. 
                  No incluye la entrada al evento, solo el viaje en autobús.
                </Text>
              </View>
            </View>
          )}

          {/* Ubicación */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Ionicons name="location-outline" size={24} color="#6366f1" />
              <Text style={styles.sectionTitle}>Ubicación</Text>
            </View>
            <Text style={styles.venueText}>{party.venueName}</Text>
            {party.venueAddress && (
              <Text style={styles.addressText}>{party.venueAddress}</Text>
            )}
          </View>

          {/* Tags */}
          {party.tags && party.tags.length > 0 && (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="musical-notes-outline" size={24} color="#6366f1" />
                <Text style={styles.sectionTitle}>Géneros Musicales</Text>
              </View>
              <View style={styles.tagsContainer}>
                {party.tags.map((tag, index) => (
                  <View key={index} style={styles.tag}>
                    <Text style={styles.tagText}>{tag}</Text>
                  </View>
                ))}
              </View>
            </View>
          )}

          {/* Tipos de Entrada */}
          {party.ticketTypes && party.ticketTypes.length > 0 && (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="ticket-outline" size={24} color="#6366f1" />
                <Text style={styles.sectionTitle}>Tipos de Entrada</Text>
              </View>
              <View style={styles.ticketTypesContainer}>
                {party.ticketTypes.map((ticket) => (
                  <TicketCard key={ticket.id} ticket={ticket} />
                ))}
              </View>
            </View>
          )}

        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  imageContainer: {
    position: 'relative',
    height: 300,
  },
  eventImage: {
    width: '100%',
    height: '100%',
  },
  backButton: {
    position: 'absolute',
    top: 50,
    left: 20,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    padding: 20,
  },
  eventTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  venueName: {
    fontSize: 16,
    color: '#e5e7eb',
  },
  content: {
    padding: 20,
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
    marginLeft: 8,
  },
  dateText: {
    fontSize: 16,
    color: '#374151',
    marginBottom: 8,
    textTransform: 'capitalize',
  },
  timeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f3f4f6',
    borderRadius: 12,
    padding: 16,
  },
  timeItem: {
    flex: 1,
    alignItems: 'center',
  },
  timeLabel: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 4,
  },
  timeValue: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
  },
  timeSeparator: {
    width: 1,
    height: 30,
    backgroundColor: '#d1d5db',
    marginHorizontal: 16,
  },
  priceText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6366f1',
  },
  descriptionText: {
    fontSize: 16,
    color: '#374151',
    lineHeight: 24,
  },
  venueText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  addressText: {
    fontSize: 14,
    color: '#6b7280',
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  tag: {
    backgroundColor: '#e0e7ff',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  tagText: {
    fontSize: 14,
    color: '#6366f1',
    fontWeight: '500',
  },
  availabilityContainer: {
    backgroundColor: '#f9fafb',
    padding: 16,
    borderRadius: 12,
  },
  availabilityText: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 8,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#6366f1',
    borderRadius: 4,
  },
  statusText: {
    fontSize: 14,
    fontWeight: '500',
  },
  // Estilos para tipos de entrada
  ticketTypesContainer: {
    gap: 16,
  },
  ticketTypeCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    overflow: 'hidden',
    shadowColor: '#6366f1',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 5,
  },
  ticketTypeCardSoldOut: {
    backgroundColor: '#f1f5f9',
    borderColor: '#d1d5db',
    shadowColor: 'transparent',
    elevation: 0,
  },
  ticketTypeCardFewLeft: {
    borderColor: '#f59e0b',
    borderWidth: 1,
  },
  ticketTypeContent: {
    padding: 16,
  },
  ticketTypeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  ticketTypeInfo: {
    flex: 1,
    marginRight: 12,
  },
  priceSection: {
    alignItems: 'flex-end',
  },
  ticketTypeName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 6,
  },
  ticketTypeNameDisabled: {
    color: '#94a3b8',
  },
  badgesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginTop: 4,
  },
  fewLeftBadge: {
    backgroundColor: '#fef3c7',
    borderColor: '#f59e0b',
    borderWidth: 1,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    marginBottom: 4,
    alignSelf: 'flex-start',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  fewLeftText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#d97706',
  },
  ticketTypePrice: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#6366f1',
  },
  ticketTypePriceDisabled: {
    color: '#94a3b8',
  },
  promotionBadge: {
    backgroundColor: '#fef3c7',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    marginBottom: 4,
    alignSelf: 'flex-start',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  promotionText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#d97706',
  },
  vipBadge: {
    backgroundColor: '#ddd6fe',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    marginBottom: 4,
    alignSelf: 'flex-start',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  vipText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#7c3aed',
  },
  ticketTypeDescription: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 12,
    lineHeight: 20,
  },
  ticketTypeDescriptionDisabled: {
    color: '#94a3b8',
  },
  ticketTypeRestrictions: {
    fontSize: 12,
    color: '#f59e0b',
    marginBottom: 12,
    fontStyle: 'italic',
  },
  ticketActionContainer: {
    backgroundColor: '#6366f1',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingVertical: 12,
    marginTop: 16,
    borderRadius: 12,
  },
  ticketActionContainerFewLeft: {
    backgroundColor: '#f59e0b',
  },
  ticketActionContainerSoldOut: {
    backgroundColor: '#e2e8f0',
  },
  ticketActionText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  ticketActionTextDisabled: {
    color: '#94a3b8',
    fontSize: 16,
    fontWeight: '600',
  },
  soldOutActionContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  busInfoContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#fef3c7',
    borderRadius: 12,
    padding: 20,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#f59e0b',
  },
  busInfoText: {
    flex: 1,
    fontSize: 14,
    color: '#d97706',
    lineHeight: 20,
    marginLeft: 12,
  },
  busInfoBold: {
    fontWeight: 'bold',
  },
}); 