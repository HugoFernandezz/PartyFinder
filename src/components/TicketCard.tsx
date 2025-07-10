import React, { useRef } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  Animated,
  Linking
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { TicketType } from '../types';

interface TicketCardProps {
  ticket: TicketType;
}

export const TicketCard: React.FC<TicketCardProps> = ({ ticket }) => {
  const scaleValue = useRef(new Animated.Value(1)).current;

  const isAvailable = ticket.isAvailable && !ticket.isSoldOut;
  const hasFewLeft = ticket.fewLeft && isAvailable;
  const isClickable = isAvailable && !!ticket.purchaseUrl;

  const handlePressIn = () => {
    if (!isClickable) return;
    Animated.spring(scaleValue, {
      toValue: 0.98,
      useNativeDriver: true,
    }).start();
  };

  const handlePressOut = () => {
    if (!isClickable) return;
    Animated.spring(scaleValue, {
      toValue: 1,
      friction: 3,
      tension: 40,
      useNativeDriver: true,
    }).start();
  };

  const handlePress = () => {
    if (!isClickable) return;
    
    // Abrir el link inmediatamente, sin esperar la animación
    if (ticket.purchaseUrl) {
      Linking.openURL(ticket.purchaseUrl);
    }
  };

  return (
    <Animated.View style={{ transform: [{ scale: scaleValue }] }}>
      <TouchableOpacity
        key={ticket.id}
        style={[
          styles.ticketTypeCard,
          hasFewLeft && styles.ticketTypeCardFewLeft,
          !isAvailable && styles.ticketTypeCardSoldOut,
        ]}
        onPress={handlePress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        disabled={!isClickable}
        activeOpacity={1} // Usamos nuestra propia animación, no la de opacidad
      >
        <View style={styles.ticketTypeContent}>
          <View style={styles.ticketTypeHeader}>
            <View style={styles.ticketTypeInfo}>
              <Text style={[styles.ticketTypeName, !isAvailable && styles.ticketTypeNameDisabled]}>
                {ticket.name}
              </Text>
              
              <View style={styles.badgesContainer}>
                {ticket.isPromotion && (
                  <View style={styles.promotionBadge}>
                    <Ionicons name="flash" size={12} color="#d97706" />
                    <Text style={styles.promotionText}>PROMOCIÓN</Text>
                  </View>
                )}
                {ticket.isVip && (
                  <View style={styles.vipBadge}>
                    <Ionicons name="star" size={12} color="#7c3aed" />
                    <Text style={styles.vipText}>VIP</Text>
                  </View>
                )}
                {hasFewLeft && (
                  <View style={styles.fewLeftBadge}>
                    <Ionicons name="warning" size={12} color="#d97706" />
                    <Text style={styles.fewLeftText}>¡ÚLTIMAS!</Text>
                  </View>
                )}
              </View>
            </View>
            
            <View style={styles.priceSection}>
              <Text style={[styles.ticketTypePrice, !isAvailable && styles.ticketTypePriceDisabled]}>
                {ticket.price}€
              </Text>
            </View>
          </View>
          
          {ticket.description && (
            <Text style={[styles.ticketTypeDescription, !isAvailable && styles.ticketTypeDescriptionDisabled]}>
              {ticket.description}
            </Text>
          )}
          
          {ticket.restrictions && (
            <Text style={styles.ticketTypeRestrictions}>
              <Ionicons name="information-circle" size={12} color="#f59e0b" />
              {' '}{ticket.restrictions}
            </Text>
          )}
        </View>
        
        <View style={[styles.ticketActionContainer, hasFewLeft && styles.ticketActionContainerFewLeft, !isAvailable && styles.ticketActionContainerSoldOut]}>
          {isAvailable ? (
            <View style={styles.soldOutActionContent}>
              <Ionicons name={hasFewLeft ? "flash" : "card"} size={20} color="#fff" />
              <Text style={styles.ticketActionText}>{hasFewLeft ? "¡Comprar Ahora!" : "Comprar Entrada"}</Text>
            </View>
          ) : (
            <View style={styles.soldOutActionContent}>
              <Ionicons name="close-circle" size={20} color="#94a3b8" />
              <Text style={styles.ticketActionTextDisabled}>Agotado</Text>
            </View>
          )}
        </View>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Copiaremos los estilos exactos de EventDetailScreen
const styles = StyleSheet.create({
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
    paddingVertical: 12,
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
}); 