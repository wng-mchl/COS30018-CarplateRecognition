# Import All the Required Libraries
import json
import cv2
import numpy as np
import math
import re
import os
import sqlite3
from datetime import datetime
from paddleocr import PaddleOCR
import torch
from torch.serialization import add_safe_globals
from ultralytics.nn.tasks import YOLOv10DetectionModel
from ultralytics import YOLOv10

# Allow loading custom model class from checkpoint
add_safe_globals({'ultralytics.nn.tasks.YOLOv10DetectionModel': YOLOv10DetectionModel})

# Create a Video Capture Object
cap = cv2.VideoCapture("data/carplate1.mp4")

# Load YOLOv10 Model
weights_path = "weights/best.pt"
model_obj = torch.load(weights_path, map_location="cpu", weights_only=False)
model = YOLOv10(model=model_obj)

# Initialize the frame count
count = 0

# Class Names
className = ["carplate"]

# Initialize the Paddle OCR
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)

# OCR Function
def paddle_ocr(frame, x1, y1, x2, y2):
    frame = frame[y1:y2, x1:x2]
    result = ocr.ocr(frame, det=False, rec=True, cls=False)
    text = ""
    for r in result:
        scores = r[0][1]
        if np.isnan(scores):
            scores = 0
        else:
            scores = int(scores * 100)
        if scores > 60:
            text = r[0][0]
    pattern = re.compile(r'[\W]')  # fixed invalid escape sequence warning
    text = pattern.sub('', text)
    text = text.replace("???", "")
    text = text.replace("O", "0")
    return str(text)

# Save Detected Plates
def save_json(license_plates, startTime, endTime):
    interval_data = {
        "Start Time": startTime.isoformat(),
        "End Time": endTime.isoformat(),
        "License Plate": list(license_plates)
    }
    os.makedirs("json", exist_ok=True)
    interval_file_path = "json/output_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".json"
    with open(interval_file_path, 'w') as f:
        json.dump(interval_data, f, indent=2)

    cummulative_file_path = "json/LicensePlateData.json"
    if os.path.exists(cummulative_file_path):
        with open(cummulative_file_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(interval_data)
    with open(cummulative_file_path, 'w') as f:
        json.dump(existing_data, f, indent=2)

    save_to_database(license_plates, startTime, endTime)

# Save to SQLite DB
def save_to_database(license_plates, start_time, end_time):
    conn = sqlite3.connect('Licenseplatedetection.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LicensePlates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            license_plate TEXT
        )
    ''')
    for plate in license_plates:
        cursor.execute('''
            INSERT INTO LicensePlates(start_time, end_time, license_plate)
            VALUES (?, ?, ?)
        ''', (start_time.isoformat(), end_time.isoformat(), plate))
    conn.commit()
    conn.close()

# Main Loop
startTime = datetime.now()
license_plates = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    currentTime = datetime.now()
    count += 1
    print(f"Frame Number: {count}")
    results = model.predict(frame, conf=0.45)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            classNameInt = int(box.cls[0])
            clsName = className[classNameInt]
            conf = math.ceil(box.conf[0] * 100) / 100
            label = paddle_ocr(frame, x1, y1, x2, y2)
            if label:
                license_plates.add(label)
            textSize = cv2.getTextSize(label, 0, fontScale=0.5, thickness=2)[0]
            c2 = x1 + textSize[0], y1 - textSize[1] - 3
            cv2.rectangle(frame, (x1, y1), c2, (255, 0, 0), -1)
            cv2.putText(frame, label, (x1, y1 - 2), 0, 0.5, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    if (currentTime - startTime).seconds >= 20:
        endTime = currentTime
        save_json(license_plates, startTime, endTime)
        startTime = currentTime
        license_plates.clear()

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break

cap.release()
cv2.destroyAllWindows()
