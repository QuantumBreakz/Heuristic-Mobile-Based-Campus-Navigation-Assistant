from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import math
from typing import Optional, List, Dict
import uvicorn
from pydantic import BaseModel
import io
from PIL import Image
import base64

app = FastAPI(title="Distance Estimator API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Location(BaseModel):
    latitude: float
    longitude: float

class CalibrationPoint(BaseModel):
    known_distance: float
    image: str  # base64 encoded image

class DistanceEstimator:
    def __init__(self):
        self.focal_length = None
        self.known_width = 3.0  # meters (average building width)
        self.camera_matrix = None
        self.dist_coeffs = None
        
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better edge detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    def _detect_edges(self, image: np.ndarray) -> List[np.ndarray]:
        """Detect edges in the image"""
        # Find contours
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours based on area and shape
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Minimum area threshold
                # Approximate the contour
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                
                # Check if the shape is roughly rectangular
                if len(approx) >= 4 and len(approx) <= 6:
                    valid_contours.append(approx)
        
        return valid_contours

    def _calculate_distance(self, width_in_pixels: float) -> float:
        """Calculate distance using the focal length"""
        if self.focal_length is None:
            raise ValueError("Camera not calibrated")
        
        # Distance = (Known Width * Focal Length) / Width in Pixels
        distance = (self.known_width * self.focal_length) / width_in_pixels
        return distance

    def calibrate(self, known_distance: float, image: np.ndarray) -> bool:
        """Calibrate the camera using a known distance"""
        try:
            # Preprocess image
            processed = self._preprocess_image(image)
            
            # Detect edges
            contours = self._detect_edges(processed)
            
            if not contours:
                return False
            
            # Find the largest contour (assuming it's the building)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get the width in pixels
            x, y, w, h = cv2.boundingRect(largest_contour)
            width_in_pixels = w
            
            # Calculate focal length
            self.focal_length = (width_in_pixels * known_distance) / self.known_width
            
            return True
        except Exception as e:
            print(f"Calibration error: {str(e)}")
            return False

    def estimate_distance(self, image: np.ndarray, user_location: Optional[tuple] = None) -> float:
        """Estimate distance to the building in the image"""
        try:
            # Preprocess image
            processed = self._preprocess_image(image)
            
            # Detect edges
            contours = self._detect_edges(processed)
            
            if not contours:
                raise ValueError("No valid building contours detected")
            
            # Find the largest contour (assuming it's the building)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get the width in pixels
            x, y, w, h = cv2.boundingRect(largest_contour)
            width_in_pixels = w
            
            # Calculate distance
            distance = self._calculate_distance(width_in_pixels)
            
            # If user location is provided, adjust distance based on perspective
            if user_location and self.camera_matrix is not None:
                # Convert distance to meters
                distance_meters = distance
                
                # Calculate angle based on user location
                lat1, lon1 = user_location
                # Assuming building is at a fixed location (can be parameterized)
                lat2, lon2 = 24.9147, 67.0997  # Example coordinates
                
                # Calculate bearing
                dlon = lon2 - lon1
                y = math.sin(dlon) * math.cos(lat2)
                x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
                bearing = math.atan2(y, x)
                
                # Adjust distance based on angle
                distance = distance_meters / math.cos(bearing)
            
            return distance
        except Exception as e:
            raise ValueError(f"Distance estimation error: {str(e)}")

# Initialize the distance estimator
distance_estimator = DistanceEstimator()

@app.post("/calibrate")
async def calibrate_distance(calibration: CalibrationPoint):
    """Calibrate the distance estimator with a known distance"""
    try:
        # Convert base64 image to numpy array
        image_data = calibration.image.split(',')[1] if ',' in calibration.image else calibration.image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Convert RGB to BGR (OpenCV format)
        if len(image_np.shape) == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Calibrate the estimator
        success = distance_estimator.calibrate(calibration.known_distance, image_np)
        
        if success:
            return JSONResponse({
                "message": "Calibration successful",
                "focal_length": float(distance_estimator.focal_length)
            })
        else:
            raise HTTPException(status_code=400, detail="Calibration failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estimate")
async def estimate_distance(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    """Estimate distance to the building in the image"""
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_np is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
        
        # Estimate distance
        distance = distance_estimator.estimate_distance(
            image_np,
            (latitude, longitude)
        )
        
        return JSONResponse({
            "distance": float(distance),
            "unit": "meters"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 