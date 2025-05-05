import cv2
import numpy as np
from .calibration_utils import CalibrationUtility

class AdvancedDistanceEstimator:
    def __init__(self):
        self.calibration_utility = CalibrationUtility()
        self.calibration_data = None
    
    def estimate_distance(self, image, building_id, building_dimensions):
        """Estimate distance to building using size-based estimation."""
        try:
            if self.calibration_data is None:
                raise ValueError("Camera not calibrated")
            
            # Get building dimensions
            height = building_dimensions.get('height', 0)
            if height == 0:
                raise ValueError("Building height not available")
            
            # Detect building in image
            building_contour = self._detect_building_contour(image)
            if building_contour is None:
                raise ValueError("Building not detected in image")
            
            # Calculate distance using perspective projection
            distance = self._calculate_distance(building_contour, height)
            return distance
            
        except Exception as e:
            print(f"Error in distance estimation: {str(e)}")
            return None
    
    def _detect_building_contour(self, image):
        """Detect building contour in the image."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest contour (assuming it's the building)
        if contours:
            return max(contours, key=cv2.contourArea)
        return None
    
    def _calculate_distance(self, contour, real_height):
        """Calculate distance using perspective projection."""
        # Get the height of the building in pixels
        _, _, _, h = cv2.boundingRect(contour)
        
        # Calculate distance using similar triangles
        # distance = (real_height * focal_length) / (pixel_height * pixel_size)
        focal_length = self.calibration_data['focal_length']
        pixel_size = self.calibration_data['pixel_size']
        
        distance = (real_height * focal_length) / (h * pixel_size)
        return distance 