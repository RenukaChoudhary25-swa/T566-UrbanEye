# UrbanEye — Premium Civic Monitoring UI/UX Specification

**Author:** Manus AI  
**Purpose:** Directly recreate the approved visual direction in the existing Streamlit UrbanEye application.  
**Backend constraint:** Keep the current YOLOv8n pipeline unchanged. AI detection remains limited to **Pothole** and **Garbage**.

> UrbanEye should feel like a municipal command center: calm, accountable, operational, and fast to scan. The interface is not a consumer social feed and should not behave like a generic analytics SaaS product.

## 1. Design principles

The interface is built around four principles. **Triage first** means the first viewport should expose volume, urgency, location, and recent changes without requiring navigation. **Evidence before action** means the AI Detection and Civic Map screens show the source image, location, confidence, severity, and recommended action together. **Status is explicit** means every issue has a visible lifecycle such as Pending, Assigned, or Resolved. **Progressive detail** means cards provide summary context while drawers and detail panels expose the full record.

The visual hierarchy should be driven by page title, one-line context, filters, primary metric cards, then investigation content. Use sentence case and short labels. Every chart needs a meaningful title, a visible unit or comparison, and a clear empty state.

## 2. Visual tokens

| Token | Value | Usage |
| --- | --- | --- |
| `color.ink` | `#10213D` | Primary text, headings, chart labels |
| `color.navy` | `#0B1730` | Sidebar, shell, high-contrast controls |
| `color.navy-2` | `#101F3D` | Secondary dark surfaces |
| `color.blue` | `#2563EB` | Primary action, active navigation, pothole series |
| `color.blue-soft` | `#EAF2FF` | Selection backgrounds, info banners |
| `color.orange` | `#F59E0B` | Garbage series, medium priority |
| `color.red` | `#D64545` | Critical/high priority, destructive/error |
| `color.green` | `#12805C` | Resolved, healthy, positive trend |
| `color.violet` | `#7357D8` | Analytics comparison accent |
| `color.surface` | `#F7F9FC` | App background |
| `color.card` | `#FFFFFF` | Cards and panels |
| `color.border` | `#E5EBF4` | Borders, dividers, input outlines |
| `radius.card` | `16px` | Main cards and drawers |
| `radius.control` | `10px` | Buttons, inputs, filter pills |
| `shadow.card` | `0 6px 22px rgba(16,33,61,.06)` | Subtle elevation |
| `space.page` | `28–32px` | Desktop content inset |
| `space.section` | `20–24px` | Vertical spacing between sections |

Use Inter or Source Sans 3. Headings use 600 weight, body copy 400, controls 500, and KPI values 700 with tabular numerals. A recommended desktop scale is 12 px metadata, 14 px body, 16 px card title, 22 px page title, and 34–40 px KPI value.

## 3. App shell

The desktop shell is a 248 px fixed left rail, a 64 px top bar, and a scrollable content area. The sidebar uses `#0B1730` and contains the UrbanEye mark at the top, the product descriptor “AI-Powered Urban Civic Monitoring,” five primary navigation items, and a bottom System health card. The active route uses a blue filled pill with white icon and label. Inactive items use white at approximately 86% opacity.

The top bar is white with a faint bottom border. It contains a menu icon at the left edge of content, then search, notification count, operator avatar, operator name, role, and a small dropdown chevron. On narrower screens, the sidebar collapses into a drawer and the top bar keeps only menu, notifications, and profile.

For Streamlit, use a single `st.session_state["active_page"]` value and a custom sidebar rendered once per rerun. Hide the default Streamlit menu and footer through CSS. Use `st.container()` and `st.columns()` for page structure, while using small HTML/CSS blocks only for decorative shells, KPI cards, pills, and compact status indicators.

## 4. Reusable component contract

