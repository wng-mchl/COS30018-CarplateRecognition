# CRNN
This part provides instructions on how to set up and run the `crnn.ipynb` notebook for license plate recognition.

## 1. Prerequisites / Requirements

Before running the notebook, ensure you have the following:

*   **Google Colab Environment:**
    *   A Google account.
    *   GPU is highly recommended for faster CRNN inference.
*   **Google Drive Account:**
    *   Sufficient storage space for datasets, pre-trained models, and outputs.
*   **Python Libraries (Installed by the notebook):**
    *   `torch`, `torchvision`, `tqdm`
    *   `ultralytics`
    *   `python-Levenshtein`
    *   `pandas`
    *   `matplotlib`
    *   `opencv-python` (for `cv2`)
    *   `numpy`
    *   `tensorflow` (primarily for EfficientDet, if used)
*   **Dataset:**
    *   **Training Images:** Images containing license plates.
    *   **Training/Validation Annotations:** CVAT XML format.
        *   `annotations_main.xml`: For the training set and validation set used during CRNN training.
        *   `annotations_val.xml`: For the validation set used standalone during CRNN evaluation.
        *   Annotations should have bounding boxes labeled `carplate` and an attribute `plate_number` containing the ground truth text for each plate.
    *   **Test Images/Videos:** Sample images and videos for testing the full end-to-end pipeline.
*   **Pre-trained Object Detection Models:**
    *   You'll need at least one pre-trained object detection model. The notebook supports:
        *   YOLOv11 (Ultralytics format)
        *   YOLOv10 (Ultralytics format, or a compatible structure)
        *   EfficientDet (TensorFlow SavedModel format)
    *   These models should be downloaded or trained separately and stored in your Google Drive. Their paths are configured in the "Path Setup" section of the notebook.

## 2. Installation / Getting Started

Follow these steps to set up and prepare the notebook:

1.  **Upload to Colab:**
    *   Upload the `crnn.ipynb` notebook to your Google Colab environment.

