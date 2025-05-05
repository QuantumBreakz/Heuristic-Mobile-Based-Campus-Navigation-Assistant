#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python dependencies are installed
check_python_deps() {
    if ! command_exists pip; then
        echo "Error: pip is not installed"
        exit 1
    fi

    if ! pip list | grep -q "flask"; then
        echo "Installing Python dependencies..."
        pip install -r backend/requirements.txt
    fi
}

# Function to check if Flutter dependencies are installed
check_flutter_deps() {
    if ! command_exists flutter; then
        echo "Error: Flutter SDK is not installed"
        exit 1
    fi

    cd mobile_app/campus_navigation
    if [ ! -d "build" ]; then
        echo "Installing Flutter dependencies..."
        flutter pub get
    fi
    cd ../..
}

# Function to start the backend server
start_backend() {
    echo "Starting backend server..."
    cd backend/api
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo "Backend server started with PID: $BACKEND_PID"
}

# Function to start the Flutter app
start_flutter_app() {
    echo "Starting Flutter app..."
    cd mobile_app/campus_navigation
    flutter run
}

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID
    fi
    exit 0
}

# Set up cleanup trap
trap cleanup EXIT

# Main script
echo "Setting up Campus Navigation Assistant..."

# Check dependencies
check_python_deps
check_flutter_deps

# Create .env file if it doesn't exist
if [ ! -f "mobile_app/campus_navigation/.env" ]; then
    echo "Creating .env file..."
    cp mobile_app/campus_navigation/.env.example mobile_app/campus_navigation/.env
    echo "Please update the .env file with your configuration"
    exit 1
fi

# Start services
start_backend

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Start Flutter app
start_flutter_app

# Cleanup
kill $BACKEND_PID 