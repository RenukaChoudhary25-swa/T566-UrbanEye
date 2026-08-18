import { UrbanIssue, Severity } from '@/data/mockData';

const API_URL = 'http://127.0.0.1:8000';

export interface DetectionResult {
  issue: string;
  category: string;
  confidence: number;
  severity: Severity;
  bbox: { x: number; y: number; w: number; h: number };
  recommendedAction: string;
  department: string;
}

export async function detectImage(file: File | Blob): Promise<DetectionResult> {
  try {
    const formData = new FormData();

    const imageFile =
      file instanceof File
        ? file
        : new File([file], "garbage-image.jpg", {
            type: file.type || "image/jpeg",
          });

    formData.append("file", imageFile);

    console.log("Sending image to:", `${API_URL}/detect`);
    console.log("Image:", imageFile.name, imageFile.type, imageFile.size);

    const response = await fetch(`${API_URL}/detect`, {
      method: "POST",
      body: formData,
    });

    console.log("Detection response status:", response.status);

    const responseText = await response.text();

    console.log("Detection response:", responseText);

    if (!response.ok) {
      throw new Error(
        `Detection failed: ${response.status} - ${responseText}`
      );
    }

    const data = JSON.parse(responseText);
    const detections = data.detections || [];

    if (detections.length === 0) {
      return {
        issue: "No Issue Detected",
        category: "None",
        confidence: 0,
        severity: "Low",
        bbox: { x: 0, y: 0, w: 0, h: 0 },
        recommendedAction:
          data.recommended_action ||
          "No supported civic issue detected.",
        department: "Urban Monitoring",
      };
    }

    const primary = [...detections].sort(
      (a, b) => b.confidence - a.confidence
    )[0];

    const [x1, y1, x2, y2] = primary.bbox || [0, 0, 0, 0];

    return {
      issue: primary.class_name,
      category: primary.class_name,
      confidence: Math.round(primary.confidence * 100),
      severity: primary.severity,
      bbox: {
        x: x1,
        y: y1,
        w: x2 - x1,
        h: y2 - y1,
      },
      recommendedAction:
        data.recommended_action ||
        "Review the detected civic issue.",
      department:
        primary.class_name === "Garbage"
          ? "Solid Waste Management"
          : primary.class_name === "Pothole"
          ? "Public Works Department"
          : "Urban Monitoring",
    };
  } catch (error) {
    console.error("DETECTION ERROR:", error);
    throw error;
  }
}

export interface ReportPayload {
  image?: File | Blob | null;
  description: string;
  category: string;
  location: string;
  lat?: number;
  lng?: number;
  severity?: Severity;
  department?: string;
}

export interface ReportReceipt {
  reportId: string;
  classification: string;
  severity: Severity;
  location: string;
  department: string;
  status: string;
}

export async function submitReport(
  payload: ReportPayload
): Promise<ReportReceipt> {

  const formData = new FormData();

  if (payload.image) {
    formData.append('file', payload.image);
  }

  formData.append('description', payload.description);
  formData.append('category', payload.category);
  formData.append('location', payload.location);

  if (payload.lat !== undefined)
    formData.append('lat', String(payload.lat));

  if (payload.lng !== undefined)
    formData.append('lng', String(payload.lng));

  const response = await fetch(`${API_URL}/report`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Report submission failed');
  }

  return await response.json();
}

export async function getIssues(): Promise<UrbanIssue[]> {
  const response = await fetch(`${API_URL}/issues`);

  if (!response.ok) {
    throw new Error('Failed to load issues');
  }

  return await response.json();
}

export async function updateIssue(
  id: string,
  status: UrbanIssue['status']
): Promise<UrbanIssue> {

  const response = await fetch(`${API_URL}/issues/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });

  if (!response.ok) {
    throw new Error('Failed to update issue');
  }

  return await response.json();
}

export interface AnalyticsSummary {
  total: number;
  critical: number;
  pending: number;
  resolved: number;
  aiDetections: number;
  hotspots: number;
}

export async function getAnalytics(): Promise<AnalyticsSummary> {
  const response = await fetch(`${API_URL}/analytics`);

  if (!response.ok) {
    throw new Error('Failed to load analytics');
  }

  return await response.json();
}

export function scorePriority(
  severity: Severity,
  confidence: number,
  impact: number
): number {
  const sev =
    severity === 'Critical' ? 40 :
    severity === 'High' ? 30 :
    severity === 'Medium' ? 18 : 8;

  return Math.min(
    100,
    sev +
      Math.round(confidence * 0.3) +
      Math.round(impact * 0.3)
  );
}