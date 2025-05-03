import cv2
import numpy as np
from typing import List, Tuple, Optional
from advanced_distance_estimator import ReferenceObject, AdvancedDistanceEstimator

class CalibrationUtility:
    def __init__(self):
        self.camera_matrix = None
        self.distortion_coeffs = None
        self.reference_objects = []
        
    def calibrate_camera(self, 
                        calibration_images: List[np.ndarray],
                        pattern_size: Tuple[int, int],
                        square_size: float) -> dict:
        """
        Calibrate camera using chessboard pattern
        :param calibration_images: List of calibration images
        :param pattern_size: Number of inner corners (width, height)
        :param square_size: Size of squares in meters
        :return: Dictionary of camera parameters
        """
        # Prepare object points
        objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
        objp *= square_size
        
        # Arrays to store object points and image points
        objpoints = []  # 3D points in real world space
        imgpoints = []  # 2D points in image plane
        
        for img in calibration_images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
            
            if ret:
                # Refine corner detection
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                
                objpoints.append(objp)
                imgpoints.append(corners2)
        
        if not objpoints:
            raise ValueError("No valid calibration images found")
        
        # Calibrate camera
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)
        
        # Calculate focal length in pixels
        focal_length = mtx[0, 0]
        
        # Calculate field of view
        fov_x = 2 * np.arctan(gray.shape[1] / (2 * focal_length))
        fov_x_deg = np.degrees(fov_x)
        
        # Store calibration results
        self.camera_matrix = mtx
        self.distortion_coeffs = dist
        
        return {
            'focal_length': focal_length,
            'image_width': gray.shape[1],
            'image_height': gray.shape[0],
            'fov': fov_x_deg,
            'camera_matrix': mtx.tolist(),
            'distortion_coeffs': dist.tolist()
        }
    
    def add_reference_object(self,
                           name: str,
                           actual_height: float,
                           actual_width: float,
                           template_image: Optional[np.ndarray] = None,
                           confidence_threshold: float = 0.7) -> None:
        """
        Add a reference object for distance estimation
        :param name: Name of the reference object
        :param actual_height: Actual height in meters
        :param actual_width: Actual width in meters
        :param template_image: Optional template image for matching
        :param confidence_threshold: Confidence threshold for detection
        """
        ref_obj = ReferenceObject(
            name=name,
            actual_height=actual_height,
            actual_width=actual_width,
            template=template_image,
            confidence_threshold=confidence_threshold
        )
        self.reference_objects.append(ref_obj)
    
    def calibrate_reference_object(self,
                                 image: np.ndarray,
                                 name: str,
                                 actual_height: float,
                                 actual_width: float,
                                 confidence_threshold: float = 0.7) -> None:
        """
        Calibrate a reference object from an image
        :param image: Image containing the reference object
        :param name: Name of the reference object
        :param actual_height: Actual height in meters
        :param actual_width: Actual width in meters
        :param confidence_threshold: Confidence threshold for detection
        """
        # Extract template
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("No reference object found in image")
        
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Extract template
        template = image[y:y+h, x:x+w]
        
        # Add reference object
        self.add_reference_object(
            name=name,
            actual_height=actual_height,
            actual_width=actual_width,
            template_image=template,
            confidence_threshold=confidence_threshold
        )
    
    def create_estimator(self) -> AdvancedDistanceEstimator:
        """
        Create a distance estimator with current calibration
        :return: AdvancedDistanceEstimator instance
        """
        if not self.camera_matrix is not None:
            raise ValueError("Camera not calibrated")
        
        camera_params = {
            'focal_length': self.camera_matrix[0, 0],
            'image_width': self.camera_matrix[0, 2] * 2,
            'image_height': self.camera_matrix[1, 2] * 2,
            'fov': np.degrees(2 * np.arctan(self.camera_matrix[0, 2] / self.camera_matrix[0, 0])),
            'camera_matrix': self.camera_matrix.tolist(),
            'distortion_coeffs': self.distortion_coeffs.tolist()
        }
        
        return AdvancedDistanceEstimator(camera_params, self.reference_objects)
    
    def save_calibration(self, filepath: str) -> None:
        """
        Save calibration data to file
        :param filepath: Path to save calibration file
        """
        calibration_data = {
            'camera_matrix': self.camera_matrix.tolist(),
            'distortion_coeffs': self.distortion_coeffs.tolist(),
            'reference_objects': [
                {
                    'name': obj.name,
                    'actual_height': obj.actual_height,
                    'actual_width': obj.actual_width,
                    'confidence_threshold': obj.confidence_threshold
                }
                for obj in self.reference_objects
            ]
        }
        
        import json
        with open(filepath, 'w') as f:
            json.dump(calibration_data, f, indent=4)
    
    @classmethod
    def load_calibration(cls, filepath: str) -> 'CalibrationUtility':
        """
        Load calibration from file
        :param filepath: Path to calibration file
        :return: CalibrationUtility instance
        """
        import json
        with open(filepath, 'r') as f:
            calibration_data = json.load(f)
        
        utility = cls()
        utility.camera_matrix = np.array(calibration_data['camera_matrix'])
        utility.distortion_coeffs = np.array(calibration_data['distortion_coeffs'])
        
        for obj in calibration_data['reference_objects']:
            utility.add_reference_object(
                name=obj['name'],
                actual_height=obj['actual_height'],
                actual_width=obj['actual_width'],
                confidence_threshold=obj['confidence_threshold']
            )
        
        return utility 