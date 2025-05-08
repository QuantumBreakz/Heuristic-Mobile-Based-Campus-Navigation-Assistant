from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize ResNet model
model = ResNet50(weights='imagenet')

# Building information database
BUILDINGS = {
    'main_block': {
        'name': 'Main Block',
        'description': 'Main administrative building of FAST-NUCES',
        'location': {'latitude': 24.9147, 'longitude': 67.0997}
    },
    'cs_block': {
        'name': 'CS Block',
        'description': 'Computer Science Department',
        'location': {'latitude': 24.9145, 'longitude': 67.0995}
    },
    'library': {
        'name': 'Library',
        'description': 'Central Library',
        'location': {'latitude': 24.9148, 'longitude': 67.0996}
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path):
    """Preprocess image for model input"""
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

def recognize_building(image_path):
    """Recognize building using ResNet model"""
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        
        # Make prediction
        predictions = model.predict(processed_img)
        
        # Get top prediction
        decoded_predictions = decode_predictions(predictions, top=1)[0]
        label = decoded_predictions[0][1]
        confidence = float(decoded_predictions[0][2])
        
        # Map prediction to building
        building_info = BUILDINGS.get(label, {
            'name': 'Unknown Building',
            'description': 'Building not recognized',
            'location': None
        })
        
        return {
            'building': building_info,
            'confidence': confidence
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """API endpoint for building recognition"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result = recognize_building(filepath)
            # Clean up uploaded file
            os.remove(filepath)
            return jsonify(result)
        except Exception as e:
            # Clean up uploaded file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/buildings', methods=['GET'])
def get_buildings():
    """API endpoint to get all buildings information"""
    return jsonify(BUILDINGS)

@app.route('/api/buildings/<building_id>', methods=['GET'])
def get_building(building_id):
    """API endpoint to get specific building information"""
    building = BUILDINGS.get(building_id)
    if building:
        return jsonify(building)
    return jsonify({'error': 'Building not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 