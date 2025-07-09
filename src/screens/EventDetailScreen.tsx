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
import { Party } from '../types';

const { width } = Dimensions.get('window');

interface EventDetailScreenProps {
  route: {
    params: {
      party: Party;
    };
  };
  navigation: any;
}

export const EventDetailScreen: React.FC<EventDetailScreenProps> = ({ route, navigation }) => {
  const { party } = route.params;

  const handleBuyTickets = () => {
    // Si la URL principal no existe, intentar abrir la del primer ticket disponible
    const urlToOpen = party.ticketUrl || party.ticketTypes?.find(t => t.isAvailable && t.purchaseUrl)?.purchaseUrl;
    if (urlToOpen) {
      Linking.openURL(urlToOpen);
    }
  };

  const handleBuyTicketType = (ticket: TicketType) => {
    if (ticket.purchaseUrl) {
      Linking.openURL(ticket.purchaseUrl);
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

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header con imagen */}
        <View style={styles.imageContainer}>
          <Image
            source={{ uri: party.imageUrl }}
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
              {party.price === 0 ? 'GRATIS' : `${party.price}€`}
            </Text>
          </View>

          {/* Descripción */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Ionicons name="information-circle-outline" size={24} color="#6366f1" />
              <Text style={styles.sectionTitle}>Descripción</Text>
            </View>
            <Text style={styles.descriptionText}>{party.description}</Text>
          </View>

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
                {party.ticketTypes.map((ticket, index) => {
                  const isClickable = ticket.isAvailable && !!ticket.purchaseUrl;
                  return (
                    <TouchableOpacity 
                      key={ticket.id} 
                      style={[
                        styles.ticketTypeCard,
                        !isClickable && styles.ticketTypeCardDisabled
                      ]}
                      onPress={() => isClickable && handleBuyTicketType(ticket)}
                      disabled={!isClickable}
                    >
                      <View style={styles.ticketTypeHeader}>
                        <View style={styles.ticketTypeInfo}>
                          <Text style={styles.ticketTypeName}>{ticket.name}</Text>
                          {ticket.fewLeft && !ticket.isSoldOut && (
                            <View style={styles.fewLeftBadge}>
                              <Text style={styles.fewLeftText}>¡ÚLTIMAS ENTRADAS!</Text>
                            </View>
                          )}
                          {ticket.isPromotion && (
                            <View style={styles.promotionBadge}>
                              <Text style={styles.promotionText}>PROMOCIÓN</Text>
                            </View>
                          )}
                          {ticket.isVip && (
                            <View style={styles.vipBadge}>
                              <Text style={styles.vipText}>VIP</Text>
                            </View>
                          )}
                        </View>
                        <Text style={styles.ticketTypePrice}>{ticket.price}€</Text>
                      </View>
                      
                      {ticket.description && (
                        <Text style={styles.ticketTypeDescription}>{ticket.description}</Text>
                      )}
                      
                      {ticket.restrictions && (
                        <Text style={styles.ticketTypeRestrictions}>⚠️ {ticket.restrictions}</Text>
                      )}
                      
                      <View style={styles.ticketTypeFooter}>
                        <View style={[
                          styles.availabilityBadge,
                          { backgroundColor: ticket.isAvailable ? '#dcfce7' : '#fee2e2' }
                        ]}>
                          <Text style={[
                            styles.availabilityBadgeText,
                            { color: ticket.isAvailable ? '#16a34a' : '#dc2626' }
                          ]}>
                            {ticket.isAvailable ? 'Disponible' : 'Agotado'}
                          </Text>
                        </View>
                      </View>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>
          )}

          {/* Disponibilidad */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Ionicons name="people-outline" size={24} color="#6366f1" />
              <Text style={styles.sectionTitle}>Disponibilidad</Text>
            </View>
            <View style={styles.availabilityContainer}>
              <Text style={styles.availabilityText}>
                {party.soldTickets} / {party.capacity} entradas vendidas
              </Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { width: `${(party.soldTickets / party.capacity) * 100}%` }
                  ]} 
                />
              </View>
              <Text style={[
                styles.statusText,
                { color: party.isAvailable ? '#10b981' : '#ef4444' }
              ]}>
                {party.isAvailable ? 'Entradas disponibles' : 'Agotado'}
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* Botón de compra fijo */}
      <View style={styles.bottomContainer}>
        <TouchableOpacity 
          style={[
            styles.buyButton,
            (!party.isAvailable || !party.ticketUrl) && styles.buyButtonDisabled
          ]}
          onPress={handleBuyTickets}
          disabled={!party.isAvailable || !party.ticketUrl}
        >
          <Ionicons 
            name="ticket-outline" 
            size={24} 
            color="#fff" 
            style={styles.buyButtonIcon}
          />
          <Text style={styles.buyButtonText}>
            {party.isAvailable ? 'Comprar Entradas' : 'Agotado'}
          </Text>
        </TouchableOpacity>
      </View>
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
  bottomContainer: {
    padding: 20,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  buyButton: {
    backgroundColor: '#6366f1',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    borderRadius: 12,
  },
  buyButtonDisabled: {
    backgroundColor: '#9ca3af',
  },
  buyButtonIcon: {
    marginRight: 8,
  },
  buyButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  // Estilos para tipos de entrada
  ticketTypesContainer: {
    gap: 12,
  },
  ticketTypeCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  ticketTypeCardDisabled: {
    backgroundColor: '#f9fafb',
    borderColor: '#e5e7eb',
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
  ticketTypeName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 6,
  },
  fewLeftBadge: {
    backgroundColor: '#fffbeb',
    borderColor: '#f59e0b',
    borderWidth: 1,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    marginBottom: 4,
    alignSelf: 'flex-start',
  },
  fewLeftText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#d97706',
  },
  ticketTypePrice: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#6366f1',
  },
  promotionBadge: {
    backgroundColor: '#fef3c7',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    marginBottom: 4,
    alignSelf: 'flex-start',
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
  },
  vipText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#7c3aed',
  },
  ticketTypeDescription: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 8,
    lineHeight: 20,
  },
  ticketTypeRestrictions: {
    fontSize: 12,
    color: '#f59e0b',
    marginBottom: 8,
    fontStyle: 'italic',
  },
  ticketTypeFooter: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
  availabilityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 16,
  },
  availabilityBadgeText: {
    fontSize: 12,
    fontWeight: '500',
  },
}); 