# Campus Navigation Assistant - Backend

This is the backend server for the Campus Navigation Assistant mobile app. It integrates building detection (Module-2) and distance estimation (Module-3) functionality.

## Features

- Building detection using trained ResNet50 model
- Distance estimation using both size-based and triangulation methods
- Camera calibration support
- RESTful API endpoints for mobile app integration

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
./run.sh
```

## API Endpoints

### 1. Building Detection and Distance Estimation
- **Endpoint**: `/api/detect`
- **Method**: POST
- **Input**: Single image file
- **Response**:
```json
{
    "success": true,
    "building": "Building Name",
    "confidence": 0.95,
    "distance": 15.5,
    "bbox": [x1, y1, x2, y2]
}
```

### 2. Triangulation-based Distance Estimation
- **Endpoint**: `/api/triangulate`
- **Method**: POST
- **Input**: Two images and baseline distance
- **Response**:
```json
{
    "success": true,
    "building": "Building Name",
    "distance": 15.5,
    "confidence1": 0.95,
    "confidence2": 0.92,
    "bbox1": [x1, y1, x2, y2],
    "bbox2": [x1, y1, x2, y2]
}
```

### 3. Camera Calibration
- **Endpoint**: `/api/calibrate`
- **Method**: POST
- **Input**: Multiple calibration images, pattern size, square size
- **Response**:
```json
{
    "success": true,
    "message": "Camera calibrated successfully"
}
```

## Directory Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── run.sh                # Server startup script
├── calibration_data.json # Camera calibration data
├── calibration_images/   # Calibration images
└── test_images/         # Test images
```

## Integration with Mobile App

The mobile app can communicate with this backend using the following steps:

1. **Initial Setup**:
   - Calibrate the camera using the `/api/calibrate` endpoint
   - Save the calibration data for future use

2. **Real-time Detection**:
   - Send images to `/api/detect` endpoint
   - Process the response to show building name and distance

3. **Enhanced Distance Estimation**:
   - Capture two images from different positions
   - Send to `/api/triangulate` with baseline distance
   - Get more accurate distance estimation

## Error Handling

All endpoints return a JSON response with a `success` field. If `success` is `false`, an `error` field will be present with the error message.

## Performance

- Building detection: ~100ms per image
- Distance estimation: ~50ms per image
- Triangulation: ~200ms for two images
- Memory usage: ~500MB (including model)

## Notes

- The server runs on port 5000 by default
- CORS is enabled for mobile app integration
- Camera calibration data is saved in `calibration_data.json`
- The model expects images in standard format (JPEG/PNG) 