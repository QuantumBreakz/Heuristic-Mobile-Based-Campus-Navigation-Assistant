import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import pandas as pd
import os

class BuildingDetector:
    def __init__(self, model_path='../Module-2/resnet50_multiclass_building_detection_full.pth'):
        """
        Initialize the building detector with the trained ResNet50 model.
        
        Args:
            model_path (str): Path to the trained model weights
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(model_path, map_location=self.device)
        self.model.eval()
        
        # Define image transformations
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Load building annotations
        self.annotations = self._load_annotations()
        self.class_names = self._get_unique_buildings()
        
        # Define standard dimensions for different types of buildings
        self.standard_dimensions = {
            'Block A: Admin Building': {'height': 20.0, 'width': 15.0},
            'Block B: Civil Department': {'height': 18.0, 'width': 12.0},
            'Block C: Old CS Department': {'height': 15.0, 'width': 10.0},
            'Block D: E&M Department': {'height': 16.0, 'width': 12.0},
            'Block E: Library': {'height': 25.0, 'width': 20.0},
            'Block F: New Building': {'height': 22.0, 'width': 18.0},
            'Highway': {'height': 0.0, 'width': 0.0},  # Not applicable
            'Main Garden': {'height': 0.0, 'width': 0.0},  # Not applicable
            'Old Cafe': {'height': 8.0, 'width': 10.0},
            'Parking': {'height': 0.0, 'width': 0.0},  # Not applicable
            'Juice Shop': {'height': 6.0, 'width': 8.0},
            'Gate Two': {'height': 4.0, 'width': 3.0},
            'Security Office': {'height': 5.0, 'width': 6.0},
            'Arm Wrestling Table': {'height': 1.0, 'width': 2.0},
            'Fountain': {'height': 3.0, 'width': 3.0},
            'Prayer Area': {'height': 0.0, 'width': 0.0},  # Not applicable
            'TennisCourt': {'height': 0.0, 'width': 0.0}  # Not applicable
        }
    
    def _load_annotations(self):
        """Load building annotations from Module-1's annotation.csv"""
        annotation_path = '../Module-1/annotation.csv'
        if os.path.exists(annotation_path):
            return pd.read_csv(annotation_path)
        else:
            raise FileNotFoundError(f"Annotation file not found at {annotation_path}")
    
    def _get_unique_buildings(self):
        """Get unique building names from annotations"""
        return sorted(self.annotations['label'].unique().tolist())
    
    def preprocess_image(self, image):
        """
        Preprocess the image for model input.
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            
        Returns:
            torch.Tensor: Preprocessed image tensor
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Convert to PIL Image
        image_pil = Image.fromarray(image_rgb)
        # Apply transformations
        image_tensor = self.transform(image_pil)
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        return image_tensor.to(self.device)
    
    def detect_building(self, image):
        """
        Detect and classify buildings in the image.
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            
        Returns:
            dict: Detection results including class, confidence, and bounding box
        """
        # Preprocess image
        image_tensor = self.preprocess_image(image)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Convert to numpy
        confidence = confidence.cpu().numpy()[0]
        predicted = predicted.cpu().numpy()[0]
        
        # Get building name
        building_name = self.class_names[predicted]
        
        # Get building dimensions
        dimensions = self.get_building_dimensions(building_name)
        
        # Get bounding box (you may need to adjust this based on your model)
        height, width = image.shape[:2]
        bbox = [0, 0, width, height]  # Full image as default
        
        return {
            'building_name': building_name,
            'confidence': float(confidence),
            'bbox': bbox,
            'dimensions': dimensions
        }
    
    def get_building_dimensions(self, building_name):
        """
        Get standard dimensions for known buildings.
        
        Args:
            building_name (str): Name of the building
            
        Returns:
            dict: Building dimensions (height, width)
        """
        return self.standard_dimensions.get(building_name, {'height': 15.0, 'width': 10.0})
    
    def is_building(self, building_name):
        """
        Check if the detected object is a building (has height and width).
        
        Args:
            building_name (str): Name of the detected object
            
        Returns:
            bool: True if it's a building, False otherwise
        """
        dimensions = self.get_building_dimensions(building_name)
        return dimensions['height'] > 0 and dimensions['width'] > 0 