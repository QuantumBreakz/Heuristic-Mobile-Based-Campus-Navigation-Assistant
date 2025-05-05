# Campus Navigation Assistant Mobile App

A Flutter mobile application for campus navigation with building detection and distance estimation capabilities.

## Features

- Building Detection: Detect and identify buildings in real-time using the device camera
- Distance Estimation: Estimate distance to buildings using both size-based and triangulation methods
- Campus Navigation: Interactive map with building locations and navigation routes
- Camera Calibration: Calibrate the device camera for accurate distance estimation
- Settings: Configure API endpoints and camera parameters

## Prerequisites

- Flutter SDK (version 3.0.0 or higher)
- Android Studio / Xcode for building
- Backend server running (see backend README for setup)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Module-4/mobile_app/campus_navigation
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Create a `.env` file in the project root:
   ```
   API_BASE_URL=http://localhost:5000
   ```

4. For Android:
   - Add the following permissions to `android/app/src/main/AndroidManifest.xml`:
     ```xml
     <uses-permission android:name="android.permission.INTERNET"/>
     <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
     <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
     <uses-permission android:name="android.permission.CAMERA"/>
     ```

5. For iOS:
   - Add the following to `ios/Runner/Info.plist`:
     ```xml
     <key>NSCameraUsageDescription</key>
     <string>Camera access is required for building detection</string>
     <key>NSLocationWhenInUseUsageDescription</key>
     <string>Location access is required for navigation</string>
     <key>NSLocationAlwaysUsageDescription</key>
     <string>Location access is required for navigation</string>
     ```

## Building

1. For Android:
   ```bash
   flutter build apk --release
   ```

2. For iOS:
   ```bash
   flutter build ios --release
   ```

## Usage

### Building Detection

1. Open the app and navigate to the Camera screen
2. Point the camera at a building
3. Tap the capture button to detect the building and estimate its distance
4. The app will display the building name, confidence score, and estimated distance

### Triangulation Mode

1. In the Camera screen, tap the mode toggle button to switch to triangulation mode
2. Capture the first image of the building
3. Move to a different position (maintaining a known baseline distance)
4. Capture the second image
5. The app will calculate the distance using triangulation

### Campus Navigation

1. Open the Map screen
2. The app will show your current location and nearby buildings
3. Tap on a building marker to see its details
4. Use the directions button to get navigation instructions

### Camera Calibration

1. Go to Settings
2. Enter the chessboard pattern size and square size
3. Capture at least 3 images of the chessboard pattern from different angles
4. Tap "Calibrate Camera" to perform calibration
5. The app will save the calibration data for future use

## Troubleshooting

### Common Issues

1. Camera not working:
   - Check if camera permissions are granted
   - Restart the app
   - Ensure the backend server is running

2. Location not updating:
   - Check if location services are enabled
   - Verify location permissions
   - Ensure GPS is turned on

3. API connection issues:
   - Verify the API base URL in settings
   - Check internet connection
   - Ensure the backend server is accessible

### Debugging

1. Enable debug mode:
   ```bash
   flutter run --debug
   ```

2. Check logs:
   ```bash
   flutter logs
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 