import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Dimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Party } from '../types';

const { width } = Dimensions.get('window');

interface PartyCardProps {
  party: Party;
  onPress: () => void;
}

const getPartyImageSource = (party: Party) => {
  if (party.venueName.toUpperCase() === 'MACCÄO OPEN AIR CLUB') {
    return require('../../assets/Maccao.jpeg'); 
  }
  return { uri: party.imageUrl };
};

export const PartyCard: React.FC<PartyCardProps> = ({ party, onPress }) => {
  const isSoldOut = !party.isAvailable;
  const hasFewLeft = party.fewLeft && !isSoldOut;

  return (
    <TouchableOpacity 
      style={styles.card} 
      onPress={onPress}
    >
      <View style={styles.imageContainer}>
        <Image
          source={getPartyImageSource(party)}
          style={styles.image}
        />
        
        {isSoldOut && (
          <View style={styles.soldOutOverlay}>
            <Ionicons name="eye-off-outline" size={28} color="rgba(255, 255, 255, 0.8)" />
            <Text style={styles.soldOutText}>AGOTADO</Text>
          </View>
        )}
        
        {hasFewLeft && (
          <View style={styles.fewLeftBadge}>
            <Ionicons name="warning" size={18} color="#fff" />
          </View>
        )}
      </View>
      
      <View style={styles.content}>
        <Text style={styles.title} numberOfLines={1}>{party.title}</Text>
        <Text style={styles.venue}>{party.venueName}</Text>
        
        <View style={styles.infoRow}>
          <Ionicons name="calendar-outline" size={16} color="#6b7280" />
          <Text style={styles.infoText}>{new Date(party.date).toLocaleDateString('es-ES', { day: 'numeric', month: 'long' })}</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Ionicons name="time-outline" size={16} color="#6b7280" />
          <Text style={styles.infoText}>{party.startTime}</Text>
        </View>
        
        <View style={[
          styles.priceContainer,
          isSoldOut ? styles.soldOutPriceContainer : {},
          hasFewLeft ? styles.fewLeftPriceContainer : {},
        ]}>
          <Text style={styles.price}>
            {isSoldOut ? 'Agotado' : (party.price > 0 ? `${party.price}€` : 'GRATIS')}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  imageContainer: {
    position: 'relative',
  },
  image: {
    width: '100%',
    height: 180,
  },
  soldOutOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(31, 41, 55, 0.65)', // Un gris oscuro y elegante
    justifyContent: 'center',
    alignItems: 'center',
  },
  soldOutText: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 8,
    letterSpacing: 1,
  },
  fewLeftBadge: {
    position: 'absolute',
    top: 10,
    left: 10,
    backgroundColor: '#f59e0b',
    width: 30,
    height: 30,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4,
  },
  content: {
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 4,
  },
  venue: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 12,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  infoText: {
    fontSize: 14,
    color: '#374151',
    marginLeft: 8,
  },
  priceContainer: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    backgroundColor: '#6366f1',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  soldOutPriceContainer: {
    backgroundColor: '#ef4444',
  },
  fewLeftPriceContainer: {
    backgroundColor: '#f59e0b',
  },
  price: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
}); 