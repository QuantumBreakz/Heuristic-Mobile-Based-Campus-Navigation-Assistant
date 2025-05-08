import cv2
import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List, Optional, Tuple
import os
import pickle
from pathlib import Path

class BuildingRecognizer:
    def __init__(self, features_dir: str = 'building_features'):
        self.features_dir = Path(features_dir)
        self.features_dir.mkdir(exist_ok=True)
        self.feature_centers = {}
        self.sift = cv2.SIFT_create()
        self.matcher = cv2.BFMatcher()
        self.feature_cache = {}
        self.load_building_features()

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better feature detection"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply histogram equalization
        equalized = cv2.equalizeHist(gray)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
        
        return blurred

    def extract_features(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Extract SIFT features from an image"""
        # Preprocess image
        processed = self._preprocess_image(image)
        
        # Detect keypoints and compute descriptors
        keypoints, descriptors = self.sift.detectAndCompute(processed, None)
        
        if descriptors is None:
            return np.array([]), np.array([])
        
        return keypoints, descriptors

    def _compute_feature_centers(self, building_name: str, descriptors: List[np.ndarray]) -> None:
        """Compute feature centers using K-means clustering"""
        if not descriptors:
            return
        
        # Combine all descriptors
        all_descriptors = np.vstack(descriptors)
        
        # Use K-means to find feature centers
        kmeans = KMeans(n_clusters=min(100, len(all_descriptors)), random_state=42)
        kmeans.fit(all_descriptors)
        
        # Store the centers
        self.feature_centers[building_name] = kmeans.cluster_centers_

    def load_building_features(self) -> None:
        """Load building features from disk"""
        for feature_file in self.features_dir.glob('*.pkl'):
            building_name = feature_file.stem
            try:
                with open(feature_file, 'rb') as f:
                    features = pickle.load(f)
                    self.feature_cache[building_name] = features
                    
                    # Compute feature centers if not already done
                    if building_name not in self.feature_centers:
                        self._compute_feature_centers(building_name, features)
            except Exception as e:
                print(f"Error loading features for {building_name}: {str(e)}")

    def save_building_features(self, building_name: str) -> None:
        """Save building features to disk"""
        if building_name in self.feature_cache:
            feature_file = self.features_dir / f"{building_name}.pkl"
            try:
                with open(feature_file, 'wb') as f:
                    pickle.dump(self.feature_cache[building_name], f)
            except Exception as e:
                print(f"Error saving features for {building_name}: {str(e)}")

    def recognize(self, features: Tuple[np.ndarray, np.ndarray]) -> Optional[str]:
        """Recognize a building from its features"""
        if not features[1].any():
            return None
        
        best_match = None
        best_score = 0
        
        for building_name, centers in self.feature_centers.items():
            # Match features against centers
            matches = self.matcher.knnMatch(features[1], centers, k=2)
            
            # Apply ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
            
            score = len(good_matches)
            if score > best_score:
                best_score = score
                best_match = building_name
        
        return best_match if best_score > 10 else None

    def train(self, image: np.ndarray, building_name: str) -> None:
        """Train the recognizer with a new image"""
        # Extract features
        keypoints, descriptors = self.extract_features(image)
        
        if descriptors is None or len(descriptors) == 0:
            raise ValueError("No features detected in the image")
        
        # Add features to cache
        if building_name not in self.feature_cache:
            self.feature_cache[building_name] = []
        self.feature_cache[building_name].append(descriptors)
        
        # Update feature centers
        self._compute_feature_centers(building_name, self.feature_cache[building_name])
        
        # Save features to disk
        self.save_building_features(building_name)

    def get_building_info(self, building_name: str) -> Dict:
        """Get information about a building's features"""
        if building_name not in self.feature_cache:
            return {
                "name": building_name,
                "feature_count": 0,
                "has_centers": False
            }
        
        return {
            "name": building_name,
            "feature_count": len(self.feature_cache[building_name]),
            "has_centers": building_name in self.feature_centers
        } 