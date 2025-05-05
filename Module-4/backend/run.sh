#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install requirements
pip install -r requirements.txt

# Create necessary directories
mkdir -p calibration_images
mkdir -p test_images

# Run the Flask application
python app.py 