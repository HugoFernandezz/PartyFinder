import React from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { HomeScreen } from '../screens/HomeScreen';
import { EventDetailScreen } from '../screens/EventDetailScreen';
import { Party } from '../types';

// Crear un tema personalizado para forzar el fondo blanco
const MyTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: '#ffffff',
  },
};

export type RootStackParamList = {
  Home: undefined;
  EventDetail: { party: Party };
};

const Stack = createStackNavigator<RootStackParamList>();

export const Navigation: React.FC = () => {
  return (
    <NavigationContainer theme={MyTheme}>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="EventDetail" component={EventDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}; 