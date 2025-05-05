import torch
import cv2
import numpy as np
from torchvision import transforms
from PIL import Image

class BuildingDetector:
    def __init__(self, model_path='../models/resnet50_multiclass_building_detection_full.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(model_path, map_location=self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def detect(self, image):
        """Detect buildings in the image."""
        try:
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            
            # Preprocess image
            input_tensor = self.transform(image_pil)
            input_batch = input_tensor.unsqueeze(0).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                output = self.model(input_batch)
                probabilities = torch.nn.functional.softmax(output, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
            
            return {
                'building_id': predicted.item(),
                'confidence': confidence.item(),
                'class_name': self.get_building_name(predicted.item())
            }
            
        except Exception as e:
            print(f"Error in building detection: {str(e)}")
            return None
    
    def get_building_name(self, building_id):
        """Get building name from ID."""
        building_names = {
            0: "Main Building",
            1: "Science Center",
            2: "Library"
        }
        return building_names.get(building_id, "Unknown Building") 