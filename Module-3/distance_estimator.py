import cv2
import numpy as np
from scipy.spatial import distance
from typing import Tuple, List, Optional

class DistanceEstimator:
    def __init__(self, camera_params: dict):
        """
        Initialize the distance estimator with camera parameters
        :param camera_params: Dictionary containing camera parameters
            - focal_length: Camera's focal length in pixels
            - image_width: Width of images in pixels
            - image_height: Height of images in pixels
            - fov: Field of view in degrees
        """
        self.focal_length = camera_params.get('focal_length', 1000)
        self.image_width = camera_params.get('image_width', 1920)
        self.image_height = camera_params.get('image_height', 1080)
        self.fov = camera_params.get('fov', 60)
        
    def size_based_distance(self, 
                          object_height_pixels: float, 
                          actual_height: float) -> float:
        """
        Estimate distance using size-based method
        :param object_height_pixels: Height of object in image in pixels
        :param actual_height: Actual height of object in meters
        :return: Estimated distance in meters
        """
        if object_height_pixels == 0:
            return float('inf')
        return (actual_height * self.focal_length) / object_height_pixels
    
    def triangulation_distance(self, 
                             point1: Tuple[float, float], 
                             point2: Tuple[float, float], 
                             baseline_distance: float) -> float:
        """
        Estimate distance using triangulation
        :param point1: (x, y) coordinates in first image
        :param point2: (x, y) coordinates in second image
        :param baseline_distance: Distance between camera positions in meters
        :return: Estimated distance in meters
        """
        # Calculate angles
        angle1 = self._calculate_angle(point1[0])
        angle2 = self._calculate_angle(point2[0])
        
        # Calculate distance using law of sines
        alpha = np.pi/2 - angle1
        beta = np.pi/2 + angle2
        gamma = np.pi - alpha - beta
        
        if np.sin(gamma) == 0:
            return float('inf')
            
        distance = (baseline_distance * np.sin(beta)) / np.sin(gamma)
        return distance
    
    def _calculate_angle(self, x_coordinate: float) -> float:
        """
        Calculate angle to point in image
        :param x_coordinate: x-coordinate of point in image
        :return: Angle in radians
        """
        relative_position = (2 * x_coordinate / self.image_width) - 1
        fov_rad = np.radians(self.fov)
        return np.arctan(relative_position * np.tan(fov_rad/2))
    
    def detect_reference_object(self, 
                              image: np.ndarray, 
                              template: Optional[np.ndarray] = None) -> Tuple[float, float]:
        """
        Detect reference object in image
        :param image: Input image
        :param template: Optional template image for template matching
        :return: (height_pixels, width_pixels) of detected object
        """
        if template is not None:
            # Use template matching
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            h, w = template.shape[:2]
            return h, w
        else:
            # Use simple edge detection for demonstration
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                # Find the largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                return h, w
            
        return 0, 0
    
    def visualize_distance(self, 
                         image: np.ndarray, 
                         bbox: Tuple[int, int, int, int], 
                         distance: float) -> np.ndarray:
        """
        Draw bounding box and distance on image
        :param image: Input image
        :param bbox: Bounding box (x, y, w, h)
        :param distance: Estimated distance
        :return: Image with visualization
        """
        x, y, w, h = bbox
        vis_image = image.copy()
        
        # Draw bounding box
        cv2.rectangle(vis_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw distance text
        text = f"Distance: {distance:.2f}m"
        cv2.putText(vis_image, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return vis_image

def calibrate_camera(images: List[np.ndarray], 
                    pattern_size: Tuple[int, int], 
                    square_size: float) -> dict:
    """
    Calibrate camera using chessboard pattern
    :param images: List of calibration images
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
    
    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
    
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
    
    return {
        'focal_length': focal_length,
        'image_width': gray.shape[1],
        'image_height': gray.shape[0],
        'fov': fov_x_deg
    }