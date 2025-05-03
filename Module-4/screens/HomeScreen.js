import React, { useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, SafeAreaView, Image, Animated, Dimensions, ScrollView } from 'react-native';
import { COLORS, FONTS, SPACING, SHADOWS, BORDER_RADIUS } from '../constants/theme';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  const fadeAnim = new Animated.Value(0);
  const translateY = new Animated.Value(50);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.spring(translateY, {
        toValue: 0,
        tension: 20,
        friction: 7,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const menuItems = [
    {
      title: 'Capture Image',
      icon: 'camera-alt',
      screen: 'Camera',
      description: 'Take a photo to recognize campus buildings',
      color: '#FFD700',
      gradient: ['#FFD700', '#FFA000'],
    },
    {
      title: 'Campus Map',
      icon: 'map',
      screen: 'Map',
      description: 'View interactive campus map with building locations',
      color: '#4CAF50',
      gradient: ['#4CAF50', '#2E7D32'],
    },
    {
      title: 'History',
      icon: 'history',
      screen: 'History',
      description: 'View your previous location recognitions',
      color: '#2196F3',
      gradient: ['#2196F3', '#1976D2'],
    },
    {
      title: 'Help',
      icon: 'help',
      screen: 'Help',
      description: 'Learn how to use the app',
      color: '#9C27B0',
      gradient: ['#9C27B0', '#7B1FA2'],
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={[COLORS.primary, '#FFA500']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.headerTop}>
          <View style={styles.logoWrapper}>
            <Image
              source={require('../assets/fast.png')}
              style={styles.logo}
              resizeMode="contain"
            />
          </View>
          <View style={styles.headerTextContainer}>
            <Text style={styles.headerTitle}>Campus Navigation</Text>
            <Text style={styles.headerSubtitle}>Welcome to FAST-NUCES Lahore</Text>
          </View>
        </View>
      </LinearGradient>

      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {menuItems.map((item, index) => (
          <Animated.View
            key={index}
            style={[
              styles.menuItemWrapper,
              {
                opacity: fadeAnim,
                transform: [{ translateY: translateY }],
                marginTop: index === 0 ? 0 : SPACING.lg,
              },
            ]}
          >
            <TouchableOpacity
              style={styles.menuItem}
              onPress={() => navigation.navigate(item.screen)}
              activeOpacity={0.7}
            >
              <LinearGradient
                colors={item.gradient}
                style={styles.menuItemContent}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <View style={styles.menuIconContainer}>
                  <MaterialIcons name={item.icon} size={32} color={COLORS.background} />
                </View>
                <View style={styles.menuTextContainer}>
                  <Text style={styles.menuTitle}>{item.title}</Text>
                  <Text style={styles.menuDescription}>{item.description}</Text>
                </View>
                <MaterialIcons name="chevron-right" size={24} color={COLORS.background} />
              </LinearGradient>
            </TouchableOpacity>
          </Animated.View>
        ))}
      </ScrollView>

      <View style={styles.footer}>
        <Text style={styles.footerText}>FAST-NUCES © 2024</Text>
      </View>
    </SafeAreaView>
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
  headerTop: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoWrapper: {
    width: 60,
    height: 60,
    borderRadius: BORDER_RADIUS.round,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.small,
  },
  logo: {
    width: 45,
    height: 45,
  },
  headerTextContainer: {
    marginLeft: SPACING.md,
    flex: 1,
  },
  headerTitle: {
    fontSize: FONTS.sizes.xl,
    fontWeight: 'bold',
    color: COLORS.background,
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
    paddingBottom: SPACING.xl,
  },
  menuItemWrapper: {
    borderRadius: BORDER_RADIUS.lg,
    ...SHADOWS.medium,
  },
  menuItem: {
    borderRadius: BORDER_RADIUS.lg,
    overflow: 'hidden',
  },
  menuItemContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.lg,
  },
  menuIconContainer: {
    width: 56,
    height: 56,
    borderRadius: BORDER_RADIUS.lg,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  menuTextContainer: {
    flex: 1,
    marginRight: SPACING.sm,
  },
  menuTitle: {
    fontSize: FONTS.sizes.lg,
    fontWeight: 'bold',
    color: COLORS.background,
    marginBottom: SPACING.xs,
  },
  menuDescription: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.background,
    opacity: 0.9,
  },
  footer: {
    padding: SPACING.md,
    alignItems: 'center',
    backgroundColor: COLORS.card,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  footerText: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.textSecondary,
  },
});

export default HomeScreen; 