import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Dimensions, ScrollView } from 'react-native';
import { COLORS, FONTS, SPACING, SHADOWS, BORDER_RADIUS } from '../constants/theme';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

const buildings = [
  {
    name: 'Main Academic Block',
    description: 'Main teaching and administrative building',
    icon: 'account-balance',
    distance: '0m',
    gradient: ['#4CAF50', '#2E7D32'],
  },
  {
    name: 'Library',
    description: 'Central library and study area',
    icon: 'local-library',
    distance: '50m',
    gradient: ['#2196F3', '#1976D2'],
  },
  {
    name: 'Cafeteria',
    description: 'Student dining and recreation area',
    icon: 'restaurant',
    distance: '100m',
    gradient: ['#FF9800', '#F57C00'],
  },
  {
    name: 'Sports Complex',
    description: 'Indoor and outdoor sports facilities',
    icon: 'sports-basketball',
    distance: '150m',
    gradient: ['#9C27B0', '#7B1FA2'],
  },
  {
    name: 'Auditorium',
    description: 'Main event and ceremony hall',
    icon: 'event-seat',
    distance: '200m',
    gradient: ['#F44336', '#D32F2F'],
  },
];

const CampusMapScreen = () => {
  const [selectedBuilding, setSelectedBuilding] = useState(null);

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[COLORS.primary, '#FFA500']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.headerTitle}>Campus Map</Text>
        <Text style={styles.headerSubtitle}>Explore FAST-NUCES Lahore Campus</Text>
      </LinearGradient>

      <View style={styles.mapContainer}>
        <View style={styles.mapPlaceholder}>
          <MaterialIcons name="map" size={48} color={COLORS.textSecondary} />
          <Text style={styles.mapText}>Interactive Map Coming Soon</Text>
        </View>
      </View>

      <View style={styles.buildingsContainer}>
        <Text style={styles.sectionTitle}>Nearby Buildings</Text>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.buildingsList}
        >
          {buildings.map((building, index) => (
            <TouchableOpacity
              key={index}
              style={styles.buildingCard}
              onPress={() => setSelectedBuilding(building)}
              activeOpacity={0.8}
            >
              <LinearGradient
                colors={building.gradient}
                style={styles.buildingCardContent}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <MaterialIcons name={building.icon} size={32} color={COLORS.background} />
                <Text style={styles.buildingName}>{building.name}</Text>
                <Text style={styles.buildingDistance}>{building.distance}</Text>
              </LinearGradient>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {selectedBuilding && (
        <View style={styles.detailsCard}>
          <LinearGradient
            colors={selectedBuilding.gradient}
            style={styles.detailsContent}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <View style={styles.detailsHeader}>
              <MaterialIcons name={selectedBuilding.icon} size={40} color={COLORS.background} />
              <View style={styles.detailsTextContainer}>
                <Text style={styles.detailsTitle}>{selectedBuilding.name}</Text>
                <Text style={styles.detailsDescription}>{selectedBuilding.description}</Text>
              </View>
              <TouchableOpacity
                style={styles.closeButton}
                onPress={() => setSelectedBuilding(null)}
              >
                <MaterialIcons name="close" size={24} color={COLORS.background} />
              </TouchableOpacity>
            </View>
            <TouchableOpacity style={styles.directionsButton}>
              <MaterialIcons name="directions" size={24} color={COLORS.background} />
              <Text style={styles.directionsText}>Get Directions</Text>
            </TouchableOpacity>
          </LinearGradient>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    padding: SPACING.lg,
    borderBottomLeftRadius: BORDER_RADIUS.xl,
    borderBottomRightRadius: BORDER_RADIUS.xl,
    ...SHADOWS.medium,
  },
  headerTitle: {
    fontSize: FONTS.sizes.xl,
    fontWeight: 'bold',
    color: COLORS.background,
    marginBottom: SPACING.xs,
    textShadowColor: 'rgba(0, 0, 0, 0.2)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  headerSubtitle: {
    fontSize: FONTS.sizes.md,
    color: COLORS.background,
    opacity: 0.9,
  },
  mapContainer: {
    height: 200,
    margin: SPACING.lg,
    backgroundColor: COLORS.card,
    borderRadius: BORDER_RADIUS.lg,
    ...SHADOWS.medium,
    overflow: 'hidden',
  },
  mapPlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.card,
  },
  mapText: {
    marginTop: SPACING.sm,
    fontSize: FONTS.sizes.md,
    color: COLORS.textSecondary,
  },
  buildingsContainer: {
    padding: SPACING.lg,
  },
  sectionTitle: {
    fontSize: FONTS.sizes.lg,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  buildingsList: {
    paddingRight: SPACING.lg,
  },
  buildingCard: {
    width: 150,
    marginRight: SPACING.md,
    borderRadius: BORDER_RADIUS.lg,
    ...SHADOWS.medium,
    overflow: 'hidden',
  },
  buildingCardContent: {
    padding: SPACING.lg,
    alignItems: 'center',
    height: 160,
  },
  buildingName: {
    fontSize: FONTS.sizes.md,
    fontWeight: 'bold',
    color: COLORS.background,
    marginTop: SPACING.md,
    marginBottom: SPACING.xs,
    textAlign: 'center',
  },
  buildingDistance: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.background,
    opacity: 0.9,
  },
  detailsCard: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: SPACING.lg,
    backgroundColor: 'transparent',
  },
  detailsContent: {
    padding: SPACING.lg,
    borderRadius: BORDER_RADIUS.lg,
    ...SHADOWS.large,
  },
  detailsHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  detailsTextContainer: {
    flex: 1,
    marginLeft: SPACING.md,
  },
  detailsTitle: {
    fontSize: FONTS.sizes.lg,
    fontWeight: 'bold',
    color: COLORS.background,
    marginBottom: SPACING.xs,
  },
  detailsDescription: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.background,
    opacity: 0.9,
  },
  closeButton: {
    padding: SPACING.xs,
  },
  directionsButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    marginTop: SPACING.md,
  },
  directionsText: {
    fontSize: FONTS.sizes.md,
    fontWeight: 'bold',
    color: COLORS.background,
    marginLeft: SPACING.sm,
  },
});

export default CampusMapScreen; 