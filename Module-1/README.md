# Module 1: Image Collection & Dataset Preparation

## Dataset Overview
- Total Images: 179
- Buildings Covered: 12
- Image Format: JPEG/PNG
- Resolution: 1920x1080

## Annotation Process
1. **Manual Annotation**:
   - Used LabelImg for bounding box annotation
   - Each building labeled with its official name
   - Multiple angles captured for each building

2. **Annotation Format**:
   ```csv
   image_name,label
   block_a_1.jpg,Block A: Admin Building
   block_b_1.jpg,Block B: Civil Department
   ```

3. **Challenges Addressed**:
   - Varying lighting conditions
   - Occlusions (trees, people)
   - Different viewing angles
   - Weather conditions

## Data Augmentation
Applied the following augmentations:
- Random rotation (±15 degrees)
- Brightness adjustment (±20%)
- Contrast adjustment (±20%)
- Horizontal flip
- Random crop

## Directory Structure
```
Module-1/
├── images/                # Original images
├── augmented_images/      # Augmented images
├── annotations/           # Annotation files
│   └── annotation.csv    # Main annotation file
├── dataset_description.txt
└── README.md
```

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