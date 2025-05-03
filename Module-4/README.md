# Module-4: Path Planning and Mobile Application

This module implements the mobile application interface and path planning functionality for the Campus Navigation Assistant.

## Features

1. **User Interface**
   - Interactive campus map
   - Building directory
   - Real-time navigation
   - Settings and preferences
   - User authentication

2. **Path Planning**
   - Optimal route calculation
   - Real-time path updates
   - Obstacle avoidance
   - Multiple destination support

3. **Integration**
   - Landmark recognition integration
   - Distance estimation integration
   - Real-time camera feed processing

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

## Installation

1. Install dependencies:
```bash
cd Module-4
npm install
```

2. For iOS (macOS only):
```bash
cd ios
pod install
cd ..
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Android
```bash
npm run android
```

### iOS (macOS only)
```bash
npm run ios
```

## Project Structure

```
Module-4/
├── src/
│   ├── components/         # Reusable UI components
│   ├── screens/           # Application screens
│   ├── navigation/        # Navigation configuration
│   ├── services/          # API and backend services
│   ├── utils/             # Utility functions
│   ├── assets/            # Images and other assets
│   └── constants/         # App constants and themes
├── android/               # Android-specific files
├── ios/                   # iOS-specific files
└── tests/                 # Test files
```

## Key Components

### 1. MapView Component
- Interactive campus map
- Real-time location tracking
- Path visualization
- Building markers

### 2. Navigation Service
- Path calculation algorithms
- Real-time updates
- Obstacle detection
- Multiple route options

### 3. Building Directory
- Search functionality
- Building details
- Quick navigation
- Favorites management

## API Integration

The application integrates with several APIs:

1. **Map Services**
   - Campus map data
   - Building coordinates
   - Path network

2. **Navigation Services**
   - Route calculation
   - Real-time updates
   - Traffic information

3. **User Services**
   - Authentication
   - Preferences
   - History

## Testing

Run the test suite:
```bash
npm test
```

## Building for Production

### Android
```bash
cd android
./gradlew assembleRelease
```

### iOS (macOS only)
```bash
cd ios
xcodebuild -workspace App.xcworkspace -scheme App -configuration Release
```

## Troubleshooting

Common issues and solutions:

1. **Build Failures**
   - Clear cache: `npm cache clean --force`
   - Reinstall dependencies: `rm -rf node_modules && npm install`

2. **Runtime Errors**
   - Check environment variables
   - Verify API endpoints
   - Ensure proper permissions

3. **Performance Issues**
   - Optimize image assets
   - Implement lazy loading
   - Use proper caching

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 