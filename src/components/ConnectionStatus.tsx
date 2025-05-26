import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { apiService } from '../services/api';

interface ConnectionStatusProps {
  style?: any;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ style }) => {
  const [status, setStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [serverInfo, setServerInfo] = useState<any>(null);

  const checkConnection = async () => {
    try {
      const response = await apiService.getServerStatus();
      if (response.success) {
        setStatus('connected');
        setServerInfo(response.data);
      } else {
        setStatus('disconnected');
        setServerInfo(null);
      }
    } catch (error) {
      setStatus('disconnected');
      setServerInfo(null);
    }
  };

  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000); // Verificar cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'connected': return '#4CAF50';
      case 'disconnected': return '#F44336';
      default: return '#FF9800';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected': 
        return serverInfo 
          ? `Servidor activo - ${serverInfo.events || 0} eventos`
          : 'Servidor conectado';
      case 'disconnected': return 'Servidor desconectado';
      default: return 'Verificando conexión...';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'connected': return 'checkmark-circle';
      case 'disconnected': return 'close-circle';
      default: return 'time';
    }
  };

  return (
    <View style={[styles.container, style, { backgroundColor: getStatusColor() + '20' }]}>
      <Ionicons 
        name={getStatusIcon()} 
        size={16} 
        color={getStatusColor()} 
      />
      <Text style={[styles.text, { color: getStatusColor() }]}>
        {getStatusText()}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginHorizontal: 16,
    marginBottom: 8,
  },
  text: {
    fontSize: 12,
    fontWeight: '500',
    marginLeft: 6,
  },
}); 