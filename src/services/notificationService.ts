import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getFirestore, collection, doc, setDoc, getDocs, query, where, deleteDoc } from 'firebase/firestore';
import { db } from './firebase';
import { Party } from '../types';
import { NotificationAlert } from '../types/notifications';

const EVENTS_SNAPSHOT_KEY = '@partyfinder_events_snapshot';
const ALERT_EVENTS_SNAPSHOT_KEY = '@partyfinder_alert_events_snapshot'; // Para guardar eventos por alerta
const FCM_TOKEN_KEY = '@partyfinder_fcm_token';

// Configure notification behavior
Notifications.setNotificationHandler({
    handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: false,
        shouldShowBanner: true,
        shouldShowList: true,
    }),
});

export const notificationService = {
    // Request notification permissions and get FCM token
    async requestPermissions(): Promise<string | null> {
        if (!Device.isDevice) {
            console.log('Must use physical device for Push Notifications');
            return null;
        }

        const { status: existingStatus } = await Notifications.getPermissionsAsync();
        let finalStatus = existingStatus;

        if (existingStatus !== 'granted') {
            const { status } = await Notifications.requestPermissionsAsync();
            finalStatus = status;
        }

        if (finalStatus !== 'granted') {
            console.log('Failed to get push token for push notification!');
            return null;
        }

        // Configure Android channel
        if (Platform.OS === 'android') {
            await Notifications.setNotificationChannelAsync('default', {
                name: 'default',
                importance: Notifications.AndroidImportance.MAX,
                vibrationPattern: [0, 250, 250, 250],
                lightColor: '#FF231F7C',
            });
        }

        // Get FCM token (Expo Push Token)
        try {
            // Get projectId from app.json (expo.extra.eas.projectId)
            const projectId = Constants.expoConfig?.extra?.eas?.projectId;
            
            if (!projectId || projectId === 'REEMPLAZA_CON_TU_UUID_DE_EXPO') {
                console.error('❌ Error: projectId de Expo no configurado correctamente.');
                console.error('📋 Para obtener tu projectId:');
                console.error('   1. Ve a https://expo.dev y crea un nuevo proyecto');
                console.error('   2. O ejecuta: npx eas init');
                console.error('   3. Copia el UUID del proyecto y reemplázalo en app.json');
                console.error('   4. El projectId debe ser un UUID (ej: a1b2c3d4-e5f6-7890-abcd-ef1234567890)');
                return null;
            }

            const tokenData = await Notifications.getExpoPushTokenAsync({
                projectId: projectId,
            });
            const token = tokenData.data;
            
            // Save token locally
            await AsyncStorage.setItem(FCM_TOKEN_KEY, token);
            
            return token;
        } catch (error) {
            console.error('Error getting Expo push token:', error);
            return null;
        }
    },

    // Get stored FCM token
    async getStoredToken(): Promise<string | null> {
        try {
            return await AsyncStorage.getItem(FCM_TOKEN_KEY);
        } catch (error) {
            console.error('Error getting stored token:', error);
            return null;
        }
    },

    // Register device token for an alert in Firebase
    async registerAlertToken(alertId: string, token: string): Promise<void> {
        try {
            const alertsRef = collection(db, 'alert_tokens');
            await setDoc(doc(alertsRef, `${alertId}_${token}`), {
                alertId,
                token,
                platform: Platform.OS,
                registeredAt: new Date().toISOString(),
            });
        } catch (error: any) {
            // Silently fail - tokens can't be registered due to Firestore security rules
            // This doesn't affect local notifications functionality
            if (error?.code !== 'permission-denied') {
                console.error('Error registering alert token:', error);
            }
        }
    },

    // Unregister device token for an alert
    async unregisterAlertToken(alertId: string, token: string): Promise<void> {
        try {
            const alertsRef = collection(db, 'alert_tokens');
            await deleteDoc(doc(alertsRef, `${alertId}_${token}`));
        } catch (error) {
            console.error('Error unregistering alert token:', error);
        }
    },

    // Unregister all tokens for an alert (when alert is deleted)
    async unregisterAllAlertTokens(alertId: string): Promise<void> {
        try {
            const alertsRef = collection(db, 'alert_tokens');
            const q = query(alertsRef, where('alertId', '==', alertId));
            const snapshot = await getDocs(q);
            
            const deletePromises = snapshot.docs.map(doc => deleteDoc(doc.ref));
            await Promise.all(deletePromises);
        } catch (error: any) {
            // Silently fail - tokens will remain in Firestore but won't cause issues
            // This happens because Firestore security rules don't allow client-side deletion
            // The tokens are harmless if left in the database
            if (error?.code !== 'permission-denied') {
                console.error('Error unregistering all alert tokens:', error);
            }
        }
    },

    // Show a local notification
    async showNotification(title: string, body: string, data?: any): Promise<void> {
        await Notifications.scheduleNotificationAsync({
            content: {
                title,
                body,
                data: data || {},
                sound: true,
            },
            trigger: null, // Show immediately
        });
    },

    // Save current events snapshot for comparison
    async saveEventsSnapshot(events: Party[]): Promise<void> {
        try {
            const snapshot = events.map(e => ({
                id: e.id,
                date: e.date,
                venueName: e.venueName,
                title: e.title,
            }));
            await AsyncStorage.setItem(EVENTS_SNAPSHOT_KEY, JSON.stringify(snapshot));
        } catch (error) {
            console.error('Error saving events snapshot:', error);
        }
    },

    // Get previous events snapshot
    async getEventsSnapshot(): Promise<{ id: string; date: string; venueName: string; title: string }[]> {
        try {
            const stored = await AsyncStorage.getItem(EVENTS_SNAPSHOT_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error getting events snapshot:', error);
            return [];
        }
    },

    // Save events snapshot for a specific alert (when alert is created)
    async saveAlertEventsSnapshot(alertId: string, events: Party[]): Promise<void> {
        try {
            const snapshot = events.map(e => ({
                id: e.id,
                date: e.date,
                venueName: e.venueName,
                title: e.title,
            }));
            const key = `${ALERT_EVENTS_SNAPSHOT_KEY}_${alertId}`;
            await AsyncStorage.setItem(key, JSON.stringify(snapshot));
        } catch (error) {
            console.error('Error saving alert events snapshot:', error);
        }
    },

    // Get events snapshot for a specific alert
    async getAlertEventsSnapshot(alertId: string): Promise<{ id: string; date: string; venueName: string; title: string }[]> {
        try {
            const key = `${ALERT_EVENTS_SNAPSHOT_KEY}_${alertId}`;
            const stored = await AsyncStorage.getItem(key);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error getting alert events snapshot:', error);
            return [];
        }
    },

    // Delete events snapshot for a specific alert (when alert is deleted)
    async deleteAlertEventsSnapshot(alertId: string): Promise<void> {
        try {
            const key = `${ALERT_EVENTS_SNAPSHOT_KEY}_${alertId}`;
            await AsyncStorage.removeItem(key);
        } catch (error) {
            console.error('Error deleting alert events snapshot:', error);
        }
    },

    // Check for new events and trigger notifications
    async checkForNewEvents(
        currentEvents: Party[],
        alerts: NotificationAlert[]
    ): Promise<void> {
        if (alerts.length === 0) return;

        // Check each alert individually
        const enabledAlerts = alerts.filter(a => a.enabled);

        for (const alert of enabledAlerts) {
            // Get the snapshot of events that existed when this alert was created
            const alertSnapshot = await this.getAlertEventsSnapshot(alert.id);
            
            // If alert was just created (snapshot doesn't exist yet), save current events as snapshot and skip notification
            // This prevents immediate notifications when creating an alert for a date that already has events
            if (alertSnapshot.length === 0) {
                // Find events that match this alert's criteria
                const matchingEvents = currentEvents.filter(event => {
                    const dateMatches = event.date === alert.date;
                    const venueMatches = !alert.venueName ||
                        event.venueName.toLowerCase().includes(alert.venueName.toLowerCase());
                    return dateMatches && venueMatches;
                });
                
                // Save snapshot for future checks (but don't notify now)
                await this.saveAlertEventsSnapshot(alert.id, matchingEvents);
                continue; // Skip to next alert
            }
            
            const alertSnapshotIds = new Set(alertSnapshot.map(e => e.id));

            // Find events that match this alert's criteria
            const matchingEvents = currentEvents.filter(event => {
                const dateMatches = event.date === alert.date;
                const venueMatches = !alert.venueName ||
                    event.venueName.toLowerCase().includes(alert.venueName.toLowerCase());
                return dateMatches && venueMatches;
            });

            // Find NEW events (that weren't in the snapshot when alert was created)
            const newEventsForAlert = matchingEvents.filter(event => !alertSnapshotIds.has(event.id));

            // Notify for each new event
            for (const event of newEventsForAlert) {
                // Format notification - usar parseLocalDate para evitar problemas de zona horaria
                const parseLocalDate = (dateStr: string): Date => {
                    const [year, month, day] = dateStr.split('-').map(Number);
                    return new Date(year, month - 1, day);
                };
                const formattedDate = parseLocalDate(event.date).toLocaleDateString('es-ES', {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long',
                });

                await this.showNotification(
                    `🎉 ¡${event.venueName} ya sacó entradas!`,
                    `${event.venueName} - ${formattedDate} - ${event.title}`,
                    { eventId: event.id }
                );
            }

            // Update the snapshot for this alert with current matching events
            await this.saveAlertEventsSnapshot(alert.id, matchingEvents);
        }

        // Still maintain global snapshot for backward compatibility
        await this.saveEventsSnapshot(currentEvents);
    },
};
