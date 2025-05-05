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

def test_triangulation(estimator, image1, image2, baseline, building_name=None):
    """Test triangulation-based distance estimation using two images and a known baseline."""
    print("\nTesting triangulation-based distance estimation...")
    results = estimator.estimate_distance_triangulation(image1, image2, baseline, building_name)
    if not results['success']:
        print(f"Error: {results['error']}")
        return
    print(f"Building detected: {results['building_name']}")
    print(f"Estimated distance (triangulation): {results['distance_m']:.2f} meters")
    print(f"Confidence (image 1): {results['confidence1']:.2f}")
    print(f"Confidence (image 2): {results['confidence2']:.2f}")
    # Visualize bounding boxes
    for idx, (img, bbox) in enumerate(zip([image1, image2], [results['bbox1'], results['bbox2']])):
        img_vis = img.copy()
        if bbox:
            cv2.rectangle(img_vis, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0,255,0), 2)
        plt.subplot(1,2,idx+1)
        plt.imshow(cv2.cvtColor(img_vis, cv2.COLOR_BGR2RGB))
        plt.title(f'Image {idx+1}')
    plt.suptitle('Triangulation Bounding Boxes')
    plt.show()

def main():
    """Main test function"""
    # Test camera calibration
    calib_util = test_camera_calibration()
    # Create distance estimator
    estimator = AdvancedDistanceEstimator(calib_util)
    # Test with sample images (size-based)
    test_dir = 'test_images'
    test_images = []
    if os.path.exists(test_dir):
        for img_file in sorted(os.listdir(test_dir)):
            if img_file.endswith(('.jpg', '.png')):
                img_path = os.path.join(test_dir, img_file)
                test_image = cv2.imread(img_path)
                test_images.append((img_file, test_image))
                print(f"\nTesting with image: {img_file}")
                test_building_detection(estimator, test_image)
    else:
        print("No test images found. Please add images to the 'test_images' directory.")
    # Triangulation test (requires at least 2 images and known baseline)
    if len(test_images) >= 2:
        print("\n--- Triangulation Test ---")
        baseline = 1.0  # meters (example, user should set actual value)
        print(f"Using baseline: {baseline} meter(s)")
        image1 = test_images[0][1]
        image2 = test_images[1][1]
        # Optionally, specify building_name if known
        test_triangulation(estimator, image1, image2, baseline)
    else:
        print("Not enough images for triangulation test. Add at least 2 images to 'test_images'.")

if __name__ == "__main__":
    main() 