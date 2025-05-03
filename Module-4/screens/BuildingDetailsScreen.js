import React from 'react';
import { StyleSheet, View, Text, ScrollView, Image } from 'react-native';
import { Card, Button } from 'react-native-elements';
import MapView, { Marker } from 'react-native-maps';

const BuildingDetailsScreen = ({ route }) => {
  const { building } = route.params;

  return (
    <ScrollView style={styles.container}>
      <Card containerStyle={styles.card}>
        <Text style={styles.buildingName}>{building.building}</Text>
        
        <View style={styles.mapContainer}>
          <MapView
            style={styles.map}
            initialRegion={{
              latitude: building.coordinates.latitude,
              longitude: building.coordinates.longitude,
              latitudeDelta: 0.01,
              longitudeDelta: 0.01,
            }}
          >
            <Marker
              coordinate={{
                latitude: building.coordinates.latitude,
                longitude: building.coordinates.longitude,
              }}
              title={building.building}
            />
          </MapView>
        </View>

        <View style={styles.detailsContainer}>
          <Text style={styles.sectionTitle}>Location Details</Text>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Distance:</Text>
            <Text style={styles.detailValue}>{building.distance}m</Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Last Updated:</Text>
            <Text style={styles.detailValue}>{building.date}</Text>
          </View>
        </View>

        <View style={styles.actionsContainer}>
          <Button
            title="Get Directions"
            buttonStyle={styles.actionButton}
            onPress={() => {
              // Implement directions functionality
            }}
          />
          <Button
            title="View Building Information"
            buttonStyle={[styles.actionButton, styles.secondaryButton]}
            onPress={() => {
              // Implement building info functionality
            }}
          />
        </View>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    borderRadius: 10,
    margin: 10,
    padding: 15,
  },
  buildingName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#007AFF',
  },
  mapContainer: {
    height: 200,
    marginBottom: 20,
    borderRadius: 10,
    overflow: 'hidden',
  },
  map: {
    flex: 1,
  },
  detailsContainer: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  detailLabel: {
    fontSize: 16,
    color: '#666',
  },
  detailValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  actionsContainer: {
    marginTop: 10,
  },
  actionButton: {
    backgroundColor: '#007AFF',
    borderRadius: 10,
    marginBottom: 10,
  },
  secondaryButton: {
    backgroundColor: '#34C759',
  },
});

export default BuildingDetailsScreen; 