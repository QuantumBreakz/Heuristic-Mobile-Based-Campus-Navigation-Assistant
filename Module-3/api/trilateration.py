import numpy as np
from typing import List, Tuple, Dict, Optional
import math
from dataclasses import dataclass
from scipy.optimize import least_squares
import json
from pathlib import Path

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0  # For 2D trilateration, z is always 0

@dataclass
class Landmark:
    name: str
    position: Point
    distance: float
    confidence: float = 1.0

class TrilaterationSolver:
    def __init__(self, calibration_file: str = 'trilateration_calibration.json'):
        self.calibration_file = Path(calibration_file)
        self.landmark_positions = self._load_landmark_positions()
        self.last_position = None
        self.position_history = []
        self.max_history = 10  # Keep last 10 positions for smoothing
        
    def _load_landmark_positions(self) -> Dict[str, Point]:
        """Load known landmark positions from calibration file"""
        if not self.calibration_file.exists():
            return {}
            
        try:
            with open(self.calibration_file, 'r') as f:
                data = json.load(f)
                return {
                    name: Point(**pos)
                    for name, pos in data.items()
                }
        except Exception as e:
            print(f"Error loading landmark positions: {str(e)}")
            return {}

    def _save_landmark_positions(self) -> None:
        """Save landmark positions to calibration file"""
        try:
            data = {
                name: {
                    'x': pos.x,
                    'y': pos.y,
                    'z': pos.z
                }
                for name, pos in self.landmark_positions.items()
            }
            with open(self.calibration_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving landmark positions: {str(e)}")

    def _distance(self, p1: Point, p2: Point) -> float:
        """Calculate Euclidean distance between two points"""
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2 +
            (p1.z - p2.z) ** 2
        )

    def _residuals(self, point: np.ndarray, landmarks: List[Landmark]) -> np.ndarray:
        """Calculate residuals for least squares optimization"""
        current_point = Point(point[0], point[1], point[2])
        residuals = []
        
        for landmark in landmarks:
            calculated_distance = self._distance(current_point, landmark.position)
            residual = calculated_distance - landmark.distance
            # Weight by confidence
            residuals.append(residual * landmark.confidence)
            
        return np.array(residuals)

    def _estimate_position(self, landmarks: List[Landmark]) -> Optional[Point]:
        """Estimate position using trilateration with least squares"""
        if len(landmarks) < 3:
            return None
            
        # Initial guess (use last known position or average of landmarks)
        if self.last_position:
            initial_guess = np.array([
                self.last_position.x,
                self.last_position.y,
                self.last_position.z
            ])
        else:
            initial_guess = np.array([
                np.mean([l.position.x for l in landmarks]),
                np.mean([l.position.y for l in landmarks]),
                0.0
            ])
            
        # Solve using least squares
        result = least_squares(
            self._residuals,
            initial_guess,
            args=(landmarks,),
            method='trf',
            loss='soft_l1'
        )
        
        if not result.success:
            return None
            
        return Point(
            x=result.x[0],
            y=result.x[1],
            z=result.x[2]
        )

    def _smooth_position(self, new_position: Point) -> Point:
        """Apply temporal smoothing to position estimates"""
        self.position_history.append(new_position)
        if len(self.position_history) > self.max_history:
            self.position_history.pop(0)
            
        # Calculate weighted average of recent positions
        weights = np.linspace(0.5, 1.0, len(self.position_history))
        weights /= weights.sum()
        
        x = sum(p.x * w for p, w in zip(self.position_history, weights))
        y = sum(p.y * w for p, w in zip(self.position_history, weights))
        z = sum(p.z * w for p, w in zip(self.position_history, weights))
        
        return Point(x, y, z)

    def update_landmark_position(self, name: str, position: Point) -> None:
        """Update the position of a known landmark"""
        self.landmark_positions[name] = position
        self._save_landmark_positions()

    def estimate_position(self, distances: Dict[str, float], confidences: Optional[Dict[str, float]] = None) -> Optional[Point]:
        """Estimate current position based on distances to landmarks"""
        # Create landmark objects with distances
        landmarks = []
        for name, distance in distances.items():
            if name not in self.landmark_positions:
                continue
                
            confidence = confidences.get(name, 1.0) if confidences else 1.0
            landmarks.append(Landmark(
                name=name,
                position=self.landmark_positions[name],
                distance=distance,
                confidence=confidence
            ))
            
        if len(landmarks) < 3:
            return None
            
        # Estimate position
        estimated_position = self._estimate_position(landmarks)
        if estimated_position is None:
            return None
            
        # Apply temporal smoothing
        smoothed_position = self._smooth_position(estimated_position)
        self.last_position = smoothed_position
        
        return smoothed_position

    def get_position_history(self) -> List[Point]:
        """Get the history of position estimates"""
        return self.position_history.copy()

    def reset_position_history(self) -> None:
        """Reset the position history"""
        self.position_history = []
        self.last_position = None 