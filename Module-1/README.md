# Module 1: Image Collection & Dataset Preparation

## Overview
This module focuses on collecting and preparing the dataset for campus building recognition. It includes image collection, annotation, and dataset organization.

## Directory Structure
```
Module-1/
├── images/              # Raw building images
├── annotations/         # Annotation files
├── dataset_description.txt
└── README.md
```

## Dataset Details
- Total Images: 50-75 (5-15 images per building)
- Image Format: JPEG (.jpg) or PNG (.png)
- Resolution: Minimum 1920x1080
- Buildings Covered:
  - Main Academic Block
  - Central Library
  - Main Auditorium
  - Student Cafeteria
  - Sports Complex

## Annotation Format
Annotations are stored in `annotations.csv` with the following columns:
- image_path: Path to the image file
- building_id: Unique identifier for the building
- building_name: Name of the building
- x_min, y_min: Top-left coordinates of bounding box
- x_max, y_max: Bottom-right coordinates of bounding box

## Usage
1. Place raw images in the `images/` directory
2. Run annotation tool:
   ```bash
   python annotate.py
   ```
3. Generate dataset description:
   ```bash
   python generate_description.py
   ```

## Requirements
- Python 3.8+
- OpenCV
- LabelImg
- Pandas

## Challenges
- Varying lighting conditions
- Building obstructions
- Perspective variations
- Weather conditions

## Data Augmentation
Applied the following augmentations:
- Random rotation (±15 degrees)
- Brightness adjustment (±20%)
- Contrast adjustment (±20%)
- Horizontal flip
- Random crop

## Usage
1. **View Dataset**:
   ```bash
   python view_dataset.py
   ```

2. **Generate Augmented Images**:
   ```bash
   python augment_dataset.py
   ```

3. **Verify Annotations**:
   ```bash
   python verify_annotations.py
   ```

## Notes
- Images captured during daylight hours
- Multiple angles per building
- Consistent image resolution
- Proper lighting conditions maintained 