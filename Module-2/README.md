# Module 2: Landmark Recognition Model

## Model Overview
- Architecture: ResNet50
- Pretrained Weights: ImageNet
- Training Dataset: Campus Buildings (179 images)
- Classes: 12 building types

## Model Deployment
1. **API Endpoints**:
   ```python
   # Flask API for model inference
   from flask import Flask, request, jsonify
   from model_utils import BuildingDetector
   
   app = Flask(__name__)
   detector = BuildingDetector()
   
   @app.route('/predict', methods=['POST'])
   def predict():
       image = request.files['image']
       result = detector.detect_building(image)
       return jsonify(result)
   ```

2. **Batch Processing**:
   ```python
   # Batch inference example
   def process_batch(images):
       results = []
       for img in images:
           result = detector.detect_building(img)
           results.append(result)
       return results
   ```

## Model Optimization
1. **Quantization**:
   ```python
   # Quantize model for mobile deployment
   model_quantized = torch.quantization.quantize_dynamic(
       model, {torch.nn.Linear}, dtype=torch.qint8
   )
   ```

2. **Pruning**:
   ```python
   # Prune model weights
   parameters_to_prune = (
       (model.conv1, 'weight'),
       (model.layer1, 'weight'),
   )
   prune.global_unstructured(
       parameters_to_prune,
       pruning_method=prune.L1Unstructured,
       amount=0.2,
   )
   ```

## Performance Benchmarks
- Inference Time: ~50ms per image
- Accuracy: 92.5%
- Memory Usage: ~200MB
- Batch Processing: 32 images/second

## Integration with Module 3
```python
# Example integration with distance estimation
from model_utils import BuildingDetector
from advanced_distance_estimator import AdvancedDistanceEstimator

detector = BuildingDetector()
estimator = AdvancedDistanceEstimator()

def process_image(image):
    # Detect building
    detection = detector.detect_building(image)
    
    # Estimate distance
    if detection['success']:
        distance = estimator.estimate_distance(
            image,
            building_name=detection['building_name']
        )
        return {
            'building': detection['building_name'],
            'distance': distance,
            'confidence': detection['confidence']
        }
```

## Directory Structure
```
Module-2/
├── model/                    # Trained models
│   ├── resnet50_multiclass_building_detection_full.pth
│   └── resnet50_quantized.pth
├── notebooks/                # Jupyter notebooks
│   ├── model_training.ipynb
│   └── model_evaluation.ipynb
├── api/                     # API implementation
│   ├── app.py
│   └── requirements.txt
├── utils/                   # Utility scripts
│   ├── data_loader.py
│   └── model_utils.py
└── README.md
```

## Usage
1. **Train Model**:
   ```bash
   python train.py --epochs 50 --batch_size 32
   ```

2. **Evaluate Model**:
   ```bash
   python evaluate.py --model_path model/resnet50_multiclass_building_detection_full.pth
   ```

3. **Run API**:
   ```bash
   python api/app.py
   ```

## Notes
- Model optimized for mobile deployment
- Supports batch processing
- Includes error handling
- Provides confidence scores 