# UrbanEye — Visual Design Brief

## Product
UrbanEye is an AI-powered urban civic-monitoring dashboard for municipal operations teams. It detects and prioritizes civic issues from computer vision, citizen reports, GIS, and analytics. The existing YOLOv8n backend remains unchanged and currently supports only **Pothole** and **Garbage** detection.

## Audience and use context
The primary users are municipal command-center operators, ward officers, field supervisors, and civic administrators. The interface should support fast triage, investigation, assignment, and reporting on a large desktop monitor while remaining usable on a laptop or tablet-width viewport.

## Visual direction
The design language is premium municipal-tech: calm, precise, accountable, and operational rather than flashy. Use a deep navy application shell, cool white content surfaces, civic blue actions, indigo analytics accents, and semantic status colors. Cards are lightly elevated with 14–18 px radii, restrained borders, and minimal glass effects only in the top navigation and map overlays. Use generous whitespace, clear 8 px spacing rhythm, strong numerical hierarchy, and compact labels.

## Palette
- Ink navy: #0B1730
- Deep navy: #101F3D
- Civic blue: #2563EB
- Electric blue accent: #4F7CFF
- Sky tint: #EAF2FF
- Surface: #F7F9FC
- Card: #FFFFFF
- Text: #10213D
- Muted text: #6B7B95
- Border: #E5EBF4
- Success: #12805C
- Warning: #C57A10
- Critical: #D64545
- Violet analytics: #7357D8

## Typography
Use Inter or Source Sans 3. Headings are semibold with tight tracking, body copy is regular, numeric KPI values are bold and tabular. Prefer sentence case. Avoid all-caps except tiny overline labels.

## Global shell
A left rail at 248 px on desktop contains the UrbanEye mark, workspace selector, primary navigation, and a compact “System health” module. A top bar contains the current page title, date/range selector, search, notifications, and the operator profile. Main content uses a max width around 1440 px with 28–32 px page padding.

## Screens to visualize
1. **Dashboard** — KPI strip for Total issues, Potholes, Garbage, and High priority; 14-day issue trend; issue distribution; map hotspot panel; recent alerts list; filter chips for date, ward, and source.
2. **AI Detection** — upload zone with Image/Video tabs; preview panel with bounding boxes for Pothole and Garbage; detection metadata with confidence and severity; recommended action card; “Save as issue” path.
3. **Citizen Report** — photo upload, category selector, description field, location/GPS field, priority preview, submission success and status timeline.
4. **Civic Map** — full-width dark-neutral map canvas with issue markers, cluster hotspot, left filter drawer, right selected-issue detail drawer, legend for priority and status.
5. **Analytics** — issue mix, weekly trend, severity breakdown, ward comparison, resolution SLA summary, and area-wise table.

## Reusable components
App shell, navigation item, page header, filter bar, KPI card, trend chart card, distribution card, status pill, issue row, alert row, map marker, map legend, upload dropzone, media preview, bounding-box overlay, confidence meter, severity badge, recommended-action card, form field, location field, step timeline, chart card, empty state, loading skeleton, success banner, error banner, and responsive drawer.

## UX constraints
The visuals should communicate that only Pothole and Garbage are AI-detected today; other future categories may appear in report filters but should not be implied as current model outputs. Use realistic sample data, but treat it as illustrative. Avoid excessive gradients, decorative city imagery, dense tables, and decorative charts with no operational purpose.

## Mockup generation brief
Create a premium visual product mockup showing the UrbanEye municipal dashboard as a coherent five-screen design system. Use realistic interface text and labels, consistent shell, clear hierarchy, readable cards, restrained navy/blue palette, subtle shadows, and a desktop-first 16:10 presentation. Include the Dashboard, AI Detection, Citizen Report, Civic Map, and Analytics views in a polished multi-screen board, with enough detail to communicate layout and components. Avoid unreadable tiny text, fake logos, excessive glow, and generic SaaS gradients.
