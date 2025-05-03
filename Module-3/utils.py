import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from distance_estimator import DistanceEstimator

def plot_distance_accuracy(true_distances: List[float], 
                         estimated_distances: List[float],
                         method: str) -> None:
    """
    Plot accuracy of distance estimation
    :param true_distances: List of true distances
    :param estimated_distances: List of estimated distances
    :param method: Name of the estimation method
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(true_distances, estimated_distances, label='Measurements')
    plt.plot([min(true_distances), max(true_distances)], 
             [min(true_distances), max(true_distances)], 
             'r--', label='Perfect Estimation')
    plt.xlabel('True Distance (m)')
    plt.ylabel('Estimated Distance (m)')
    plt.title(f'Distance Estimation Accuracy - {method}')
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_error_metrics(true_distances: List[float],
                          estimated_distances: List[float]) -> dict:
    """
    Calculate error metrics for distance estimation
    :param true_distances: List of true distances
    :param estimated_distances: List of estimated distances
    :return: Dictionary of error metrics
    """
    errors = np.array(estimated_distances) - np.array(true_distances)
    absolute_errors = np.abs(errors)
    
    return {
        'mean_absolute_error': np.mean(absolute_errors),
        'root_mean_square_error': np.sqrt(np.mean(errors**2)),
        'max_error': np.max(absolute_errors),
        'min_error': np.min(absolute_errors),
        'std_error': np.std(errors)
    }

def visualize_triangulation(image1: np.ndarray,
                          image2: np.ndarray,
                          point1: Tuple[float, float],
                          point2: Tuple[float, float],
                          distance: float) -> None:
    """
    Visualize triangulation setup
    :param image1: First image
    :param image2: Second image
    :param point1: Point in first image
    :param point2: Point in second image
    :param distance: Estimated distance
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot first image
    ax1.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    ax1.plot(point1[0], point1[1], 'ro', markersize=10)
    ax1.set_title('First Image')
    
    # Plot second image
    ax2.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    ax2.plot(point2[0], point2[1], 'ro', markersize=10)
    ax2.set_title(f'Second Image (Distance: {distance:.2f}m)')
    
    plt.show()

def test_size_based_estimation(estimator: DistanceEstimator,
                             images: List[np.ndarray],
                             actual_heights: List[float],
                             true_distances: List[float]) -> None:
    """
    Test size-based distance estimation
    :param estimator: DistanceEstimator instance
    :param images: List of test images
    :param actual_heights: List of actual heights of objects
    :param true_distances: List of true distances
    """
    estimated_distances = []
    
    for img, actual_height in zip(images, actual_heights):
        # Detect object in image
        height_pixels, _ = estimator.detect_reference_object(img)
        
        # Estimate distance
        distance = estimator.size_based_distance(height_pixels, actual_height)
        estimated_distances.append(distance)
        
        # Visualize
        vis_img = estimator.visualize_distance(img, (0, 0, img.shape[1], height_pixels), distance)
        plt.figure(figsize=(8, 6))
        plt.imshow(cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB))
        plt.title(f'Estimated Distance: {distance:.2f}m')
        plt.show()
    
    # Plot accuracy
    plot_distance_accuracy(true_distances, estimated_distances, 'Size-based')
    
    # Calculate and print error metrics
    metrics = calculate_error_metrics(true_distances, estimated_distances)
    print("\nError Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}m")

def test_triangulation_estimation(estimator: DistanceEstimator,
                                image_pairs: List[Tuple[np.ndarray, np.ndarray]],
                                points_pairs: List[Tuple[Tuple[float, float], Tuple[float, float]]],
                                baseline_distances: List[float],
                                true_distances: List[float]) -> None:
    """
    Test triangulation-based distance estimation
    :param estimator: DistanceEstimator instance
    :param image_pairs: List of image pairs
    :param points_pairs: List of point pairs
    :param baseline_distances: List of baseline distances
    :param true_distances: List of true distances
    """
    estimated_distances = []
    
    for (img1, img2), (point1, point2), baseline in zip(image_pairs, points_pairs, baseline_distances):
        # Estimate distance
        distance = estimator.triangulation_distance(point1, point2, baseline)
        estimated_distances.append(distance)
        
        # Visualize
        visualize_triangulation(img1, img2, point1, point2, distance)
    
    # Plot accuracy
    plot_distance_accuracy(true_distances, estimated_distances, 'Triangulation-based')
    
    # Calculate and print error metrics
    metrics = calculate_error_metrics(true_distances, estimated_distances)
    print("\nError Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}m") 