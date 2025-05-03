# Campus Navigation Assistant

A React Native mobile application that helps users navigate through campus by recognizing buildings from images and estimating their location.

## Features

- Image capture using device camera
- Building recognition and distance estimation
- Interactive campus map with user position
- Real-time location updates

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Run on iOS or Android:
```bash
npm run ios
# or
npm run android
```

## Backend API Integration

The app communicates with a backend server for image processing. Update the API endpoint in `components/ImageCapture.js`:

```javascript
const response = await axios.post('http://your-backend-api/process-image', {
  image: base64Image,
});
```

### API Request Format
```json
{
  "image": "base64_encoded_image_string"
}
```

### API Response Format
```json
{
  "building": "Building Name",
  "distance": 100,
  "coordinates": {
    "latitude": 37.7749,
    "longitude": -122.4194
  }
}
```

## Configuration

1. Update the default map region in `components/MapView.js` with your campus coordinates:
```javascript
const defaultRegion = {
  latitude: YOUR_CAMPUS_LATITUDE,
  longitude: YOUR_CAMPUS_LONGITUDE,
  latitudeDelta: 0.01,
  longitudeDelta: 0.01,
};
```

## Dependencies

- React Native
- Expo
- React Native Maps
- React Native Elements
- Axios
- Expo Camera

## License

MIT 