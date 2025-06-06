import cv2
import numpy as np
from scipy.spatial import distance
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
import json
from model_utils import BuildingDetector
from calibration_utils import CalibrationUtility

@dataclass
class ReferenceObject:
    """Class for storing reference object information"""
    name: str
    actual_height: float
    actual_width: float
    template: Optional[np.ndarray] = None
    confidence_threshold: float = 0.7

class AdvancedDistanceEstimator:
    def __init__(self, calibration_util, reference_objects=None):
        """
        Initialize the advanced distance estimator.
        
        Args:
            calibration_util (CalibrationUtility): Calibrated camera utility
            reference_objects (list, optional): List of reference objects
        """
        self.calibration_util = calibration_util
        self.reference_objects = reference_objects if reference_objects is not None else []
        self.error_correction = True
        self.building_detector = BuildingDetector()
        
    def estimate_distance(self, image, method='size_based', use_multiple_references=True):
        """
        Estimate distance to buildings in the image.
        
        Args:
            image (numpy.ndarray): Input image
            method (str): Estimation method ('size_based' or 'triangulation')
            use_multiple_references (bool): Whether to use multiple reference points
            
        Returns:
            dict: Distance estimation results
        """
        # Detect buildings in the image
        detection_results = self.building_detector.detect_building(image)
        
        if not self.building_detector.is_building(detection_results['building_name']):
            return {
                'success': False,
                'error': 'No building detected in the image',
                'building_name': detection_results['building_name']
            }
        
        # Get building dimensions
        dimensions = detection_results['dimensions']
        
        if method == 'size_based':
            return self._estimate_distance_size_based(image, dimensions)
        else:
            return self._estimate_distance_triangulation(image, dimensions)
    
    def _estimate_distance_size_based(self, image, dimensions):
        """
        Estimate distance using size-based method.
        
        Args:
            image (numpy.ndarray): Input image
            dimensions (dict): Building dimensions
            
        Returns:
            dict: Distance estimation results
        """
        # Get camera parameters
        camera_matrix = self.calibration_util.camera_matrix
        dist_coeffs = self.calibration_util.dist_coeffs
        
        # Undistort image
        undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)
        
        # Get image dimensions
        height, width = undistorted_image.shape[:2]
        
        # Calculate focal length in pixels
        focal_length_px = camera_matrix[0, 0]
        
        # Calculate apparent height in pixels
        # This is a simplified version - you might want to use more sophisticated
        # methods to measure the apparent height in the image
        apparent_height_px = height * 0.8  # Assuming building takes up 80% of image height
        
        # Calculate distance using similar triangles
        distance = (dimensions['height'] * focal_length_px) / apparent_height_px
        
        return {
            'success': True,
            'distance': distance,
            'building_height': dimensions['height'],
            'apparent_height_px': apparent_height_px,
            'focal_length_px': focal_length_px
        }
    
    def _estimate_distance_triangulation(self, image, dimensions):
        """
        Placeholder for backward compatibility. Use estimate_distance_triangulation instead.
        """
        return {
            'success': False,
            'error': 'Use estimate_distance_triangulation(image1, image2, baseline, building_name) for triangulation.',
            'building_name': dimensions['name'] if 'name' in dimensions else None
        }
    
    def estimate_distance_triangulation(self, image1, image2, baseline, building_name=None):
        """
        Estimate distance to a building using triangulation from two images.
        Args:
            image1 (np.ndarray): First image
            image2 (np.ndarray): Second image
            baseline (float): Distance between camera positions (meters)
            building_name (str, optional): Name of the building to detect (if known)
        Returns:
            dict: Distance estimation results
        """
        # Detect building in both images
        detection1 = self.building_detector.detect_building(image1)
        detection2 = self.building_detector.detect_building(image2)

        # Optionally filter by building name
        if building_name:
            if detection1['building_name'] != building_name or detection2['building_name'] != building_name:
                return {'success': False, 'error': 'Building not detected in both images'}

        # Get bounding box centers
        bbox1 = detection1['bbox']
        bbox2 = detection2['bbox']
        if bbox1 is None or bbox2 is None:
            return {'success': False, 'error': 'Bounding box not found in one or both images'}
        x1 = (bbox1[0] + bbox1[2]) / 2
        x2 = (bbox2[0] + bbox2[2]) / 2

        # Get focal length from calibration
        f = self.calibration_util.camera_matrix[0, 0]  # fx
        if f == 0:
            return {'success': False, 'error': 'Invalid focal length'}

        # Compute disparity
        disparity = abs(x1 - x2)
        if disparity == 0:
            return {'success': False, 'error': 'Zero disparity (object at infinity or identical positions)'}

        # Estimate distance
        distance = (baseline * f) / disparity
        corrected_distance = self._correct_distance(distance, min(detection1['confidence'], detection2['confidence']))
        return {
            'success': True,
            'distance_m': corrected_distance,
            'building_name': detection1['building_name'],
            'confidence1': detection1['confidence'],
            'confidence2': detection2['confidence'],
            'bbox1': bbox1,
            'bbox2': bbox2
        }
    
    def _correct_distance(self, distance, confidence):
        """
        Apply error correction to the estimated distance.
        
        Args:
            distance (float): Estimated distance
            confidence (float): Detection confidence
            
        Returns:
            float: Corrected distance
        """
        # Apply confidence-based correction
        corrected_distance = distance * (1.0 + (1.0 - confidence) * 0.1)
        
        # Apply quadratic correction for longer distances
        if corrected_distance > 50:
            correction_factor = 1.0 + (corrected_distance - 50) * 0.001
            corrected_distance *= correction_factor
        
        return corrected_distance
    
    def save_calibration(self, filepath: str) -> None:
        """
        Save calibration parameters to file
        :param filepath: Path to save calibration file
        """
        calibration_data = {
            'camera_params': self.calibration_util.camera_matrix,
            'dist_coeffs': self.calibration_util.dist_coeffs,
            'reference_objects': [
                {
                    'name': obj.name,
                    'actual_height': obj.actual_height,
                    'actual_width': obj.actual_width,
                    'confidence_threshold': obj.confidence_threshold
                }
                for obj in self.reference_objects
            ],
            'error_correction': self.error_correction
        }
        
        with open(filepath, 'w') as f:
            json.dump(calibration_data, f, indent=4)
    
    @classmethod
    def load_calibration(cls, filepath: str) -> 'AdvancedDistanceEstimator':
        """
        Load calibration from file
        :param filepath: Path to calibration file
        :return: AdvancedDistanceEstimator instance
        """
        with open(filepath, 'r') as f:
            calibration_data = json.load(f)
        
        reference_objects = [
            ReferenceObject(
                name=obj['name'],
                actual_height=obj['actual_height'],
                actual_width=obj['actual_width'],
                confidence_threshold=obj['confidence_threshold']
            )
            for obj in calibration_data['reference_objects']
        ]
        
        estimator = cls(calibration_data['camera_params'], reference_objects)
        estimator.error_correction = calibration_data['error_correction']
        
        return estimator 