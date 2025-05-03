import cv2
import numpy as np
from scipy.spatial import distance
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
import json

@dataclass
class ReferenceObject:
    """Class for storing reference object information"""
    name: str
    actual_height: float
    actual_width: float
    template: Optional[np.ndarray] = None
    confidence_threshold: float = 0.7

class AdvancedDistanceEstimator:
    def __init__(self, camera_params: dict, reference_objects: List[ReferenceObject]):
        """
        Initialize the advanced distance estimator
        :param camera_params: Dictionary containing camera parameters
        :param reference_objects: List of known reference objects
        """
        self.camera_params = camera_params
        self.reference_objects = reference_objects
        self.error_correction = {
            'tilt_correction': True,
            'perspective_correction': True,
            'lighting_correction': True
        }
        
    def estimate_distance(self, 
                         image: np.ndarray,
                         method: str = 'size_based',
                         use_multiple_references: bool = True) -> Dict:
        """
        Estimate distance using multiple methods and reference objects
        :param image: Input image
        :param method: 'size_based' or 'triangulation'
        :param use_multiple_references: Whether to use multiple reference objects
        :return: Dictionary containing distance estimates and confidence scores
        """
        results = {
            'distances': [],
            'confidences': [],
            'reference_objects': [],
            'method_used': method
        }
        
        if method == 'size_based':
            for ref_obj in self.reference_objects:
                distance, confidence = self._size_based_estimation(image, ref_obj)
                if confidence > ref_obj.confidence_threshold:
                    results['distances'].append(distance)
                    results['confidences'].append(confidence)
                    results['reference_objects'].append(ref_obj.name)
        
        elif method == 'triangulation':
            # This would require two images, handled separately
            pass
        
        # Apply error correction
        if self.error_correction['tilt_correction']:
            results['distances'] = self._correct_tilt_error(results['distances'])
        if self.error_correction['perspective_correction']:
            results['distances'] = self._correct_perspective_error(results['distances'])
        
        # Calculate final distance
        if results['distances']:
            results['final_distance'] = np.average(
                results['distances'],
                weights=results['confidences']
            )
            results['confidence'] = np.mean(results['confidences'])
        else:
            results['final_distance'] = None
            results['confidence'] = 0.0
            
        return results
    
    def _size_based_estimation(self, 
                             image: np.ndarray,
                             ref_obj: ReferenceObject) -> Tuple[float, float]:
        """
        Perform size-based distance estimation with a single reference object
        :param image: Input image
        :param ref_obj: Reference object to use
        :return: (distance, confidence)
        """
        # Detect object
        if ref_obj.template is not None:
            height_pixels, width_pixels, confidence = self._template_matching(
                image, ref_obj.template
            )
        else:
            height_pixels, width_pixels, confidence = self._detect_by_features(
                image, ref_obj
            )
        
        if confidence < ref_obj.confidence_threshold:
            return float('inf'), 0.0
            
        # Calculate distance
        distance = (ref_obj.actual_height * self.camera_params['focal_length']) / height_pixels
        
        return distance, confidence
    
    def _template_matching(self, 
                         image: np.ndarray,
                         template: np.ndarray) -> Tuple[float, float, float]:
        """
        Detect object using template matching
        :param image: Input image
        :param template: Template image
        :return: (height_pixels, width_pixels, confidence)
        """
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        h, w = template.shape[:2]
        return h, w, max_val
    
    def _detect_by_features(self, 
                          image: np.ndarray,
                          ref_obj: ReferenceObject) -> Tuple[float, float, float]:
        """
        Detect object using feature matching
        :param image: Input image
        :param ref_obj: Reference object
        :return: (height_pixels, width_pixels, confidence)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return 0, 0, 0.0
            
        # Find the most likely contour based on aspect ratio
        best_contour = None
        best_confidence = 0.0
        expected_ratio = ref_obj.actual_width / ref_obj.actual_height
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            ratio = w / h
            
            # Calculate confidence based on aspect ratio similarity
            confidence = 1.0 - min(abs(ratio - expected_ratio) / expected_ratio, 1.0)
            
            if confidence > best_confidence:
                best_contour = contour
                best_confidence = confidence
        
        if best_contour is None:
            return 0, 0, 0.0
            
        x, y, w, h = cv2.boundingRect(best_contour)
        return h, w, best_confidence
    
    def _correct_tilt_error(self, distances: List[float]) -> List[float]:
        """
        Correct for camera tilt errors
        :param distances: List of estimated distances
        :return: Corrected distances
        """
        # Simple linear correction based on expected tilt error
        correction_factor = 1.0  # This should be calibrated
        return [d * correction_factor for d in distances]
    
    def _correct_perspective_error(self, distances: List[float]) -> List[float]:
        """
        Correct for perspective distortion
        :param distances: List of estimated distances
        :return: Corrected distances
        """
        # Simple quadratic correction for perspective
        correction_factor = 1.0  # This should be calibrated
        return [d * (1 + correction_factor * (d/10)**2) for d in distances]
    
    def save_calibration(self, filepath: str) -> None:
        """
        Save calibration parameters to file
        :param filepath: Path to save calibration file
        """
        calibration_data = {
            'camera_params': self.camera_params,
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