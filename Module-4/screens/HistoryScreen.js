import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView, Image, Animated } from 'react-native';
import { COLORS, FONTS, SPACING, SHADOWS, BORDER_RADIUS } from '../constants/theme';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

const historyData = [
  {
    id: 1,
    building: 'Main Academic Block',
    timestamp: '2 hours ago',
    distance: '10m',
    accuracy: '95%',
    gradient: ['#4CAF50', '#2E7D32'],
    icon: 'account-balance',
  },
  {
    id: 2,
    building: 'Library',
    timestamp: '4 hours ago',
    distance: '50m',
    accuracy: '92%',
    gradient: ['#2196F3', '#1976D2'],
    icon: 'local-library',
  },
  {
    id: 3,
    building: 'Cafeteria',
    timestamp: 'Yesterday',
    distance: '100m',
    accuracy: '88%',
    gradient: ['#FF9800', '#F57C00'],
    icon: 'restaurant',
  },
];

const HistoryScreen = () => {
  const [selectedItem, setSelectedItem] = useState(null);

  const renderHistoryItem = (item, index) => {
    const isSelected = selectedItem?.id === item.id;

    return (
      <TouchableOpacity
        key={item.id}
        style={[
          styles.historyItem,
          isSelected && styles.historyItemSelected,
        ]}
        onPress={() => setSelectedItem(isSelected ? null : item)}
        activeOpacity={0.8}
      >
        <LinearGradient
          colors={item.gradient}
          style={styles.historyContent}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.historyHeader}>
            <View style={styles.iconContainer}>
              <MaterialIcons name={item.icon} size={28} color={COLORS.background} />
            </View>
            <View style={styles.headerInfo}>
              <Text style={styles.buildingName}>{item.building}</Text>
              <Text style={styles.timestamp}>{item.timestamp}</Text>
            </View>
            <MaterialIcons 
              name={isSelected ? 'keyboard-arrow-up' : 'keyboard-arrow-down'} 
              size={24} 
              color={COLORS.background} 
            />
          </View>

          {isSelected && (
            <View style={styles.detailsContainer}>
              <View style={styles.detailRow}>
                <View style={styles.detail}>
                  <MaterialIcons name="place" size={20} color={COLORS.background} />
                  <Text style={styles.detailText}>Distance: {item.distance}</Text>
                </View>
                <View style={styles.detail}>
                  <MaterialIcons name="verified" size={20} color={COLORS.background} />
                  <Text style={styles.detailText}>Accuracy: {item.accuracy}</Text>
                </View>
              </View>
              <TouchableOpacity style={styles.actionButton}>
                <MaterialIcons name="navigation" size={20} color={COLORS.background} />
                <Text style={styles.actionButtonText}>Navigate Again</Text>
              </TouchableOpacity>
            </View>
          )}
        </LinearGradient>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[COLORS.primary, '#FFA500']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.headerTitle}>History</Text>
        <Text style={styles.headerSubtitle}>Your Recent Locations</Text>
      </LinearGradient>

      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {historyData.map((item, index) => renderHistoryItem(item, index))}
      </ScrollView>

      <TouchableOpacity style={styles.clearButton}>
        <MaterialIcons name="delete-outline" size={24} color={COLORS.error} />
        <Text style={styles.clearButtonText}>Clear History</Text>
      </TouchableOpacity>
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
  scrollView: {
    flex: 1,
  },
  content: {
    padding: SPACING.lg,
  },
  historyItem: {
    marginBottom: SPACING.md,
    borderRadius: BORDER_RADIUS.lg,
    ...SHADOWS.medium,
    overflow: 'hidden',
  },
  historyContent: {
    padding: SPACING.lg,
  },
  historyHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: BORDER_RADIUS.lg,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerInfo: {
    flex: 1,
    marginLeft: SPACING.md,
  },
  buildingName: {
    fontSize: FONTS.sizes.md,
    fontWeight: 'bold',
    color: COLORS.background,
    marginBottom: SPACING.xs,
  },
  timestamp: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.background,
    opacity: 0.9,
  },
  detailsContainer: {
    marginTop: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.2)',
    paddingTop: SPACING.lg,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.md,
  },
  detail: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  detailText: {
    marginLeft: SPACING.xs,
    fontSize: FONTS.sizes.sm,
    color: COLORS.background,
    opacity: 0.9,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
  },
  actionButtonText: {
    marginLeft: SPACING.sm,
    fontSize: FONTS.sizes.md,
    fontWeight: 'bold',
    color: COLORS.background,
  },
  clearButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  clearButtonText: {
    marginLeft: SPACING.sm,
    fontSize: FONTS.sizes.md,
    color: COLORS.error,
  },
});

export default HistoryScreen; 