# FAST-NUCES Campus Navigation API

This API provides building recognition and distance estimation services for the FAST-NUCES campus navigation system.

## Features

- Building Recognition: Identify buildings from images using computer vision
- Distance Estimation: Calculate distances to buildings using image processing
- Building Information: Get details about campus buildings

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

3. Create a `building_features` directory:
```bash
mkdir building_features
```

## Running the API

Start the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Recognize Building
- **URL**: `/recognize_building`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "image": "base64_encoded_image"
  }
  ```
- **Response**:
  ```json
  {
    "building": {
      "id": "main_block",
      "name": "Main Block",
      "coordinates": [24.9147, 67.0997]
    },
    "confidence": 0.85
  }
  ```

### 2. Estimate Distance
- **URL**: `/estimate_distance`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "image": "base64_encoded_image",
    "user_location": {
      "latitude": 24.9147,
      "longitude": 67.0997
    }
  }
  ```
- **Response**:
  ```json
  {
    "distance": 50.5,
    "unit": "meters"
  }
  ```

### 3. Get Buildings
- **URL**: `/get_buildings`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "id": "main_block",
      "name": "Main Block",
      "coordinates": [24.9147, 67.0997]
    },
    ...
  ]
  ```

## Training the Building Recognizer

To add new buildings or update existing ones:

1. Take clear photos of the buildings
2. Convert images to base64
3. Use the training endpoint to update the model

## Notes

- The distance estimation uses a simplified model and may need calibration for your specific camera
- Building recognition requires good lighting and clear views of the buildings
- The API uses CORS to allow cross-origin requests from the mobile app 