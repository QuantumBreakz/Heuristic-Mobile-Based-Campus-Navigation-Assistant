# Campus Navigation Assistant API Documentation

## Base URL
`http://localhost:5000/api`

## Endpoints

### 1. Building Detection and Distance Estimation
**Endpoint:** `/detect`  
**Method:** `POST`  
**Description:** Detects buildings in an image and estimates their distances.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `image`: Image file (PNG, JPG, JPEG)

**Response:**
```json
{
    "success": true,
    "detections": [
        {
            "building_name": "string",
            "confidence": float,
            "bbox": [x1, y1, x2, y2]
        }
    ],
    "distances": [
        {
            "building_name": "string",
            "distance": float,
            "unit": "meters"
        }
    ]
}
```

### 2. Triangulation-based Distance Estimation
**Endpoint:** `/triangulate`  
**Method:** `POST`  
**Description:** Estimates distance to a building using triangulation from two images.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `image1`: First image file (PNG, JPG, JPEG)
  - `image2`: Second image file (PNG, JPG, JPEG)
  - `baseline`: Distance between camera positions in meters (default: 1.0)

**Response:**
```json
{
    "success": true,
    "distance": float
}
```

### 3. Camera Calibration
**Endpoint:** `/calibrate`  
**Method:** `POST`  
**Description:** Calibrates the camera using chessboard pattern images.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `images`: Multiple image files (PNG, JPG, JPEG)
  - `pattern_size`: Chessboard pattern size as "rows,columns" (default: "9,6")
  - `square_size`: Size of chessboard squares in meters (default: 0.025)

**Response:**
```json
{
    "success": true,
    "calibration_data": {
        "camera_matrix": [[float, float, float], [float, float, float], [float, float, float]],
        "dist_coeffs": [float, float, float, float, float]
    }
}
```

### 4. Health Check
**Endpoint:** `/health`  
**Method:** `GET`  
**Description:** Checks the health status of the API and models.

**Response:**
```json
{
    "status": "healthy",
    "models_loaded": true,
    "calibration_available": true,
    "rate_limit": 60
}
```

## Error Responses

All endpoints return error responses in the following format:
```json
{
    "success": false,
    "error": "Error message"
}
```

Common HTTP status codes:
- 400: Bad Request (invalid input)
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error

## Rate Limiting

The API implements rate limiting to prevent abuse. By default, each IP address is limited to 60 requests per minute. This can be configured using the `RATE_LIMIT` environment variable.

## File Upload Requirements

- Maximum file size: 16MB
- Supported image formats: PNG, JPG, JPEG
- For calibration: At least 3 images required
- For triangulation: Exactly 2 images required 