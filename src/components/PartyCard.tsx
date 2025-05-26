import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  Linking,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Party } from '../types';

interface PartyCardProps {
  party: Party;
  onPress?: () => void;
}

export const PartyCard: React.FC<PartyCardProps> = ({ party, onPress }) => {
  const [imageError, setImageError] = useState(false);

  const handleBuyTickets = async () => {
    try {
      const supported = await Linking.canOpenURL(party.ticketUrl);
      if (supported) {
        await Linking.openURL(party.ticketUrl);
      } else {
        Alert.alert('Error', 'No se puede abrir el enlace de compra');
      }
    } catch (error) {
      Alert.alert('Error', 'Error al abrir el enlace de compra');
    }
  };

  const getImageSource = () => {
    if (imageError || !party.imageUrl) {
      // Imagen de fallback basada en el tipo de evento
      if (party.tags.some(tag => tag.toLowerCase().includes('electr'))) {
        return { uri: 'https://images.unsplash.com/photo-1571266028243-d220c9c3b31f?w=800&h=600&fit=crop&crop=center' };
      } else if (party.tags.some(tag => tag.toLowerCase().includes('karaoke'))) {
        return { uri: 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop&crop=center' };
      } else if (party.tags.some(tag => tag.toLowerCase().includes('acústico') || tag.toLowerCase().includes('concierto'))) {
        return { uri: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop&crop=center' };
      } else {
        return { uri: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&h=600&fit=crop&crop=center' };
      }
    }
    return { uri: party.imageUrl };
  };

  const getAvailabilityColor = () => {
    const percentage = (party.soldTickets / party.capacity) * 100;
    if (percentage >= 90) return '#ff4444';
    if (percentage >= 70) return '#ff8800';
    return '#44ff44';
  };

  const getAvailabilityText = () => {
    const available = party.capacity - party.soldTickets;
    if (available <= 0) return 'Agotado';
    if (available <= 10) return `Solo ${available} entradas`;
    return `${available} disponibles`;
  };

  return (
    <TouchableOpacity 
      style={[
        styles.container,
        !party.isAvailable && styles.containerSoldOut
      ]} 
      onPress={onPress}
    >
      <View style={styles.imageContainer}>
        <Image
          source={getImageSource()}
          style={[
            styles.image,
            !party.isAvailable && styles.imageSoldOut
          ]}
          resizeMode="cover"
          onError={() => setImageError(true)}
        />
        <View style={styles.overlay} />
        <View style={[
          styles.priceTag,
          !party.isAvailable && styles.priceTagSoldOut
        ]}>
          <Text style={[
            styles.priceText,
            !party.isAvailable && styles.priceTextSoldOut
          ]}>
            {party.price === 0 ? 'GRATIS' : `${party.price}€`}
          </Text>
        </View>
        {!party.isAvailable && (
          <View style={styles.soldOutOverlay}>
            <Text style={styles.soldOutText}>AGOTADO</Text>
          </View>
        )}
      </View>
      
      <View style={[
        styles.content,
        !party.isAvailable && styles.contentSoldOut
      ]}>
        <View style={styles.header}>
          <Text style={[
            styles.title,
            !party.isAvailable && styles.titleSoldOut
          ]} numberOfLines={2}>
            {party.title}
          </Text>
          <View style={styles.venueContainer}>
            <Ionicons 
              name="location-outline" 
              size={16} 
              color={!party.isAvailable ? "#999" : "#666"} 
            />
            <Text style={[
              styles.venueName,
              !party.isAvailable && styles.venueNameSoldOut
            ]}>
              {party.venueName}
            </Text>
          </View>
        </View>

        <Text style={[
          styles.description,
          !party.isAvailable && styles.descriptionSoldOut
        ]} numberOfLines={2}>
          {party.description}
        </Text>

        <View style={styles.timeContainer}>
          <Ionicons 
            name="time-outline" 
            size={16} 
            color={!party.isAvailable ? "#999" : "#666"} 
          />
          <Text style={[
            styles.timeText,
            !party.isAvailable && styles.timeTextSoldOut
          ]}>
            {party.startTime} - {party.endTime}
          </Text>
        </View>

        <View style={styles.tagsContainer}>
          {party.tags.slice(0, 3).map((tag, index) => (
            <View key={index} style={[
              styles.tag,
              !party.isAvailable && styles.tagSoldOut
            ]}>
              <Text style={[
                styles.tagText,
                !party.isAvailable && styles.tagTextSoldOut
              ]}>
                {tag}
              </Text>
            </View>
          ))}
        </View>

        <View style={styles.footer}>
          {!party.isAvailable ? (
            <View style={styles.soldOutBadge}>
              <Text style={styles.soldOutBadgeText}>EVENTO AGOTADO</Text>
            </View>
          ) : (
            <>
              <View style={styles.availabilityContainer}>
                <View 
                  style={[
                    styles.availabilityDot, 
                    { backgroundColor: getAvailabilityColor() }
                  ]} 
                />
                <Text style={styles.availabilityText}>
                  {getAvailabilityText()}
                </Text>
              </View>
              
              <TouchableOpacity 
                style={styles.buyButton}
                onPress={handleBuyTickets}
              >
                <Ionicons name="ticket-outline" size={16} color="#fff" />
                <Text style={styles.buyButtonText}>Comprar</Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
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
  containerSoldOut: {
    backgroundColor: '#f5f5f5',
    opacity: 0.7,
  },
  imageContainer: {
    position: 'relative',
  },
  image: {
    width: '100%',
    height: 200,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  priceTag: {
    position: 'absolute',
    top: 12,
    right: 12,
    backgroundColor: '#6366f1',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  priceText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  overlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 60,
    backgroundColor: 'rgba(0,0,0,0.2)',
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  soldOutOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'center',
    alignItems: 'center',
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  soldOutText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  content: {
    padding: 16,
  },
  header: {
    marginBottom: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 4,
  },
  venueContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  venueName: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  description: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
    marginBottom: 12,
  },
  timeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  timeText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 16,
  },
  tag: {
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 8,
    marginBottom: 4,
  },
  tagText: {
    fontSize: 12,
    color: '#6b7280',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  availabilityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  availabilityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  availabilityText: {
    fontSize: 12,
    color: '#6b7280',
  },
  buyButton: {
    backgroundColor: '#6366f1',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  buyButtonText: {
    color: '#fff',
    fontWeight: '600',
    marginLeft: 4,
  },
  // Estilos para eventos agotados
  imageSoldOut: {
    opacity: 0.5,
  },
  priceTagSoldOut: {
    backgroundColor: '#999',
  },
  priceTextSoldOut: {
    color: '#fff',
  },
  contentSoldOut: {
    backgroundColor: '#f9f9f9',
  },
  titleSoldOut: {
    color: '#999',
  },
  venueNameSoldOut: {
    color: '#bbb',
  },
  descriptionSoldOut: {
    color: '#aaa',
  },
  timeTextSoldOut: {
    color: '#bbb',
  },
  tagSoldOut: {
    backgroundColor: '#e5e5e5',
  },
  tagTextSoldOut: {
    color: '#999',
  },
  soldOutBadge: {
    backgroundColor: '#fee2e2',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    alignSelf: 'flex-start',
  },
  soldOutBadgeText: {
    color: '#dc2626',
    fontWeight: 'bold',
    fontSize: 12,
  },
}); 