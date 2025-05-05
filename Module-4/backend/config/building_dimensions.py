import json
import os

def load_building_dimensions():
    """Load building dimensions from the JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dimensions_file = os.path.join(current_dir, 'building_dimensions.json')
    
    try:
        with open(dimensions_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Building dimensions file not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in building dimensions file") 