| Component | Required content | Streamlit implementation | Interaction / state |
| --- | --- | --- | --- |
| `PageHeader` | Title, supporting sentence, optional actions | `st.columns([2.2, 1])` | Read-only or filter action |
| `FilterBar` | Date range, ward, source/status selectors | `st.columns()` + `st.selectbox()` | Writes filter state and reruns |
| `KpiCard` | Label, value, delta, comparison, icon | HTML/CSS card inside `st.container()` | Read-only |
| `ChartCard` | Title, subtitle, chart, empty/loading slot | `st.container()` + Plotly/Altair | Read-only, optional chart selector |
| `StatusPill` | Label and semantic color | Inline HTML/CSS or styled markdown | Read-only |
| `IssueRow` | Type, location, ward, timestamp, priority, status | `st.container(border=True)` | Click sets selected issue state |
| `AlertRow` | Icon, issue summary, time, severity | Compact `st.columns()` row | Click sets selected alert |
| `UploadDropzone` | Upload instructions, file rules, browse action | `st.file_uploader()` with custom wrapper | Empty, uploading, uploaded, error |
| `MediaPreview` | Image/video preview, filename, controls | `st.image()` / `st.video()` | Delete or replace file |
| `DetectionOverlay` | Source media plus bounding boxes and labels | Preserve existing YOLO result image; overlay only if already supported | Read-only after inference |
| `ConfidenceMeter` | Class name, numeric confidence, progress bar | HTML/CSS or `st.progress()` | Read-only |
| `RecommendedAction` | Action title, rationale, time window | Info-style card | Read-only |
| `LocationField` | Address, GPS action, optional map preview | `st.text_input()` + button | Writes location state |
| `Timeline` | Submitted, Triaged, Assigned, Resolved | Horizontal desktop / vertical mobile | Read-only status history |
| `MapLegend` | Type, priority, status keys | Positioned HTML/CSS overlay | Read-only |
| `EmptyState` | Icon, explanation, next action | Reusable card | Optional CTA |
| `LoadingSkeleton` | Placeholder rectangles for key content | CSS shimmer or static gray blocks | Shown while processing |
| `ErrorBanner` | What failed, recovery action | `st.error()` wrapped in styled container | Retry / clear action |
| `SuccessBanner` | Confirmed action, issue ID, next action | `st.success()` wrapped in styled container | Dismiss / open details |

Each component should accept a compact data object rather than reaching into global state. Use stable field names such as `issue_type`, `confidence`, `severity`, `status`, `ward`, `location_text`, `reported_at`, and `recommended_action`.

## 5. Dashboard screen

### Intended job
The Dashboard is the command-center overview. A municipal operator should understand volume, urgency, trend direction, geographic concentration, and the most recent alerts in under one minute.

### Layout

| Region | Desktop specification |
| --- | --- |
| Header | `Good morning, Ananya` and “Here’s the civic pulse across your city.” Right-aligned date, ward, and source filters |
| KPI strip | Four equal cards: Total issues, Potholes, Garbage, High priority |
| Row 2 left | Issue trend line chart for the selected range |
| Row 2 center | City hotspot map with Pothole, Garbage, and High priority legend |
| Row 2 right | Recent alerts list with “View all” |
| Row 3 left | Issue distribution donut for Pothole vs Garbage |
| Row 3 center/right | Optional expanded hotspot context or second alert block; keep the first viewport uncluttered |

The KPI cards should expose the value first, then the delta and comparison. Use blue for Potholes, orange for Garbage, and red for High priority. High-priority cards may use a faint red tint but should not use a red background across the entire card.

### Recommended sample data
Use illustrative data only: Total issues 1,284; Potholes 462; Garbage 611; High priority 84. The distribution chart should display the AI-supported classes only. If citizen reports contain a future category, place it in a separate “Other citizen reports” metric rather than implying the YOLOv8n model detects it.

### States
The loading state shows four KPI skeletons and chart placeholders. The empty state reads “No civic issues match these filters” and offers “Clear filters.” The error state identifies whether metrics or map data failed separately so a chart outage does not hide the rest of the dashboard.

## 6. AI Detection screen

### Intended job
The AI Detection screen turns an image or video into evidence-backed issue records without changing the existing inference code. It should make the model output understandable and actionable.

### Layout

