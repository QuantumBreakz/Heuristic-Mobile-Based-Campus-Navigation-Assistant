import React, { useState, useRef } from 'react';
import { StyleSheet, View, TouchableOpacity, Image, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import { Button, Text } from 'react-native-elements';
import axios from 'axios';

const ImageCapture = ({ onImageCapture, onLocationUpdate, setIsLoading }) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [camera, setCamera] = useState(null);
  const [image, setImage] = useState(null);

  // Request camera permissions
  React.useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (camera) {
      try {
        const photo = await camera.takePictureAsync({
          quality: 0.5,
          base64: true,
        });
        setImage(photo.uri);
        onImageCapture(photo.uri);
        await processImage(photo.base64);
      } catch (error) {
        Alert.alert('Error', 'Failed to take picture');
      }
    }
  };

  const processImage = async (base64Image) => {
    setIsLoading(true);
    try {
      // Replace with your actual backend API endpoint
      const response = await axios.post('http://your-backend-api/process-image', {
        image: base64Image,
      });

      // Expected response format:
      // {
      //   building: "Building Name",
      //   distance: 100, // in meters
      //   coordinates: {
      //     latitude: 37.7749,
      //     longitude: -122.4194
      //   }
      // }
      
      onLocationUpdate(response.data);
    } catch (error) {
      Alert.alert('Error', 'Failed to process image');
      setIsLoading(false);
    }
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      {!image ? (
        <Camera
          style={styles.camera}
          ref={ref => setCamera(ref)}
          type={Camera.Constants.Type.back}
        >
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.captureButton}
              onPress={takePicture}
            >
              <Text style={styles.buttonText}>Capture</Text>
            </TouchableOpacity>
          </View>
        </Camera>
      ) : (
        <View style={styles.previewContainer}>
          <Image source={{ uri: image }} style={styles.preview} />
          <Button
            title="Take Another Picture"
            onPress={() => setImage(null)}
            containerStyle={styles.button}
          />
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    height: 300,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'flex-end',
    margin: 20,
  },
  captureButton: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 50,
    marginBottom: 20,
  },
  buttonText: {
    fontSize: 18,
    color: '#000',
  },
  previewContainer: {
    flex: 1,
    alignItems: 'center',
  },
  preview: {
    width: '100%',
    height: '80%',
    resizeMode: 'contain',
  },
  button: {
    marginTop: 10,
    width: '80%',
  },
});

export default ImageCapture; 