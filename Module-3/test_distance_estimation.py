import cv2
import numpy as np
import matplotlib.pyplot as plt
from advanced_distance_estimator import AdvancedDistanceEstimator, ReferenceObject
from calibration_utils import CalibrationUtility
import os

def test_camera_calibration():
    """Test camera calibration using chessboard pattern"""
    # Create calibration utility
    calib_util = CalibrationUtility()
    
    # Load calibration images (replace with your calibration images)
    calibration_images = []
    calibration_folder = 'calibration_images/'
    if os.path.exists(calibration_folder):
        for filename in os.listdir(calibration_folder):
            if filename.endswith(('.jpg', '.png')):
                img = cv2.imread(os.path.join(calibration_folder, filename))
                if img is not None:
                    calibration_images.append(img)
    
    if calibration_images:
        # Calibrate camera
        camera_params = calib_util.calibrate_camera(
            calibration_images,
            pattern_size=(9, 6),  # Standard chessboard pattern
            square_size=0.025  # 2.5cm squares
        )
        print("Camera calibration successful!")
        print("Camera parameters:", camera_params)
    else:
        print("No calibration images found. Using default parameters.")
        camera_params = {
            'focal_length': 1000,
            'image_width': 1920,
            'image_height': 1080,
            'fov': 60
        }
    
    return calib_util, camera_params

def test_reference_object_calibration(calib_util: CalibrationUtility):
    """Test reference object calibration"""
    # Add standard reference objects
    calib_util.add_reference_object(
        name='standard_door',
        actual_height=2.1,  # Standard door height
        actual_width=0.9,   # Standard door width
        confidence_threshold=0.7
    )
    
    calib_util.add_reference_object(
        name='window',
        actual_height=1.2,  # Standard window height
        actual_width=1.0,   # Standard window width
        confidence_threshold=0.7
    )
    
    # Calibrate additional reference objects from images
    reference_folder = 'reference_objects/'
    if os.path.exists(reference_folder):
        for filename in os.listdir(reference_folder):
            if filename.endswith(('.jpg', '.png')):
                img = cv2.imread(os.path.join(reference_folder, filename))
                if img is not None:
                    try:
                        # Extract object name from filename
                        name = os.path.splitext(filename)[0]
                        calib_util.calibrate_reference_object(
                            image=img,
                            name=name,
                            actual_height=2.1,  # Example height
                            actual_width=0.9,   # Example width
                            confidence_threshold=0.7
                        )
                        print(f"Successfully calibrated reference object: {name}")
                    except ValueError as e:
                        print(f"Failed to calibrate {filename}: {str(e)}")

def test_distance_estimation(estimator: AdvancedDistanceEstimator):
    """Test distance estimation with sample images"""
    test_folder = 'test_images/'
    if not os.path.exists(test_folder):
        print("No test images found.")
        return
    
    for filename in os.listdir(test_folder):
        if filename.endswith(('.jpg', '.png')):
            img = cv2.imread(os.path.join(test_folder, filename))
            if img is not None:
                # Estimate distance
                results = estimator.estimate_distance(
                    image=img,
                    method='size_based',
                    use_multiple_references=True
                )
                
                # Display results
                print(f"\nResults for {filename}:")
                print(f"Final distance: {results['final_distance']:.2f}m")
                print(f"Confidence: {results['confidence']:.2f}")
                print("Reference objects used:", results['reference_objects'])
                
                # Visualize
                plt.figure(figsize=(10, 6))
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.title(f"Distance: {results['final_distance']:.2f}m (Confidence: {results['confidence']:.2f})")
                plt.show()

def main():
    # Test camera calibration
    calib_util, camera_params = test_camera_calibration()
    
    # Test reference object calibration
    test_reference_object_calibration(calib_util)
    
    # Create distance estimator
    estimator = calib_util.create_estimator()
    
    # Test distance estimation
    test_distance_estimation(estimator)
    
    # Save calibration
    calib_util.save_calibration('calibration_data.json')
    print("\nCalibration data saved to 'calibration_data.json'")

if __name__ == "__main__":
    main() 