import numpy as np
from typing import List, Dict, Tuple
import json
import os

class TrilaterationService:
    def __init__(self, building_dimensions_file: str = 'building_dimensions.json'):
        self.building_positions = self._load_building_positions(building_dimensions_file)
    
    def _load_building_positions(self, file_path: str) -> Dict[str, Dict[str, float]]:
        """Load building positions from JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Building dimensions file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return {b['name']: {'lat': b['latitude'], 'lng': b['longitude']} 
                   for b in data if 'latitude' in b and 'longitude' in b}
    
    def estimate_position(self, distances: Dict[str, float]) -> Tuple[float, float]:
        """Estimate user position using trilateration."""
        try:
            # Get building positions and distances
            points = []
            radii = []
            
            for building_name, distance in distances.items():
                if building_name in self.building_positions:
                    points.append(self.building_positions[building_name])
                    radii.append(distance)
            
            if len(points) < 3:
                raise ValueError("At least 3 building distances required for trilateration")
            
            # Convert to numpy arrays
            points = np.array(points)
            radii = np.array(radii)
            
            # Calculate position using least squares method
            A = 2 * (points[1:] - points[0])
            b = (radii[0]**2 - radii[1:]**2 + 
                 np.sum(points[1:]**2, axis=1) - 
                 np.sum(points[0]**2))
            
            # Solve the system of equations
            position = np.linalg.lstsq(A, b, rcond=None)[0]
            
            return tuple(position)
            
        except Exception as e:
            print(f"Error in trilateration: {str(e)}")
            return None
    
    def get_building_position(self, building_name: str) -> Dict[str, float]:
        """Get the position of a specific building."""
        if building_name not in self.building_positions:
            raise ValueError(f"Building not found: {building_name}")
        return self.building_positions[building_name]
    
    def get_all_building_positions(self) -> Dict[str, Dict[str, float]]:
        """Get all building positions."""
        return self.building_positions 