from ultralytics import YOLO
import os
from functools import lru_cache

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "models",
    "urbaneye_best.pt"
)


@lru_cache(maxsize=1)
def load_yolo_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"YOLO model not found: {MODEL_PATH}"
        )

    return YOLO(MODEL_PATH)


def run_detection(image):
    model = load_yolo_model()

    # Smaller inference size to reduce RAM usage
    results = model.predict(
        source=image,
        imgsz=320,
        conf=0.25,
        device="cpu",
        verbose=False,
        max_det=10
    )

    result = results[0]
    boxes = result.boxes

    detections = []

    if boxes is not None:
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            class_name = model.names[cls]

            if class_name.lower() == "pothole":
                class_name = "Pothole"
            elif class_name.lower() == "garbage":
                class_name = "Garbage"
            else:
                class_name = class_name.title()

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

    recommended_action = (
        "No supported civic issue detected. "
        "Try a clearer image or a wider frame."
    )

    if detections:
        primary = max(
            detections,
            key=lambda d: d["confidence"]
        )

        if primary["class_name"] == "Pothole":
            if primary["severity"] == "High":
                recommended_action = (
                    "Dispatch road maintenance crew within 24 hours."
                )
            else:
                recommended_action = (
                    "Schedule asphalt patching crew within 3 to 5 days."
                )

        elif primary["class_name"] == "Garbage":
            if primary["severity"] in ["High", "Medium"]:
                recommended_action = (
                    "Schedule sanitation pickup and inspect nearby bins."
                )
            else:
                recommended_action = (
                    "Log for routine garbage clearance route."
                )

        else:
            recommended_action = (
                f"Review {primary['class_name']} manually "
                "before creating a civic issue."
            )

    return {
        "detections": detections,
        "recommended_action": recommended_action
    }