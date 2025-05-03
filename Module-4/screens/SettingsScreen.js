import React, { useState } from 'react';
import { StyleSheet, View, Text, Switch, TouchableOpacity } from 'react-native';
import { ListItem } from 'react-native-elements';
import * as SecureStore from 'expo-secure-store';

const SettingsScreen = () => {
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [mapType, setMapType] = useState('standard');

  const handleClearHistory = async () => {
    try {
      await SecureStore.deleteItemAsync('locationHistory');
      // Show success message or update UI
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await SecureStore.deleteItemAsync('userToken');
      // Navigate to login screen or handle logout
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Settings</Text>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferences</Text>
        <ListItem bottomDivider>
          <ListItem.Content>
            <ListItem.Title>Enable Notifications</ListItem.Title>
          </ListItem.Content>
          <Switch
            value={notifications}
            onValueChange={setNotifications}
          />
        </ListItem>
        <ListItem bottomDivider>
          <ListItem.Content>
            <ListItem.Title>Dark Mode</ListItem.Title>
          </ListItem.Content>
          <Switch
            value={darkMode}
            onValueChange={setDarkMode}
          />
        </ListItem>
        <ListItem bottomDivider>
          <ListItem.Content>
            <ListItem.Title>Map Type</ListItem.Title>
          </ListItem.Content>
          <ListItem.Title style={styles.mapTypeText}>
            {mapType.charAt(0).toUpperCase() + mapType.slice(1)}
          </ListItem.Title>
        </ListItem>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Data</Text>
        <TouchableOpacity
          style={styles.button}
          onPress={handleClearHistory}
        >
          <Text style={styles.buttonText}>Clear Location History</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>
        <TouchableOpacity
          style={[styles.button, styles.logoutButton]}
          onPress={handleLogout}
        >
          <Text style={[styles.buttonText, styles.logoutText]}>Logout</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#333',
  },
  section: {
    marginBottom: 30,
    backgroundColor: '#fff',
    borderRadius: 10,
    overflow: 'hidden',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    padding: 15,
    color: '#333',
    backgroundColor: '#f0f0f0',
  },
  button: {
    backgroundColor: '#fff',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  buttonText: {
    fontSize: 16,
    color: '#007AFF',
  },
  logoutButton: {
    backgroundColor: '#fff',
  },
  logoutText: {
    color: '#FF3B30',
  },
  mapTypeText: {
    color: '#666',
  },
});

export default SettingsScreen; 