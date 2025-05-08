# Module-3 Backend: Building Recognition API

A Flask-based REST API for building recognition using ResNet50.

## Features

- Building recognition from images using ResNet50
- Building information retrieval
- Support for multiple image formats (PNG, JPG, JPEG)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the API server:
```bash
python api.py
```

The server will run on `http://localhost:5000`

## API Endpoints

### 1. Building Recognition
- **POST** `/api/recognize`
- Upload an image to recognize a building
- Request: Form data with 'image' file
- Response: Building information and confidence score

### 2. Get All Buildings
- **GET** `/api/buildings`
- Get information about all buildings
- Response: JSON object with building details

### 3. Get Specific Building
- **GET** `/api/buildings/<building_id>`
- Get information about a specific building
- Response: Building details or 404 error

## Project Structure

```
backend/
├── api.py              # Main API file with all endpoints and logic
├── requirements.txt    # Project dependencies
└── README.md          # Documentation
```

## Example Usage

```python
import requests

# Recognize building
with open('building.jpg', 'rb') as f:
    response = requests.post('http://localhost:5000/api/recognize', 
                           files={'image': f})
print(response.json())

# Get all buildings
response = requests.get('http://localhost:5000/api/buildings')
print(response.json())
``` 