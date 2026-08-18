import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import os

from app.services.issues import load_issues, update_issue_status
from app.ui.components import status_pill, priority_pill, action_card
from app.ui.shell import render_topbar

def generate_leaflet_html(issues, center_lat, center_lon, zoom):
    markers_js = ""
    for idx, i in enumerate(issues):
        lat = i.get("latitude")
        lon = i.get("longitude")
        if not lat or not lon:
            continue
            
        p = i.get("priority", "Medium")
        s = i.get("status", "Pending")
        
        # Color coding
        if s == "Resolved":
            color = "#12805C" # Green
        elif p == "Critical" or p == "High":
            color = "#D64545" # Red
        elif p == "Medium":
            color = "#F59E0B" # Orange
        else:
            color = "#10B981" # Emerald Green
            
        # Binds popup content
        popup_html = f"""
        <div style="font-family: \'Inter\', sans-serif; font-size: 12px; color: #10213D; line-height: 1.4; min-width: 160px;">
            <div style="font-weight: 700; font-size: 13px; color: #10B981; margin-bottom: 4px;">{i.get('id')}</div>
            <div style="margin-bottom: 2px;"><strong>Type:</strong> {i.get('type')}</div>
            <div style="margin-bottom: 2px;"><strong>Status:</strong> {s}</div>
            <div style="margin-bottom: 2px;"><strong>Priority:</strong> {p}</div>
            <div style="margin-top: 4px; font-size: 11px; color: #6B7B95;">{i.get('location_text')}</div>
        </div>
        """
        # Escape single quotes and newlines
        popup_html = popup_html.replace("\n", "").replace("'", "\\'")
        
        # Add glowing animation for Critical / High active issues
        glow_js = ""
        if (p == "Critical" or p == "High") and s != "Resolved":
            glow_js = f"""
            L.circleMarker([{lat}, {lon}], {{
                radius: 16,
                fillColor: '{color}',
                color: '{color}',
                weight: 0,
                fillOpacity: 0.2,
                className: 'glow-marker'
            }}).addTo(map);
            """
            
        markers_js += f"""
        {glow_js}
        L.circleMarker([{lat}, {lon}], {{
            radius: 8,
            fillColor: '{color}',
            color: '#FFFFFF',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.95
        }}).addTo(map).bindPopup('{popup_html}');
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            html, body, #map {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background: #F7F9FC;
            }}
            .glow-marker {{
                animation: pulse 1.8s infinite ease-in-out;
            }}
            @keyframes pulse {{
                0% {{
                    transform: scale(0.6);
                    opacity: 0.1;
                }}
                50% {{
                    transform: scale(1.2);
                    opacity: 0.5;
                }}
                100% {{
                    transform: scale(0.6);
                    opacity: 0.1;
                }}
            }}
            .leaflet-popup-content-wrapper {{
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                border: 1px solid #E5EBF4;
                padding: 6px;
            }}
            .leaflet-popup-tip {{
                border: 1px solid #E5EBF4;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map', {{
                zoomControl: true,
                attributionControl: false
            }}).setView([{center_lat}, {center_lon}], {zoom});
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 19
            }}).addTo(map);
            
            {markers_js}
        </script>
    </body>
    </html>
    """
    return html

