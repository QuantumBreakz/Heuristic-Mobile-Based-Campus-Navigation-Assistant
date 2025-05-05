# Module 3: Distance Estimation

## Overview
This module implements distance estimation algorithms to calculate the distance between the user and detected buildings. It uses both size-based and triangulation-based approaches.

## Directory Structure
```
Module-3/
├── src/
│   ├── advanced_distance_estimator.py
│   ├── calibration_utils.py
│   └── building_dimensions.json
├── requirements.txt
└── README.md
```

## Features
- Size-based distance estimation using known building dimensions
- Triangulation-based distance estimation using multiple viewpoints
- Camera calibration utilities
- Building dimension database

## Algorithms
1. Size-based Estimation:
   - Uses known building dimensions
   - Calculates distance based on apparent size in image
   - Accounts for perspective distortion

2. Triangulation:
   - Uses multiple viewpoints
   - Calculates distance using geometric relationships
   - Improves accuracy with more viewpoints

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Calibrate camera:
   ```bash
   python src/calibration_utils.py
   ```

3. Estimate distance:
   ```python
   from src.advanced_distance_estimator import AdvancedDistanceEstimator
   
   estimator = AdvancedDistanceEstimator()
   distance = estimator.estimate_distance(image, building_id)
   ```

## Requirements
- Python 3.8+
- OpenCV
- NumPy
- SciPy
- Matplotlib

## Building Dimensions
Building dimensions are stored in `building_dimensions.json` with the following structure:
```json
{
  "building_id": {
    "height": float,
    "width": float,
    "depth": float,
    "floors": int
  }
} 