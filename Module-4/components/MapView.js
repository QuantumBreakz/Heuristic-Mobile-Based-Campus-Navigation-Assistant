import React from 'react';
import { StyleSheet, View, Dimensions } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { Text } from 'react-native-elements';

const MapView = ({ userLocation, capturedImage }) => {
  // Default map region (replace with your campus coordinates)
  const defaultRegion = {
    latitude: 37.7749,
    longitude: -122.4194,
    latitudeDelta: 0.01,
    longitudeDelta: 0.01,
  };

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={defaultRegion}
        region={userLocation ? {
          latitude: userLocation.coordinates.latitude,
          longitude: userLocation.coordinates.longitude,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        } : defaultRegion}
      >
        {userLocation && (
          <Marker
            coordinate={{
              latitude: userLocation.coordinates.latitude,
              longitude: userLocation.coordinates.longitude,
            }}
            title="Your Location"
            description={`Building: ${userLocation.building}\nDistance: ${userLocation.distance}m`}
          />
        )}
      </MapView>
      {userLocation && (
        <View style={styles.infoContainer}>
          <Text h4>Location Information</Text>
          <Text>Building: {userLocation.building}</Text>
          <Text>Distance: {userLocation.distance} meters</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 20,
  },
  map: {
    width: Dimensions.get('window').width - 40,
    height: 300,
    borderRadius: 10,
  },
  infoContainer: {
    marginTop: 10,
    padding: 10,
    backgroundColor: '#f0f0f0',
    borderRadius: 10,
  },
});

export default MapView; 