| Region | Desktop specification |
| --- | --- |
| Header | Title “AI Detection” and subtitle “Detect and identify civic issues using AI” |
| Mode tabs | Image and Video tabs; keep the existing upload/inference behavior underneath |
| Main left panel | Upload dropzone, file row, media preview, bounding-box result, detection-complete footer |
| Main right panel | Detection summary, confidence meters, severity chips, recommended action, issue detail fields, Save as issue |
| Footer note | “YOLOv8n · Pothole + Garbage” to set correct expectations |

The result panel should show only the existing model classes: `Pothole` and `Garbage`. Each detection row includes confidence to two decimals, a semantic severity label, and a thin progress bar. Severity can be derived in the presentation layer from confidence plus configured business rules, but should not alter inference output.

### Recommended action rules

| Detection context | Suggested presentation copy |
| --- | --- |
| Pothole + high severity | “Dispatch road maintenance crew within 24 hours.” |
| Garbage + medium severity | “Schedule sanitation pickup and inspect nearby bins.” |
| Low confidence | “Review manually before creating a civic issue.” |
| No detection | “No supported civic issue detected. Try a clearer image or a wider frame.” |

The “Save as issue” button should serialize the model result into the existing issue schema or the lightest available persistence layer. If persistence is not yet implemented, show a success state with a temporary issue ID and clearly mark it as a demo record rather than silently failing.

## 7. Citizen Report screen

### Intended job
Citizen Report captures structured evidence from a resident while reducing the amount of typing required. The form should be clear for a first-time user and should not imply that AI has classified unsupported categories.

### Layout

Use a three-step progress strip: **Report details → Location → Review**. On desktop, place the uploaded photo card on the left and the form on the right. The form contains Category, Description, Location, GPS action, and a Live priority preview. The lower section contains a recent-submission status timeline with Submitted, Triaged, Assigned, and Resolved.

The category selector may include broader civic categories for citizen reporting, but the AI assist label must say that automatic detection is available only for Pothole and Garbage. If an unsupported category is selected, the form remains valid but the preview should switch to “Manual triage required.”

### Validation
Require a category, a non-empty description, and either a location string or GPS coordinate. Show inline validation near the field rather than only at the top of the page. Preserve form values on validation failure. Disable Submit report while the upload or location lookup is in progress.

### States
The empty state invites “Upload a photo to improve triage.” The uploading state shows filename, progress, and cancel. The success state includes the issue number, current status, and “Open on Civic Map.” The error state explains whether the failure came from upload, location, or submission and keeps the entered form data intact.

## 8. Civic Map screen

### Intended job
Civic Map is the spatial investigation workspace. It should help an operator find clusters, compare issue types, and open the details of a specific issue without losing map context.

### Layout

The map occupies most of the page, with a compact left filter drawer and a right selected-issue drawer. Filters include status—Pending, Assigned, Resolved—issue type—Pothole, Garbage—and priority—High, Medium, Low. The bottom-left legend distinguishes issue type, high priority, and resolved.

For a hackathon-ready Streamlit implementation, prefer `st.pydeck_chart` with an issue point layer and a second high-priority radius layer. Use a neutral basemap, not satellite imagery, to maintain the government dashboard tone. Clicking or selecting a row can update `st.session_state["selected_issue_id"]`; if full map click events are not available in the current setup, provide a synchronized issue list beside the map as a reliable fallback.

### Selected issue drawer

The drawer shows issue type and location in the title, then priority, ward, confidence score, status, assignment, report time, location, recommended action, and a primary “Open issue details” action. Keep the drawer under 360 px wide on desktop so the map remains the dominant workspace.

## 9. Analytics screen

### Intended job
Analytics supports weekly review, performance reporting, and ward-level prioritization. It is a decision-support page, not a chart gallery.

### Layout

The first row contains Resolution rate, Average response time, and SLA met. The second row contains Issues over time and Ward comparison. The third row contains Severity distribution and an Area-wise resolution table. Filters are Last 30 days, All wards, and Compare by area.

Use one consistent blue line for Potholes and orange for Garbage across the product. Use green only for positive operational outcomes, such as SLA met or resolved. Any rate must include its denominator or a subtitle clarifying its scope. For the area table, show Area, Open, Resolved, Average response, and SLA; make the SLA value semantic but not overpowering.

