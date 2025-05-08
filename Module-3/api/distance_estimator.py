import cv2
import numpy as np
import math
from typing import Optional, Tuple, List
from pathlib import Path
import json

class DistanceEstimator:
    def __init__(self, calibration_file: str = 'camera_calibration.json'):
        self.focal_length = None
        self.known_width = 3.0  # meters (average building width)
        self.camera_matrix = None
        self.dist_coeffs = None
        self.calibration_file = Path(calibration_file)
        self.load_calibration()
        
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

    def _estimate_camera_parameters(self, calibration_points: List[Tuple[np.ndarray, float]]) -> bool:
        """Estimate camera parameters from multiple calibration points"""
        if len(calibration_points) < 3:
            return False
            
        # Prepare object points and image points
        obj_points = []
        img_points = []
        
        for image, distance in calibration_points:
            # Preprocess image
            processed = self._preprocess_image(image)
            
            # Detect edges
            contours = self._detect_edges(processed)
            
            if not contours:
                continue
                
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get corners
            corners = cv2.approxPolyDP(largest_contour, 0.04 * cv2.arcLength(largest_contour, True), True)
            
            if len(corners) != 4:
                continue
                
            # Add to calibration points
            obj_points.append(np.array([
                [0, 0, 0],
                [self.known_width, 0, 0],
                [self.known_width, distance, 0],
                [0, distance, 0]
            ], dtype=np.float32))
            
            img_points.append(corners.reshape(-1, 2).astype(np.float32))
        
        if len(obj_points) < 3:
            return False
            
        # Calibrate camera
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            obj_points, img_points, 
            (image.shape[1], image.shape[0]), 
            None, None
        )
        
        if ret:
            self.camera_matrix = mtx
            self.dist_coeffs = dist
            return True
            
        return False

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
            
            # Save calibration
            self.save_calibration()
            
            return True
        except Exception as e:
            print(f"Calibration error: {str(e)}")
            return False

    def estimate_distance(self, image: np.ndarray, user_location: Optional[Tuple[float, float]] = None) -> float:
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

    def save_calibration(self) -> None:
        """Save camera calibration parameters"""
        calibration_data = {
            'focal_length': float(self.focal_length) if self.focal_length is not None else None,
            'camera_matrix': self.camera_matrix.tolist() if self.camera_matrix is not None else None,
            'dist_coeffs': self.dist_coeffs.tolist() if self.dist_coeffs is not None else None
        }
        
        try:
            with open(self.calibration_file, 'w') as f:
                json.dump(calibration_data, f)
        except Exception as e:
            print(f"Error saving calibration: {str(e)}")

    def load_calibration(self) -> None:
        """Load camera calibration parameters"""
        if not self.calibration_file.exists():
            return
            
        try:
            with open(self.calibration_file, 'r') as f:
                calibration_data = json.load(f)
                
            self.focal_length = calibration_data.get('focal_length')
            camera_matrix = calibration_data.get('camera_matrix')
            dist_coeffs = calibration_data.get('dist_coeffs')
            
            if camera_matrix:
                self.camera_matrix = np.array(camera_matrix)
            if dist_coeffs:
                self.dist_coeffs = np.array(dist_coeffs)
        except Exception as e:
            print(f"Error loading calibration: {str(e)}") 