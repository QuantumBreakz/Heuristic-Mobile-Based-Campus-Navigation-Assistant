# Campus Navigation Assistant - Enhanced Distance Estimation Module

This module implements advanced distance estimation methods for the Campus Navigation Assistant project. It provides robust distance estimation using multiple reference objects and error correction techniques.

## Features

1. **Multiple Distance Estimation Methods**:
   - Size-based estimation using known reference objects
   - Triangulation-based estimation using multiple viewpoints
   - Combined approach using multiple reference objects

2. **Advanced Error Correction**:
   - Camera tilt correction
   - Perspective distortion correction
   - Lighting condition adaptation

3. **Robust Object Detection**:
   - Template matching for known objects
   - Feature-based detection for unknown objects
   - Confidence scoring for detection results

4. **Calibration Tools**:
   - Camera calibration using chessboard pattern
   - Reference object calibration
   - Calibration data persistence

## Requirements

Install the required packages using:
```bash
pip install -r requirements.txt
```

## Directory Structure

```
Module-3/
├── advanced_distance_estimator.py  # Core distance estimation implementation
├── calibration_utils.py            # Camera and reference object calibration
├── test_distance_estimation.py     # Test and demonstration script
├── requirements.txt                # Python dependencies
├── calibration_images/             # Camera calibration images
├── reference_objects/              # Reference object templates
└── test_images/                    # Test images for distance estimation
```

## Usage

### 1. Camera Calibration

```python
from calibration_utils import CalibrationUtility

# Create calibration utility
calib_util = CalibrationUtility()

# Calibrate camera using chessboard pattern
camera_params = calib_util.calibrate_camera(
    calibration_images,
    pattern_size=(9, 6),
    square_size=0.025  # 2.5cm squares
)
```

### 2. Reference Object Calibration

```python
# Add standard reference objects
calib_util.add_reference_object(
    name='standard_door',
    actual_height=2.1,  # Standard door height
    actual_width=0.9,   # Standard door width
    confidence_threshold=0.7
)

# Calibrate from image
calib_util.calibrate_reference_object(
    image=door_image,
    name='custom_door',
    actual_height=2.1,
    actual_width=0.9
)
```

### 3. Distance Estimation

```python
# Create estimator
estimator = calib_util.create_estimator()

# Estimate distance
results = estimator.estimate_distance(
    image=test_image,
    method='size_based',
    use_multiple_references=True
)

print(f"Distance: {results['final_distance']:.2f}m")
print(f"Confidence: {results['confidence']:.2f}")
```

## Error Correction

The module includes several error correction mechanisms:

1. **Camera Tilt Correction**:
   - Compensates for camera tilt using calibration data
   - Adjusts distance estimates based on tilt angle

2. **Perspective Correction**:
   - Corrects for perspective distortion
   - Uses quadratic correction for better accuracy at longer distances

3. **Lighting Adaptation**:
   - Adjusts detection thresholds based on lighting conditions
   - Improves robustness in varying environments

## Best Practices

1. **Camera Calibration**:
   - Use a high-quality chessboard pattern
   - Capture images from multiple angles
   - Ensure good lighting conditions

2. **Reference Objects**:
   - Use consistently sized objects
   - Document actual dimensions accurately
   - Include multiple reference objects for redundancy

3. **Image Capture**:
   - Maintain consistent camera height
   - Ensure good lighting
   - Minimize camera shake

4. **Error Handling**:
   - Check confidence scores
   - Use multiple reference objects
   - Consider environmental factors

## Integration with Other Modules

This module is designed to work seamlessly with:

1. **Landmark Recognition (Module 2)**:
   - Uses detected landmarks as reference points
   - Combines recognition confidence with distance estimation

2. **Mobile App (Module 4)**:
   - Provides distance estimates for localization
   - Supports real-time distance estimation
   - Includes error correction for mobile use

## Testing

Run the test script to verify the implementation:
```bash
python test_distance_estimation.py
```

## Notes

- Camera calibration is crucial for accurate results
- Use multiple reference objects for better accuracy
- Consider environmental factors in distance estimation
- Regular recalibration may be necessary for optimal performance 