## 10. Responsive behavior

| Breakpoint | Behavior |
| --- | --- |
| 1280 px and above | Full 248 px sidebar, multi-column dashboard, map and alert cards visible together |
| 900–1279 px | Sidebar collapses to icon rail or drawer; KPI cards wrap to two columns; right drawers become overlays |
| Below 900 px | Single-column content, horizontal filter scroll, vertical timeline, map detail opens as bottom sheet |

Do not attempt to preserve every desktop card on mobile. Preserve the reading order: page header, filters, KPIs, primary evidence, then secondary analytics.

## 11. Streamlit implementation notes

Create one shared stylesheet loaded at the top of the app. Define CSS classes for `.ue-shell`, `.ue-card`, `.ue-kpi`, `.ue-pill`, `.ue-muted`, `.ue-sidebar`, `.ue-primary-button`, `.ue-drawer`, `.ue-empty`, and `.ue-skeleton`. Use `unsafe_allow_html=True` only for controlled static HTML generated from sanitized application data.

Use a thin page router rather than multiple unrelated Streamlit scripts. A recommended structure is:

```text
urbaneye/
├── app.py
├── ui/
│   ├── shell.py
│   ├── components.py
│   ├── charts.py
│   └── styles.py
├── pages/
│   ├── dashboard.py
│   ├── ai_detection.py
│   ├── citizen_report.py
│   ├── civic_map.py
│   └── analytics.py
├── services/
│   ├── inference.py      # existing YOLOv8n integration; do not rewrite
│   ├── issues.py
│   └── analytics.py
└── data/
    └── sample_issues.json
```

The existing YOLOv8n function should be wrapped, not replaced. The UI adapter should normalize its output into a presentation object such as:

```python
{
    "source_file": "ring_road_near_school.jpg",
    "detections": [
        {
            "issue_type": "Pothole",
            "confidence": 0.94,
            "bbox": [x1, y1, x2, y2],
            "severity": "High"
        },
        {
            "issue_type": "Garbage",
            "confidence": 0.88,
            "bbox": [x1, y1, x2, y2],
            "severity": "Medium"
        }
    ],
    "recommended_action": "Dispatch road maintenance crew within 24 hours."
}
```

Use `st.cache_data` for sample aggregations and `st.cache_resource` for the loaded model if the existing app does not already do so. Keep uploaded file bytes in session state only when needed for the current interaction. Avoid storing large raw videos in long-lived session state.

## 12. Interaction and feedback rules

Every primary action needs a visible response. Upload shows progress; inference shows a skeleton or spinner; Save as issue shows a success banner with issue ID; filters update the page without losing the current route; map selection opens a drawer; submission failure preserves user-entered values.

Use `st.status()` or a compact custom status line for multi-step inference. Prefer one primary button per card. Secondary actions should use an outlined button or low-emphasis text button. Dangerous actions such as Remove photo should not be red unless destructive confirmation is required.

## 13. Accessibility and trust cues

Maintain a minimum contrast ratio suitable for dark sidebar text and white content surfaces. Do not communicate state with color alone; pair semantic colors with labels such as High, Medium, Resolved, or Operational. Use descriptive labels for upload controls, visible focus states, and readable chart legends. Keep the model scope visible in AI Detection so users do not infer unsupported capabilities.

## 14. Hackathon demonstration path

For a live demo, use this sequence: open Dashboard to show the city pulse; switch to AI Detection and upload a sample image showing Pothole and Garbage bounding boxes; save the result as an issue; open Civic Map to show the new marker and selected-issue drawer; submit a Citizen Report with a photo and location; finish in Analytics to show the issue entering the trend and ward statistics. This path demonstrates the value chain without requiring a backend rewrite.

## 15. Definition of done

The design is ready for recreation when the app has one coherent shell, five routes, reusable cards and status components, correct AI scope, explicit loading/success/error/empty states, responsive behavior, and sample data that makes the dashboard feel operational. The visual reference set in this package should be treated as the north star for spacing, hierarchy, palette, and information density—not as a requirement to reproduce every generated label verbatim.
