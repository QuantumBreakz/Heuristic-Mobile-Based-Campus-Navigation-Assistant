import cv2
import numpy as np
import json
import os

class CalibrationUtility:
    def __init__(self):
        self.calibration_data = None
        self.calibration_file = 'calibration_data.json'
    
    def calibrate_camera(self, image, pattern_size, square_size):
        """Calibrate camera using chessboard pattern."""
        try:
            # Convert image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Find chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
            
            if not ret:
                raise ValueError("Chessboard pattern not found")
            
            # Refine corner detection
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            
            # Prepare object points
            objp = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
            objp[:,:2] = np.mgrid[0:pattern_size[0],0:pattern_size[1]].T.reshape(-1,2) * square_size
            
            # Calibrate camera
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                [objp], [corners2], gray.shape[::-1], None, None
            )
            
            # Calculate focal length and pixel size
            focal_length = mtx[0,0]
            pixel_size = 1.0 / focal_length
            
            # Store calibration data
            self.calibration_data = {
                'focal_length': float(focal_length),
                'pixel_size': float(pixel_size),
                'matrix': mtx.tolist(),
                'distortion': dist.tolist()
            }
            
            # Save calibration data
            self._save_calibration_data()
            
            return self.calibration_data
            
        except Exception as e:
            print(f"Error in camera calibration: {str(e)}")
            return None
    
    def _save_calibration_data(self):
        """Save calibration data to file."""
        try:
            with open(self.calibration_file, 'w') as f:
                json.dump(self.calibration_data, f)
        except Exception as e:
            print(f"Error saving calibration data: {str(e)}")
    
    def load_calibration_data(self):
        """Load calibration data from file."""
        try:
            if os.path.exists(self.calibration_file):
                with open(self.calibration_file, 'r') as f:
                    self.calibration_data = json.load(f)
                return self.calibration_data
            return None
        except Exception as e:
            print(f"Error loading calibration data: {str(e)}")
            return None 