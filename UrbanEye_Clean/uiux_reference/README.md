# UrbanEye — Premium Civic Monitoring UI/UX Handoff

This package contains the polished visual reference screens and the implementation-ready specification for recreating UrbanEye in the existing Streamlit application.

## Visual references

| Screen | File | Primary purpose |
| --- | --- | --- |
| Dashboard | `urbaneye_dashboard.png` | City pulse, KPIs, trend, hotspots, recent alerts |
| AI Detection | `urbaneye_ai_detection.png` | Upload, YOLOv8n result, bounding boxes, confidence, action |
| Citizen Report | `urbaneye_citizen_report.png` | Photo, category, description, GPS/location, submit/status |
| Civic Map | `urbaneye_civic_map.png` | Map markers, filters, hotspots, selected issue drawer |
| Analytics | `urbaneye_analytics.png` | Trends, issue mix, severity, ward comparison, SLA |

## Implementation handoff

Read `urbaneye_uiux_spec.md` for the palette, typography, shell, reusable component contracts, screen-by-screen layout, Streamlit mapping, states, accessibility cues, and demo path. Read `urbaneye_visual_brief.md` for the original product and visual direction.

## Non-negotiable backend constraint

Keep the existing YOLOv8n inference and backend unchanged. AI detection is currently limited to **Pothole** and **Garbage**. The UI may support broader citizen-report categories, but it must not imply that the model detects unsupported categories.

## Suggested recreation order

Start with the shared shell and tokens, then build `KpiCard`, `ChartCard`, `StatusPill`, `IssueRow`, `UploadDropzone`, `DetectionOverlay`, `Timeline`, and `MapLegend`. Implement the Dashboard first, then connect AI Detection and Citizen Report to the existing inference/report flow, then add Civic Map and Analytics on top of the normalized issue data.
