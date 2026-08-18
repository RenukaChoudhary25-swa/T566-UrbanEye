from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.inference import run_detection

app = FastAPI(title="UrbanEye AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "online", "service": "UrbanEye AI"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        result = run_detection(image)

        # Convert non-JSON image object to a simple response.
        detections = result["detections"]

        return {
            "detections": detections,
            "recommended_action": result["recommended_action"],
            "count": len(detections),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))