import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

export const ProfileScreen: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Mi Perfil</Text>
          <Text style={styles.subtitle}>
            Gestiona tu cuenta y preferencias
          </Text>
        </View>

        {/* Placeholder para avatar */}
        <View style={styles.avatarContainer}>
          <View style={styles.avatar}>
            <Ionicons name="person" size={60} color="#6366f1" />
          </View>
          <Text style={styles.userName}>Usuario</Text>
          <Text style={styles.userEmail}>usuario@ejemplo.com</Text>
        </View>

        {/* Opciones del menú */}
        <View style={styles.menuContainer}>
          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuItemLeft}>
              <Ionicons name="heart-outline" size={24} color="#6366f1" />
              <Text style={styles.menuItemText}>Eventos Favoritos</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuItemLeft}>
              <Ionicons name="ticket-outline" size={24} color="#6366f1" />
              <Text style={styles.menuItemText}>Mis Entradas</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuItemLeft}>
              <Ionicons name="notifications-outline" size={24} color="#6366f1" />
              <Text style={styles.menuItemText}>Notificaciones</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuItemLeft}>
              <Ionicons name="settings-outline" size={24} color="#6366f1" />
              <Text style={styles.menuItemText}>Configuración</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem}>
            <View style={styles.menuItemLeft}>
              <Ionicons name="help-circle-outline" size={24} color="#6366f1" />
              <Text style={styles.menuItemText}>Ayuda y Soporte</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
          </TouchableOpacity>
        </View>

        {/* Información de la app */}
        <View style={styles.appInfo}>
          <Text style={styles.appInfoText}>PartyFinder Murcia v1.0.0</Text>
          <Text style={styles.appInfoSubtext}>
            Descubre la mejor vida nocturna de Murcia
          </Text>
        </View>

        {/* Mensaje de desarrollo */}
        <View style={styles.developmentBanner}>
          <Ionicons name="construct-outline" size={20} color="#f59e0b" />
          <Text style={styles.developmentText}>
            Esta sección está en desarrollo. Próximamente podrás gestionar tu perfil, 
            ver tus eventos favoritos y mucho más.
          </Text>
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
  avatarContainer: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#fff',
    marginTop: 1,
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  userName: {
    fontSize: 24,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 16,
    color: '#6b7280',
  },
  menuContainer: {
    backgroundColor: '#fff',
    marginTop: 20,
    paddingVertical: 8,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f3f4f6',
  },
  menuItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  menuItemText: {
    fontSize: 16,
    color: '#1f2937',
    marginLeft: 12,
  },
  appInfo: {
    alignItems: 'center',
    padding: 30,
  },
  appInfoText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 4,
  },
  appInfoSubtext: {
    fontSize: 14,
    color: '#9ca3af',
    textAlign: 'center',
  },
  developmentBanner: {
    flexDirection: 'row',
    backgroundColor: '#fef3c7',
    margin: 20,
    padding: 16,
    borderRadius: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#f59e0b',
  },
  developmentText: {
    flex: 1,
    fontSize: 14,
    color: '#92400e',
    marginLeft: 8,
    lineHeight: 20,
  },
}); 