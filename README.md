# Campus Navigation App

A mobile application for navigating the FAST-NUCES campus using computer vision and trilateration techniques.

## Project Structure

The project is organized into modules, each focusing on different aspects of the application:

- `Module-1/`: Initial project setup and requirements
- `Module-2/`: Basic UI implementation and navigation
- `Module-3/`: Camera integration and image processing
- `Module-4/`: Complete application with backend integration
  - `backend/`: Flask backend with building recognition and trilateration
  - `mobile_app/`: Flutter mobile application
  - `docs/`: Documentation and API specifications

## Getting Started

### Prerequisites

- Flutter SDK
- Python 3.8+
- Android Studio / Xcode
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/campus-navigation.git
cd campus-navigation
```

2. Set up the backend:
```bash
cd Module-4/backend
pip install -r requirements.txt
python run.sh
```

3. Set up the mobile app:
```bash
cd Module-4/mobile_app/campus_navigation
flutter pub get
flutter run
```

## Features

- Real-time building recognition using computer vision
- Accurate position estimation using trilateration
- Interactive campus map with building information
- Offline support for basic navigation
- Dark mode support
- Multi-language support

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 