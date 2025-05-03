import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, FlatList, TextInput, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { Card, Icon } from 'react-native-elements';
import * as SecureStore from 'expo-secure-store';

const BuildingDirectoryScreen = () => {
  const navigation = useNavigation();
  const [searchQuery, setSearchQuery] = useState('');
  const [buildings, setBuildings] = useState([]);
  const [filteredBuildings, setFilteredBuildings] = useState([]);
  const [favorites, setFavorites] = useState(new Set());

  useEffect(() => {
    loadBuildings();
    loadFavorites();
  }, []);

  const loadBuildings = async () => {
    try {
      // Replace with your actual API endpoint
      const response = await fetch('http://your-api/buildings');
      const data = await response.json();
      setBuildings(data);
      setFilteredBuildings(data);
    } catch (error) {
      console.error('Error loading buildings:', error);
    }
  };

  const loadFavorites = async () => {
    try {
      const favs = await SecureStore.getItemAsync('favoriteBuildings');
      if (favs) {
        setFavorites(new Set(JSON.parse(favs)));
      }
    } catch (error) {
      console.error('Error loading favorites:', error);
    }
  };

  const handleSearch = (text) => {
    setSearchQuery(text);
    const filtered = buildings.filter(building =>
      building.name.toLowerCase().includes(text.toLowerCase()) ||
      building.description.toLowerCase().includes(text.toLowerCase())
    );
    setFilteredBuildings(filtered);
  };

  const toggleFavorite = async (buildingId) => {
    const newFavorites = new Set(favorites);
    if (newFavorites.has(buildingId)) {
      newFavorites.delete(buildingId);
    } else {
      newFavorites.add(buildingId);
    }
    setFavorites(newFavorites);
    await SecureStore.setItemAsync('favoriteBuildings', JSON.stringify([...newFavorites]));
  };

  const renderBuilding = ({ item }) => (
    <Card containerStyle={styles.card}>
      <View style={styles.cardHeader}>
        <Text style={styles.buildingName}>{item.name}</Text>
        <TouchableOpacity onPress={() => toggleFavorite(item.id)}>
          <Icon
            name={favorites.has(item.id) ? 'favorite' : 'favorite-border'}
            color={favorites.has(item.id) ? '#FF3B30' : '#666'}
            size={24}
          />
        </TouchableOpacity>
      </View>
      <Text style={styles.buildingDescription}>{item.description}</Text>
      <View style={styles.buildingDetails}>
        <Text style={styles.detailText}>📍 {item.location}</Text>
        <Text style={styles.detailText}>🕒 {item.hours}</Text>
      </View>
      <TouchableOpacity
        style={styles.viewButton}
        onPress={() => navigation.navigate('BuildingDetails', { building: item })}
      >
        <Text style={styles.viewButtonText}>View Details</Text>
      </TouchableOpacity>
    </Card>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Icon name="search" size={20} color="#666" />
        <TextInput
          style={styles.searchInput}
          placeholder="Search buildings..."
          value={searchQuery}
          onChangeText={handleSearch}
        />
      </View>

      <View style={styles.filterContainer}>
        <TouchableOpacity style={styles.filterButton}>
          <Text style={styles.filterText}>All Buildings</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.filterButton}>
          <Text style={styles.filterText}>Favorites</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.filterButton}>
          <Text style={styles.filterText}>Nearby</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={filteredBuildings}
        renderItem={renderBuilding}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.list}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 10,
    margin: 10,
    borderRadius: 10,
    elevation: 2,
  },
  searchInput: {
    flex: 1,
    marginLeft: 10,
    fontSize: 16,
  },
  filterContainer: {
    flexDirection: 'row',
    padding: 10,
    justifyContent: 'space-around',
  },
  filterButton: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: '#fff',
    elevation: 2,
  },
  filterText: {
    color: '#007AFF',
    fontWeight: 'bold',
  },
  list: {
    padding: 10,
  },
  card: {
    borderRadius: 10,
    marginBottom: 10,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  buildingName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  buildingDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  buildingDetails: {
    marginBottom: 15,
  },
  detailText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 5,
  },
  viewButton: {
    backgroundColor: '#007AFF',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  viewButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default BuildingDirectoryScreen; 