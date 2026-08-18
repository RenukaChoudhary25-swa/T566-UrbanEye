from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import sys
import os
import uuid

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

# Temporary in-memory storage for prototype reports
reports = []


@app.get("/")
def health():
    return {
        "status": "online",
        "service": "UrbanEye AI"
    }


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        result = run_detection(image)

        detections = result["detections"]

        return {
            "detections": detections,
            "recommended_action": result["recommended_action"],
            "count": len(detections),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report")
async def submit_report(
    description: str = Form(""),
    category: str = Form("General"),
    location: str = Form("Unknown"),
    lat: float | None = Form(None),
    lng: float | None = Form(None),
    file: UploadFile | None = File(None),
):
    report_id = "URB-" + uuid.uuid4().hex[:8].upper()

    report = {
        "reportId": report_id,
        "classification": category,
        "severity": "Medium",
        "location": location,
        "department": (
            "Solid Waste Management"
            if category.lower() == "garbage"
            else "Public Works Department"
            if category.lower() == "pothole"
            else "Urban Monitoring"
        ),
        "status": "Pending",
        "description": description,
        "lat": lat,
        "lng": lng,
    }

    reports.append(report)

    return {
        "reportId": report_id,
        "classification": category,
        "severity": "Medium",
        "location": location,
        "department": report["department"],
        "status": "Pending",
    }


@app.get("/issues")
def get_issues():
    return reports


@app.put("/issues/{issue_id}")
async def update_issue(issue_id: str, payload: dict):
    for report in reports:
        if report["reportId"] == issue_id:
            report["status"] = payload.get(
                "status",
                report["status"]
            )
            return report

    raise HTTPException(
        status_code=404,
        detail="Issue not found"
    )


@app.get("/analytics")
def get_analytics():
    total = len(reports)

    return {
        "total": total,
        "critical": sum(
            1 for r in reports
            if r.get("severity") == "Critical"
        ),
        "pending": sum(
            1 for r in reports
            if r.get("status") == "Pending"
        ),
        "resolved": sum(
            1 for r in reports
            if r.get("status") == "Resolved"
        ),
        "aiDetections": total,
        "hotspots": min(total, 10),
    }