def render_civic_map():
    # Page Header
    render_topbar("Civic Map", "GIS Mapping of reported civic issues and status updates.")
    
    # Load all issues
    issues = load_issues()
    
    # Initialize session state for selected issue
    if "selected_issue_id" not in st.session_state:
        st.session_state["selected_issue_id"] = None
        
    # Columns layout: Left (Filters) | Middle (Map + Fallback List) | Right (Issue Drawer)
    col_filters, col_map, col_drawer = st.columns([2.5, 6, 3.5])
    
    with col_filters:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">🗺️ Map Filters</div>', unsafe_allow_html=True)
        
        # Category Filter
        all_categories = sorted(list(set(i["type"] for i in issues)))
        selected_cats = st.multiselect("Category", all_categories, default=all_categories)
        
        # Status Filter
        selected_statuses = st.multiselect("Status", ["Pending", "Assigned", "Resolved"], default=["Pending", "Assigned"])
        
        # Priority Filter
        selected_priorities = st.multiselect("Priority", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"])
        
        # Ward Filter
        all_wards = sorted(list(set(i["ward"] for i in issues if i.get("ward"))))
        selected_wards = st.multiselect("Wards", all_wards, default=all_wards)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Legend Card
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">📌 Map Legend</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 12px; line-height: 1.8;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="height: 12px; width: 12px; background-color: #D64545; border-radius: 50%; display: inline-block;"></span>
                    <span>Critical / High Priority</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="height: 12px; width: 12px; background-color: #F59E0B; border-radius: 50%; display: inline-block;"></span>
                    <span>Medium Priority</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="height: 12px; width: 12px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
                    <span>Low Priority</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="height: 12px; width: 12px; background-color: #12805C; border-radius: 50%; display: inline-block;"></span>
                    <span>Resolved Issue</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Apply filters
    filtered_issues = [
        i for i in issues
        if i["type"] in selected_cats
        and i["status"] in selected_statuses
        and i["priority"] in selected_priorities
        and i.get("ward") in selected_wards
    ]
    
    # Load currently selected issue details
    selected_id = st.session_state.get("selected_issue_id")
    selected_issue = next((i for i in issues if i["id"] == selected_id), None) if selected_id else None
    
    # Center map on selected issue or fallback to default center
    if selected_issue and selected_issue.get("latitude") and selected_issue.get("longitude"):
        center_lat = selected_issue["latitude"]
        center_lon = selected_issue["longitude"]
        zoom_level = 14
    else:
        center_lat = 12.9716
        center_lon = 77.5946
        zoom_level = 11.2
        
    with col_map:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Live GIS Map</div>', unsafe_allow_html=True)
        
        # Render custom Leaflet map
        leaflet_html = generate_leaflet_html(filtered_issues, center_lat, center_lon, zoom_level)
        components.html(leaflet_html, height=450)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Interactivity Fallback list below the map
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Synchronized Active Incidents List</div>', unsafe_allow_html=True)
        
        if filtered_issues:
            for issue in filtered_issues:
                col_row_info, col_row_btn = st.columns([8, 2])
                with col_row_info:
                    st.markdown(
                        f"**{issue['id']}** — {issue['type']} | "
                        f"{priority_pill(issue['priority'])} | "
                        f"{status_pill(issue['status'])} <br/>"
                        f"<span style='font-size: 12px; color: #6B7B95;'>{issue['location_text']}</span>",
                        unsafe_allow_html=True
                    )
                with col_row_btn:
                    if st.button("Inspect 🔎", key=f"inspect_{issue['id']}", use_container_width=True):
                        st.session_state["selected_issue_id"] = issue["id"]
                        st.rerun()
                st.divider()
        else:
            st.write("No incidents to show.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_drawer:
        st.markdown('<div class="ue-drawer">', unsafe_allow_html=True)
        
        if selected_issue:
            st.markdown(
                f"""
                <div class="ue-drawer-header">
                    <div style="font-size: 12px; color: #6B7B95; font-weight: 600;">{selected_issue['id']}</div>
                    <div class="ue-drawer-title">{selected_issue['type']}</div>
                    <div class="ue-drawer-subtitle">{selected_issue['location_text']}</div>
                    <div style="margin-top: 8px; display: flex; gap: 8px;">
                        {priority_pill(selected_issue['priority'])}
                        {status_pill(selected_issue['status'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Show photo evidence if path is present and file exists
            img_path = selected_issue.get("image_path")
            if img_path and os.path.exists(img_path):
                st.image(img_path, caption="Incident Photo Evidence", use_container_width=True)
            
            # Metadata
            st.markdown("### Incident Metadata")
            st.write(f"**Ward:** {selected_issue.get('ward', 'N/A')}")
            time_dt = datetime.fromisoformat(selected_issue['reported_at'])
            st.write(f"**Reported:** {time_dt.strftime('%b %d, %Y at %I:%M %p')}")
            
            if selected_issue.get("confidence") is not None:
                st.write(f"**AI Confidence:** {selected_issue['confidence']:.1%}")
                
            st.write(f"**Description:** {selected_issue.get('description', 'N/A')}")
            
            # Display Priority Reasoning string
            if selected_issue.get("priority_reason"):
                st.markdown(
                    f"""
                    <div style="background-color: #F7F9FC; border-left: 4px solid #10B981; padding: 12px; border-radius: 0 8px 8px 0; margin-bottom: 16px; border: 1px solid #E5EBF4;">
                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #6B7B95; margin-bottom: 4px;">Priority Reasoning</div>
                        <div style="font-size: 12px; color: #10213D; line-height: 1.4;">{selected_issue['priority_reason'].replace(' • ', '<br/>• ')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            if selected_issue.get("assigned_to"):
                st.write(f"**Assigned Crew:** {selected_issue['assigned_to']}")
                
            st.divider()
            
            # Action logic
            st.markdown("### Dispatch & Operations")
            
            status_opts = ["Pending", "Assigned", "Resolved"]
            status_idx = status_opts.index(selected_issue["status"])
            
            new_status = st.selectbox("Action Status", status_opts, index=status_idx)
            
            assigned_crew = st.text_input(
                "Assign Field Crew", 
                value=selected_issue.get("assigned_to") if selected_issue.get("assigned_to") else ""
            )
            
            # AI derived action
            rec_action = "Routine maintenance log."
            if selected_issue["type"] == "Pothole":
                if selected_issue["priority"] in ["Critical", "High"]:
                    rec_action = "Dispatch road patching crew within 24 hours."
                else:
                    rec_action = "Schedule patching within 5 business days."
            elif selected_issue["type"] == "Garbage":
                rec_action = "Schedule sanitation truck pickup and check dump bins."
            elif selected_issue["type"] == "Water Logging":
                rec_action = "Dispatch drainage crew to clear storm drain obstructions."
            action_card(rec_action, "Recommended Field Action")
            
            if st.button("Apply Status Changes", type="primary", use_container_width=True):
                update_issue_status(selected_issue["id"], new_status, assigned_to=assigned_crew if assigned_crew else None)
                st.success("Issue status updated successfully!")
                st.rerun()
                
            if st.button("Close Drawer ✖", use_container_width=True):
                st.session_state["selected_issue_id"] = None
                st.rerun()
        else:
            # Empty state
            st.markdown(
                """
                <div style="text-align: center; padding-top: 100px; color: #6B7B95;">
                    <div style="font-size: 40px; margin-bottom: 12px;">🗺️</div>
                    <h3>No Incident Selected</h3>
                    <p style="font-size: 13px;">Select an incident from the map markers or from the synchronized list below the map to inspect location data and update dispatch statuses.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

