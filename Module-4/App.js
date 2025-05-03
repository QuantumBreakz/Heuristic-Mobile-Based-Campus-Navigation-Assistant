import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, FONTS, SPACING, SHADOWS, BORDER_RADIUS } from './constants/theme';
import SplashScreen from './screens/SplashScreen';
import HomeScreen from './screens/HomeScreen';

// Enable screens for web
import { enableScreens } from 'react-native-screens';
enableScreens();

// Simple Home Screen Component
const PlaceholderScreen = ({ route }) => (
  <View style={styles.container}>
    <Text style={styles.title}>{route.name}</Text>
    <Text style={styles.subtitle}>Coming Soon</Text>
  </View>
);

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Splash"
        screenOptions={{
          headerStyle: {
            backgroundColor: COLORS.primary,
          },
          headerTintColor: COLORS.card,
          headerTitleStyle: {
            fontWeight: 'bold',
          },
          animation: 'slide_from_right',
        }}
      >
        <Stack.Screen 
          name="Splash" 
          component={SplashScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Camera" 
          component={PlaceholderScreen}
          options={{ headerShown: true, title: 'Capture Image' }}
        />
        <Stack.Screen 
          name="Map" 
          component={PlaceholderScreen}
          options={{ headerShown: true, title: 'Campus Map' }}
        />
        <Stack.Screen 
          name="History" 
          component={PlaceholderScreen}
          options={{ headerShown: true, title: 'History' }}
        />
        <Stack.Screen 
          name="Help" 
          component={PlaceholderScreen}
          options={{ headerShown: true, title: 'Help & About' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: SPACING.xl,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: FONTS.sizes.xxxl,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginBottom: SPACING.xxl,
  },
  subtitle: {
    fontSize: FONTS.sizes.lg,
    color: COLORS.textSecondary,
    marginTop: SPACING.md,
  },
  buttonContainer: {
    width: '100%',
    maxWidth: 400,
  },
  button: {
    backgroundColor: COLORS.primary,
    padding: SPACING.lg,
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.md,
    ...SHADOWS.medium,
  },
  buttonText: {
    color: COLORS.card,
    fontSize: FONTS.sizes.lg,
    fontWeight: 'bold',
    textAlign: 'center',
  },
}); 