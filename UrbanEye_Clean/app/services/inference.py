import streamlit as st
from ultralytics import YOLO
import torch
import os
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "urbaneye_best.pt")

@st.cache_resource
def load_yolo_model():
    # Fallback to yolov8n.pt if urbaneye_best.pt doesn't exist
    if not os.path.exists(MODEL_PATH):
        alt_path = os.path.join(os.path.dirname(MODEL_PATH), "yolov8n.pt")
        if os.path.exists(alt_path):
            return YOLO(alt_path)
    return YOLO(MODEL_PATH)

def run_detection(image):
    model = load_yolo_model()
    device = 0 if torch.cuda.is_available() else "cpu"
    
    # Run prediction
    try:
        results = model.predict(
            image,
            imgsz=416,
            conf=0.25,
            device=device
        )
    except Exception as e:
        # Fallback to CPU if device=0 fails
        results = model.predict(
            image,
            imgsz=416,
            conf=0.25,
            device="cpu"
        )
        
    result_image = results[0].plot()
    boxes = results[0].boxes
    
    detections = []
    if boxes is not None:
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist() # bounding box [xmin, ymin, xmax, ymax]
            
            # Map names
            class_name = model.names[cls]
            # Standardize names to Title Case (e.g. Pothole, Garbage)
            if class_name.lower() == "pothole":
                class_name = "Pothole"
            elif class_name.lower() == "garbage":
                class_name = "Garbage"
            else:
                class_name = class_name.title()
                
            # Derive severity based on confidence
            if conf >= 0.75:
                severity = "High"
            elif conf >= 0.50:
                severity = "Medium"
            else:
                severity = "Low"
                
            detections.append({
                "class_name": class_name,
                "confidence": conf,
                "bbox": xyxy,
                "severity": severity
            })
            
    # Determine recommended action
    recommended_action = "No supported civic issue detected. Try a clearer image or a wider frame."
    if detections:
        # Sort by confidence descending to get primary issue
        sorted_detections = sorted(detections, key=lambda d: d["confidence"], reverse=True)
        primary = sorted_detections[0]
        
        if primary["class_name"] == "Pothole" and primary["severity"] == "High":
            recommended_action = "Dispatch road maintenance crew within 24 hours."
        elif primary["class_name"] == "Pothole":
            recommended_action = "Schedule asphalt patching crew within 3 to 5 days."
        elif primary["class_name"] == "Garbage" and primary["severity"] in ["High", "Medium"]:
            recommended_action = "Schedule sanitation pickup and inspect nearby bins."
        elif primary["class_name"] == "Garbage":
            recommended_action = "Log for routine garbage clearance route."
        else:
            recommended_action = f"Review {primary['class_name']} manually before creating a civic issue."
            
    return {
        "annotated_image": result_image,
        "detections": detections,
        "recommended_action": recommended_action
    }
