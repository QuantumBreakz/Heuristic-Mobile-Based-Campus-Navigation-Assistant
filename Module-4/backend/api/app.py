import os
import sys
import logging
import json
import cv2
import torch
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from functools import wraps
import time

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.building_detection import BuildingDetector
from modules.distance_estimation import AdvancedDistanceEstimator
from modules.camera_calibration import CalibrationUtility
from utils.trilateration import TrilaterationService
from config.building_dimensions import load_building_dimensions

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Rate limiting configuration
RATE_LIMIT = int(os.getenv('RATE_LIMIT', '60'))  # requests per minute
rate_limit_data = {}

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        current_time = time.time()
        
        if ip not in rate_limit_data:
            rate_limit_data[ip] = {'count': 0, 'reset_time': current_time + 60}
        
        if current_time > rate_limit_data[ip]['reset_time']:
            rate_limit_data[ip] = {'count': 0, 'reset_time': current_time + 60}
        
        if rate_limit_data[ip]['count'] >= RATE_LIMIT:
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded. Please try again later.'
            }), 429
        
        rate_limit_data[ip]['count'] += 1
        return f(*args, **kwargs)
    return decorated_function

# Input validation functions
def validate_image_file(file):
    if not file:
        return False, 'No file provided'
    if not file.filename:
        return False, 'No filename provided'
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return False, 'Invalid file type. Only PNG, JPG, and JPEG are allowed'
    return True, None

def validate_calibration_params(pattern_size, square_size):
    if not isinstance(pattern_size, tuple) or len(pattern_size) != 2:
        return False, 'Invalid pattern size format'
    if not all(isinstance(x, int) and x > 0 for x in pattern_size):
        return False, 'Pattern size must be positive integers'
    if not isinstance(square_size, (int, float)) or square_size <= 0:
        return False, 'Square size must be a positive number'
    return True, None

# Initialize models and utilities
try:
    detector = BuildingDetector()
    distance_estimator = AdvancedDistanceEstimator()
    calibration_utility = CalibrationUtility()
    trilateration_service = TrilaterationService()
    logger.info("Models initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize models: {str(e)}")
    raise

# Load building dimensions from JSON file
BUILDING_DIMENSIONS = {}
try:
    with open('building_dimensions.json', 'r') as f:
        BUILDING_DIMENSIONS = json.load(f)
    logger.info("Building dimensions loaded successfully")
except FileNotFoundError:
    logger.warning("Building dimensions file not found")
except Exception as e:
    logger.error(f"Failed to load building dimensions: {str(e)}")

# Initialize additional models and utilities
try:
    model = torch.load('resnet50_multiclass_building_detection_full.pth')
    model.eval()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

# Load calibration data if exists
calibration_data = None
if os.path.exists('calibration_data.json'):
    with open('calibration_data.json', 'r') as f:
        calibration_data = json.load(f)
        logger.info("Calibration data loaded successfully")

@app.route('/api/detect', methods=['POST'])
@rate_limit
def detect_building():
    try:
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'success': False, 'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        # Read and process image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            logger.error("Failed to decode image")
            return jsonify({'success': False, 'error': 'Invalid image format'}), 400

        # Detect building
        detections = detector.detect(img)
        if not detections:
            logger.info("No buildings detected")
            return jsonify({'success': True, 'detections': []})

        # Add building dimensions to detections
        for detection in detections:
            building_id = detection['building_id']
            if building_id in BUILDING_DIMENSIONS:
                detection['dimensions'] = BUILDING_DIMENSIONS[building_id]
            else:
                logger.warning(f"No dimensions found for building {building_id}")
                detection['dimensions'] = None

        logger.info(f"Successfully detected {len(detections)} buildings")
        return jsonify({'success': True, 'detections': detections})

    except Exception as e:
        logger.error(f"Error in detect_building: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/triangulate', methods=['POST'])
@rate_limit
def triangulate_position():
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            logger.error("Missing image files in request")
            return jsonify({'success': False, 'error': 'Two images required'}), 400

        # Process first image
        file1 = request.files['image1']
        img1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
        if img1 is None:
            logger.error("Failed to decode first image")
            return jsonify({'success': False, 'error': 'Invalid first image format'}), 400

        # Process second image
        file2 = request.files['image2']
        img2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)
        if img2 is None:
            logger.error("Failed to decode second image")
            return jsonify({'success': False, 'error': 'Invalid second image format'}), 400

        # Get baseline distance from request
        baseline = float(request.form.get('baseline', 1.0))
        if baseline <= 0:
            logger.error("Invalid baseline distance")
            return jsonify({'success': False, 'error': 'Invalid baseline distance'}), 400

        # Estimate distance
        distance = distance_estimator.triangulate_distance(img1, img2, baseline, calibration_data)
        logger.info(f"Distance estimated: {distance} meters")
        return jsonify({'success': True, 'distance': distance})

    except Exception as e:
        logger.error(f"Error in triangulate_position: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/calibrate', methods=['POST'])
@rate_limit
def calibrate_camera():
    try:
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'success': False, 'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        # Read and process image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            logger.error("Failed to decode image")
            return jsonify({'success': False, 'error': 'Invalid image format'}), 400

        # Get calibration parameters
        pattern_size = tuple(map(int, request.form.get('pattern_size', '9,6').split(',')))
        square_size = float(request.form.get('square_size', 0.025))

        # Calibrate camera
        calibration_data = calibration_utility.calibrate_camera(img, pattern_size, square_size)
        logger.info("Camera calibrated successfully")

        # Save calibration data
        with open('calibration_data.json', 'w') as f:
            json.dump(calibration_data, f)

        return jsonify({'success': True, 'calibration_data': calibration_data})

    except Exception as e:
        logger.error(f"Error in calibrate_camera: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/position', methods=['POST'])
@rate_limit
def estimate_position():
    try:
        data = request.get_json()
        if not data or 'distances' not in data:
            return jsonify({'success': False, 'error': 'No distances provided'}), 400
        
        # Estimate position using trilateration
        position = trilateration_service.estimate_position(data['distances'])
        
        return jsonify({
            'success': True,
            'position': {
                'latitude': position[0],
                'longitude': position[1]
            }
        })
        
    except Exception as e:
        logger.error(f"Error in position estimation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buildings', methods=['GET'])
@rate_limit
def get_buildings():
    try:
        buildings = trilateration_service.get_all_building_positions()
        return jsonify({
            'success': True,
            'buildings': buildings
        })
    except Exception as e:
        logger.error(f"Error getting buildings: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
@rate_limit
def health_check():
    try:
        # Check if models are loaded
        if not hasattr(detector, 'model') or detector.model is None:
            logger.error("Building detection model not loaded")
            return jsonify({'status': 'error', 'message': 'Building detection model not loaded'}), 500

        if not hasattr(distance_estimator, 'model') or distance_estimator.model is None:
            logger.error("Distance estimation model not loaded")
            return jsonify({'status': 'error', 'message': 'Distance estimation model not loaded'}), 500

        if model is None:
            logger.error("Model not loaded")
            return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500

        logger.info("Health check passed")
        return jsonify({
            'status': 'ok',
            'model_loaded': True,
            'calibration_data': calibration_data is not None
        })

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', '5000')),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    ) 