2.  **Google Drive Setup:**
    *   Create a main project folder in your Google Drive. The notebook defaults to a base structure like `/content/gdrive/MyDrive/cos30018-test/`. **You must adapt the paths in the notebook if your structure differs.**
    *   Inside your main project folder, organize your data and models. A recommended structure (matching the notebook's default paths) is:
        ```
        MyDrive/
        └── cos30018-test/  # Or your chosen main project folder
            ├── CRNN_CTC_Loss/              # Main output directory for CRNN
            │   ├── cropped_images/         # Auto-generated
            │   ├── cropped_images_val/     # Auto-generated
            │   ├── labels.csv              # Auto-generated
            │   ├── labels_val.csv          # Auto-generated
            │   ├── crnn_best_model.pth     # Auto-generated
            │   └── od_crnn_predictions/    # Output for end-to-end pipeline
            │       ├── yolov11/
            │       ├── yolov10/
            │       └── efficientdet/
            ├── data/
            │   ├── annotations_main.xml
            │   ├── annotations_val.xml
            │   └── images/
            │       ├── train/              # Your training images
            │       └── val/                # Your validation images
            ├── yolov11/                    # Your YOLOv11 model files
            │   └── .../weights/best.pt
            ├── PaddleOCR/PaddleOCR/weights/ # Example path for YOLOv10
            │   └── best.pt
            ├── efficientdetd0/             # Your EfficientDet model files
            │   └── saved_model/
            ├── test_image/                 # Sample images for testing pipeline
            │   └── ...
            └── test_video/                 # Sample videos for testing pipeline
                └── ...
        ```

3.  **Modify Paths (CRITICAL):**
    *   Open the `crnn.ipynb` notebook in Colab.
    *   Navigate to the **"Path Setup"** cell.
    *   **Carefully review and update all paths** (`output_path`, `training_annotations_xml_path`, `yolov11_model_path`, etc.) to accurately point to your files and folders within Google Drive. Incorrect paths are the most common source of errors.

4.  **Select Object Detection Model:**
    *   In the **"Load Models and Run Processing"** section (near the end of the notebook):
        *   Uncomment the lines for the Object Detection (OD) model you wish to use (e.g., YOLOv11, YOLOv10, or EfficientDet).
        *   Ensure the `od_model_to_use_path` variable points to the correct location of your chosen pre-trained OD model in Google Drive.
        ```python
        # Example for YOLOv11:
        od_model_to_use_path = yolov11_model_path
        current_od_model_name = "yolov11"

        # Example for EfficientDet (uncomment if using):
        # od_model_to_use_path = efficientdet_model_path
        # current_od_model_name = "efficientdet"
        ```

## 3. Usage / How to Run

Execute the cells in the `crnn.ipynb` notebook sequentially within your Google Colab environment.

**General Workflow:**

1.  **Mount Google Drive & Install Dependencies:**
    *   Run the first few cells to connect to your Google Drive and install the necessary Python packages.

2.  **Path Setup & Configuration:**
    *   The notebook will verify the paths you've set. **Ensure all paths are correct.**
    *   Output directories will be created if they don't exist.

3.  **Data Preparation (Parse CVAT XML & Process Cropped Images):**
    *   These cells parse your CVAT XML annotations.
    *   They then crop the license plate regions from your training and validation images.
    *   Cropped images are saved to `cropped_image_path` and `cropped_image_val_path`.
    *   `labels.csv` and `labels_val.csv` are generated, mapping cropped images to their plate numbers for CRNN training.
    *   *This step will be skipped if the cropped images and label CSVs already exist in the specified output paths.*

4.  **CRNN Model Training:**
    *   Cells define hyperparameters, the CRNN dataset class, the CRNN model architecture, data augmentations, and training/validation functions.
    *   Running the "Training Model" cells will start the CRNN training process. This can take a significant amount of time, especially with a large dataset and many epochs.
    *   The best performing CRNN model (based on validation loss) will be saved to `best_model_path` (e.g., `crnn_best_model.pth`).
    *   Training and validation loss/accuracy curves will be plotted and saved.

5.  **CRNN Inference Evaluation (Standalone):**
    *   After training, you can evaluate the CRNN model's performance on the *standalone validation set of cropped plates*.
    *   The "Inference on Test Set and Save Predictions to CSV" section loads the best CRNN model.
    *   It processes each cropped validation image, displays it with its true vs. predicted label, and calculates individual metrics (exact match, edit distance).
    *   Overall CRNN performance metrics (Exact Match Accuracy, Character Error Rate) are printed.
    *   Predictions are saved to `predictions_csv_path`.

6.  **End-to-End LPR Pipeline (Object Detection + CRNN Inference):**
    *   The final sections of the notebook ("Object Detection and CRNN Inference", "Image Processing", "Video Processing", "Load Models and Run Processing") set up and run the full pipeline.
    *   Ensure you have selected your desired OD model (Step 2.4 above).
    *   The script will:
        *   Load the chosen OD model and the trained CRNN recognizer.
        *   Process sample images and/or videos specified in the "Test Cases" subsection within "Load Models and Run Processing".
            *   Example test image folder: `/content/gdrive/MyDrive/cos30018/test_image`
            *   Example test video file: `/content/gdrive/MyDrive/cos30018/20250426070025_041707.TS`
            *   **Modify these sample paths to your own test data.**
        *   For each image/video frame:
            1.  The OD model detects license plates.
            2.  Detected plates are cropped.
            3.  The CRNN model recognizes characters on the cropped plate.
            4.  (For video) Tracking and text smoothing are applied.
            5.  Annotated images/frames are displayed in Colab and saved to a subdirectory within `annotated_output_path` (e.g., `od_crnn_predictions/yolov11/images/` or `od_crnn_predictions/yolov11/videos/`).
