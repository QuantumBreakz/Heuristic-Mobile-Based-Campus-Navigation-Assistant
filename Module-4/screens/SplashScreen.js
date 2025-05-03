import React, { useEffect } from 'react';
import { StyleSheet, View, Text, Image, Animated, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, SHADOWS, BORDER_RADIUS } from '../constants/theme';
import { MaterialIcons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

const SplashScreen = ({ navigation }) => {
  const fadeAnim = new Animated.Value(0);
  const scaleAnim = new Animated.Value(0.8);
  const translateYAnim = new Animated.Value(50);
  const backgroundAnim = new Animated.Value(0);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 20,
        friction: 7,
        useNativeDriver: true,
      }),
      Animated.timing(translateYAnim, {
        toValue: 0,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.timing(backgroundAnim, {
        toValue: 1,
        duration: 2000,
        useNativeDriver: false,
      }),
    ]).start();

    // Navigate to Home after 3 seconds
    const timer = setTimeout(() => {
      navigation.replace('Home');
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const backgroundOpacity = backgroundAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0.5, 1],
  });

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[COLORS.primary, '#FFA500', '#FF8C00']}
        style={styles.gradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Animated.View 
          style={[
            styles.content, 
            { 
              opacity: fadeAnim,
              transform: [
                { scale: scaleAnim },
                { translateY: translateYAnim }
              ]
            }
          ]}
        >
          <View style={styles.logoContainer}>
            <Image
              source={require('../assets/fast.png')}
              style={styles.logo}
              resizeMode="contain"
            />
            <Animated.View style={[styles.shine, { opacity: backgroundOpacity }]} />
          </View>
          <Text style={styles.title}>FAST-NUCES</Text>
          <Text style={styles.subtitle}>Campus Navigation Assistant</Text>
          
          <View style={styles.decorationContainer}>
            <MaterialIcons name="location-on" size={24} color={COLORS.background} style={styles.icon} />
            <MaterialIcons name="navigation" size={24} color={COLORS.background} style={styles.icon} />
            <MaterialIcons name="explore" size={24} color={COLORS.background} style={styles.icon} />
          </View>
        </Animated.View>
      </LinearGradient>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
    width: width * 0.8,
  },
  logoContainer: {
    width: 180,
    height: 180,
    borderRadius: BORDER_RADIUS.xl,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.xl,
    ...SHADOWS.large,
    overflow: 'hidden',
    position: 'relative',
  },
  logo: {
    width: 150,
    height: 150,
  },
  shine: {
    position: 'absolute',
    top: -100,
    left: -100,
    width: 200,
    height: 200,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    transform: [{ rotate: '45deg' }],
  },
  title: {
    fontSize: FONTS.sizes.xxxl,
    fontWeight: 'bold',
    color: COLORS.background,
    marginBottom: SPACING.xs,
    textAlign: 'center',
    textShadowColor: 'rgba(0, 0, 0, 0.2)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  subtitle: {
    fontSize: FONTS.sizes.lg,
    color: COLORS.background,
    textAlign: 'center',
    opacity: 0.9,
    marginBottom: SPACING.xl,
  },
  decorationContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: SPACING.xl,
  },
  icon: {
    marginHorizontal: SPACING.sm,
    opacity: 0.9,
  },
});

export default SplashScreen; 