import cv2
import numpy as np
import matplotlib.pyplot as plt
from advanced_distance_estimator import AdvancedDistanceEstimator
from calibration_utils import CalibrationUtility
import os

def test_camera_calibration():
    """Test camera calibration using chessboard pattern"""
    print("Testing camera calibration...")
    calib_util = CalibrationUtility()
    
    # Load calibration images
    calibration_images = []
    calibration_dir = 'calibration_images'
    if os.path.exists(calibration_dir):
        for img_file in os.listdir(calibration_dir):
            if img_file.endswith(('.jpg', '.png')):
                img_path = os.path.join(calibration_dir, img_file)
                img = cv2.imread(img_path)
                calibration_images.append(img)
    
    if not calibration_images:
        print("No calibration images found. Using default camera parameters.")
        return calib_util
    
    # Calibrate camera
    calib_util.calibrate_camera(
        calibration_images,
        pattern_size=(9, 6),
        square_size=0.025  # 2.5cm squares
    )
    
    print("Camera calibration successful!")
    return calib_util

def test_building_detection(estimator, test_image):
    """Test building detection and distance estimation"""
    print("\nTesting building detection and distance estimation...")
    
    # Estimate distance
    results = estimator.estimate_distance(test_image)
    
    if not results['success']:
        print(f"Error: {results['error']}")
        print(f"Detected object: {results['building_name']}")
        return
    
    # Display results
    print(f"Building detected: {results['building_name']}")
    print(f"Estimated distance: {results['distance']:.2f} meters")
    print(f"Building height: {results['building_height']:.2f} meters")
    print(f"Apparent height in pixels: {results['apparent_height_px']:.2f}")
    print(f"Focal length in pixels: {results['focal_length_px']:.2f}")
    
    # Visualize results
    plt.figure(figsize=(10, 6))
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    
    plt.subplot(122)
    undistorted = cv2.undistort(
        test_image,
        estimator.calibration_util.camera_matrix,
        estimator.calibration_util.dist_coeffs
    )
    plt.imshow(cv2.cvtColor(undistorted, cv2.COLOR_BGR2RGB))
    plt.title('Undistorted Image')
    
    plt.tight_layout()
    plt.show()

def main():
    """Main test function"""
    # Test camera calibration
    calib_util = test_camera_calibration()
    
    # Create distance estimator
    estimator = AdvancedDistanceEstimator(calib_util)
    
    # Test with sample images
    test_dir = 'test_images'
    if os.path.exists(test_dir):
        for img_file in os.listdir(test_dir):
            if img_file.endswith(('.jpg', '.png')):
                print(f"\nTesting with image: {img_file}")
                img_path = os.path.join(test_dir, img_file)
                test_image = cv2.imread(img_path)
                test_building_detection(estimator, test_image)
    else:
        print("No test images found. Please add images to the 'test_images' directory.")

if __name__ == "__main__":
    main() 