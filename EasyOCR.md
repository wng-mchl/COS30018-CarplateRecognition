# EasyOCR License Plate Detection System

## Overview

This project implements a license plate detection and recognition system using:
- YOLOv8 for license plate detection
- EasyOCR for optical character recognition (OCR)
- OpenCV for image processing

The system processes images or video frames to:
1. Detect license plates using YOLO
2. Extract text from detected plates using EasyOCR
3. Visualize results with bounding boxes and confidence scores
4. Save results to CSV for analysis

## Requirements

- Python 3.7+
- Google Colab (recommended) or local environment with GPU
- Google Drive (for cloud storage)

## Dependencies

```bash
pip install ultralytics torch torchvision torchaudio easyocr opencv-python numpy
```

## Setup

1. Mount Google Drive:
```python
from google.colab import drive
drive.mount('/content/gdrive')
```

2. Configure paths in the notebook:
```python
INPUT_PATH = "/content/gdrive/My Drive/cos30018-test/data/images/val"
OUTPUT_PATH = "/content/gdrive/My Drive/cos30018-test/EasyOCR/PredictedImages"
RESULT_PATH = "/content/gdrive/My Drive/cos30018-test/EasyOCR/Result"
YOLO_MODEL_PATH = "/content/gdrive/My Drive/cos30018-test/yolov11/train_110525/runs/detect/train2/weights/best.pt"
```

## Usage

### Processing Images
```python
process_images()
```
Processes all images in the INPUT_PATH directory with optional image limit.

### Processing Videos
```python
process_video()
```
Processes video file specified in INPUT_PATH and saves annotated output.

### Key Features
- Visualizes detections with bounding boxes
- Displays both detection and OCR confidence scores
- Handles multiple license plates per image
- Saves results to CSV with detailed confidence metrics

## Output

Results include:
- Annotated images/videos with detections
- CSV file containing:
  - Source filename
  - Detected text
  - Number of plates detected
  - Timestamp
  - Detection confidence
  - OCR confidence
  - Detailed plate information

## Performance Notes

- For best performance, use GPU acceleration
- Processing time varies based on image size and number of plates
- The system includes error handling for missing files and processing failures

## Customization

Adjust these parameters for your use case:
- `IMAGE_LIMIT`: Set max number of images to process
- `SAVE_RESULTS`: Toggle saving of output images/videos
- `SAVE_CSV`: Toggle saving of CSV results
- YOLO detection thresholds (conf, iou)

## Troubleshooting

Common issues:
- File path errors: Verify all paths exist
- GPU unavailable: Runs slower on CPU
- Model loading failures: Check YOLO model path
- Memory issues: Reduce batch size or image limit