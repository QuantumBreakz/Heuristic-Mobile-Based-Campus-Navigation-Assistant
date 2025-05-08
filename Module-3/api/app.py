from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import math
from typing import Optional, List, Dict
import uvicorn
from pydantic import BaseModel
import io
from PIL import Image
import base64
import pandas as pd
import os
from building_recognition import BuildingRecognizer
from distance_estimator import DistanceEstimator
from trilateration import TrilaterationSolver, Point
from visualization import PositionVisualizer, VisualizationConfig

app = FastAPI(title="FastNUces Explorer API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recognizers
building_recognizer = BuildingRecognizer()
distance_estimator = DistanceEstimator()
trilateration_solver = TrilaterationSolver()

# Initialize visualizer
visualizer = PositionVisualizer(trilateration_solver)

# Load building data
def load_building_data():
    try:
        # Read the CSV file
        df = pd.read_csv('../Module-1/annotations/annotation.csv')
        
        # Extract unique locations and their coordinates
        buildings = {}
        for _, row in df.iterrows():
            location = row['label']
            if location not in buildings:
                # Extract coordinates from the location name
                # This is a simplified example - you'll need to implement proper coordinate extraction
                lat = 24.9147  # Example latitude
                lon = 67.0997  # Example longitude
                
                # Determine if it's a building or facility
                building_type = 'building' if 'Block' in location else 'facility'
                
                buildings[location] = {
                    'name': location,
                    'coordinates': {'latitude': lat, 'longitude': lon},
                    'type': building_type
                }
                
                # Add to trilateration solver
                trilateration_solver.update_landmark_position(
                    location,
                    Point(lat, lon)
                )
        
        return buildings
    except Exception as e:
        print(f"Error loading building data: {str(e)}")
        return {}

# Load building data
BUILDINGS = load_building_data()

class Location(BaseModel):
    latitude: float
    longitude: float

class CalibrationPoint(BaseModel):
    known_distance: float
    image: str  # base64 encoded image

class PositionUpdate(BaseModel):
    distances: Dict[str, float]
    confidences: Optional[Dict[str, float]] = None

@app.post("/recognize_building")
async def recognize_building(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    """Recognize buildings from images"""
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_np is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
        
        # Extract features
        features = building_recognizer.extract_features(image_np)
        
        # Recognize building
        building_name = building_recognizer.recognize(features)
        
        if building_name:
            building_info = BUILDINGS.get(building_name, {})
            return JSONResponse({
                "building": building_name,
                "type": building_info.get('type', 'unknown'),
                "coordinates": building_info.get('coordinates', {})
            })
        else:
            return JSONResponse({
                "building": None,
                "message": "No building recognized"
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estimate_distance")
async def estimate_distance(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    """Estimate distances to buildings"""
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_np is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
        
        # Estimate distance
        distance = distance_estimator.estimate_distance(
            image_np,
            (latitude, longitude)
        )
        
        return JSONResponse({
            "distance": float(distance),
            "unit": "meters"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_position")
async def update_position(update: PositionUpdate):
    """Update user position using trilateration"""
    try:
        # Estimate position using trilateration
        position = trilateration_solver.estimate_position(
            update.distances,
            update.confidences
        )
        
        if position is None:
            raise HTTPException(
                status_code=400,
                detail="Could not estimate position. Need at least 3 landmarks."
            )
        
        # Get position history for smoothing
        history = trilateration_solver.get_position_history()
        
        return JSONResponse({
            "position": {
                "latitude": position.x,
                "longitude": position.y
            },
            "history": [
                {"latitude": p.x, "longitude": p.y}
                for p in history
            ]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_buildings")
async def get_buildings():
    """Get information about all buildings"""
    return JSONResponse({
        "buildings": BUILDINGS
    })

@app.post("/train_building")
async def train_building(
    image: UploadFile = File(...),
    building_name: str = Form(...)
):
    """Train the building recognizer with new images"""
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_np is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
        
        # Train recognizer
        building_recognizer.train(image_np, building_name)
        
        return JSONResponse({
            "message": "Training successful",
            "building": building_name
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calibrate_distance")
async def calibrate_distance(calibration: CalibrationPoint):
    """Calibrate the distance estimator with a known distance"""
    try:
        # Convert base64 image to numpy array
        image_data = calibration.image.split(',')[1] if ',' in calibration.image else calibration.image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Convert RGB to BGR (OpenCV format)
        if len(image_np.shape) == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Calibrate the estimator
        success = distance_estimator.calibrate(calibration.known_distance, image_np)
        
        if success:
            return JSONResponse({
                "message": "Calibration successful",
                "focal_length": float(distance_estimator.focal_length)
            })
        else:
            raise HTTPException(status_code=400, detail="Calibration failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_building_types")
async def get_building_types():
    """Get all building types"""
    types = set(building['type'] for building in BUILDINGS.values())
    return JSONResponse({
        "types": list(types)
    })

@app.get("/get_buildings_by_type/{building_type}")
async def get_buildings_by_type(building_type: str):
    """Get buildings of a specific type"""
    buildings = {
        name: info for name, info in BUILDINGS.items()
        if info['type'] == building_type
    }
    return JSONResponse({
        "buildings": buildings
    })

@app.post("/update_landmark_position")
async def update_landmark_position(
    building_name: str,
    latitude: float,
    longitude: float
):
    """Update the position of a landmark in the trilateration system"""
    try:
        trilateration_solver.update_landmark_position(
            building_name,
            Point(latitude, longitude)
        )
        return JSONResponse({
            "message": "Landmark position updated successfully",
            "building": building_name,
            "position": {
                "latitude": latitude,
                "longitude": longitude
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_position_history")
async def get_position_history():
    """Get the history of position estimates"""
    history = trilateration_solver.get_position_history()
    return JSONResponse({
        "history": [
            {"latitude": p.x, "longitude": p.y}
            for p in history
        ]
    })

@app.post("/reset_position_history")
async def reset_position_history():
    """Reset the position history"""
    trilateration_solver.reset_position_history()
    return JSONResponse({
        "message": "Position history reset successfully"
    })

@app.get("/get_position_visualization")
async def get_position_visualization():
    """Get current position visualization as base64 encoded image"""
    try:
        plot_data = visualizer.get_current_plot()
        return JSONResponse({
            "plot": plot_data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_visualization_config")
async def update_visualization_config(
    figure_size: Optional[tuple] = None,
    dpi: Optional[int] = None,
    marker_size: Optional[int] = None,
    history_line_width: Optional[float] = None,
    update_interval: Optional[int] = None,
    show_grid: Optional[bool] = None,
    show_legend: Optional[bool] = None,
    show_confidence: Optional[bool] = None
):
    """Update visualization configuration"""
    try:
        # Create new config with updated values
        new_config = VisualizationConfig(
            figure_size=figure_size or visualizer.config.figure_size,
            dpi=dpi or visualizer.config.dpi,
            marker_size=marker_size or visualizer.config.marker_size,
            history_line_width=history_line_width or visualizer.config.history_line_width,
            update_interval=update_interval or visualizer.config.update_interval,
            show_grid=show_grid if show_grid is not None else visualizer.config.show_grid,
            show_legend=show_legend if show_legend is not None else visualizer.config.show_legend,
            show_confidence=show_confidence if show_confidence is not None else visualizer.config.show_confidence
        )
        
        # Update visualizer config
        visualizer.config = new_config
        
        # Recreate plot with new config
        visualizer.close()
        visualizer._setup_plot()
        
        return JSONResponse({
            "message": "Visualization configuration updated successfully",
            "config": {
                "figure_size": new_config.figure_size,
                "dpi": new_config.dpi,
                "marker_size": new_config.marker_size,
                "history_line_width": new_config.history_line_width,
                "update_interval": new_config.update_interval,
                "show_grid": new_config.show_grid,
                "show_legend": new_config.show_legend,
                "show_confidence": new_config.show_confidence
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 