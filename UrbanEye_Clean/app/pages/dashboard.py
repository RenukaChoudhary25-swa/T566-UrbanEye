import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components

from app.services.issues import load_issues
from app.services.analytics import get_basic_metrics, get_issue_trends, get_ward_distribution, get_severity_distribution
from app.ui.components import kpi_card, render_alert_row
from app.ui.charts import render_trend_chart, render_distribution_chart, render_ward_comparison
from app.ui.shell import render_topbar

def generate_leaflet_preview_html(issues):
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
            color = "#2563EB" # Blue
            
        popup_html = f"<strong>{i.get('id')}</strong>: {i.get('type')} ({p} Priority)"
        popup_html = popup_html.replace("'", "\\'")
        
        markers_js += f"""
        L.circleMarker([{lat}, {lon}], {{
            radius: 5,
            fillColor: '{color}',
            color: '#FFFFFF',
            weight: 1.5,
            opacity: 1,
            fillOpacity: 0.9
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
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map', {{
                zoomControl: false,
                attributionControl: false,
                scrollWheelZoom: false,
                dragging: false
            }}).setView([12.9716, 77.5946], 10.5);
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
            {markers_js}
        </script>
    </body>
    </html>
    """
    return html

def render_dashboard():
    # Load all issues
    issues = load_issues()
    
    # Apply global filters first to get baseline metrics
    filtered_issues = issues
    
    # Recalculate baseline metrics
    metrics = get_basic_metrics(filtered_issues)
    
    # 1. Page Header
    render_topbar("Good morning, Ananya", "Here’s the civic pulse across your city.")
    
    # Filters Row
    st.markdown('<div style="margin-bottom: 12px; font-weight: 600; font-size: 14px; color: #6B7B95;">FILTERS</div>', unsafe_allow_html=True)
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        date_range = st.selectbox("Date Range", ["Last 14 Days", "Last 30 Days", "Today"], label_visibility="collapsed")
    with col_f2:
        # Extract unique wards, filter out None
        wards = sorted(list(set(i.get("ward") for i in issues if i.get("ward"))))
        selected_ward = st.selectbox("Ward", ["All Wards"] + wards, label_visibility="collapsed")
    with col_f3:
        selected_status = st.selectbox("Status", ["All Statuses", "Pending", "Assigned", "Resolved"], label_visibility="collapsed")
    with col_f4:
        selected_priority = st.selectbox("Priority", ["All Priorities", "Critical", "High", "Medium", "Low"], label_visibility="collapsed")
        
    # Apply filters to filtered_issues
    if selected_ward != "All Wards":
        filtered_issues = [i for i in filtered_issues if i.get("ward") == selected_ward]
        
    if selected_status != "All Statuses":
        filtered_issues = [i for i in filtered_issues if i.get("status") == selected_status]
        
    if selected_priority != "All Priorities":
        filtered_issues = [i for i in filtered_issues if i.get("priority") == selected_priority]
        
    now = datetime.now()
    if date_range == "Today":
        filtered_issues = [i for i in filtered_issues if (now - datetime.fromisoformat(i.get("reported_at"))).days < 1]
    elif date_range == "Last 14 Days":
        filtered_issues = [i for i in filtered_issues if (now - datetime.fromisoformat(i.get("reported_at"))).days < 14]
    elif date_range == "Last 30 Days":
        filtered_issues = [i for i in filtered_issues if (now - datetime.fromisoformat(i.get("reported_at"))).days < 30]

    # Recalculate metrics based on active filters
    filtered_metrics = get_basic_metrics(filtered_issues)

    # Make KPI Grid
    st.markdown('<div class="ue-kpi-container">', unsafe_allow_html=True)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        kpi_card("Total Issues", filtered_metrics["total"], delta="12%", delta_type="positive", icon="🚨")
    with kpi_col2:
        kpi_card("Potholes", filtered_metrics["potholes"], delta="8%", delta_type="positive", icon="🕳️", class_name="potholes")
    with kpi_col3:
        kpi_card("Garbage", filtered_metrics["garbage"], delta="15%", delta_type="positive", icon="🗑️", class_name="garbage")
    with kpi_col4:
        # Sum Critical + High for high priority card
        crit_high_total = filtered_metrics["critical"] + filtered_metrics["high_priority"]
        kpi_card("Critical & High", crit_high_total, delta="4%", delta_type="negative", delta_text="vs last week", icon="⚠️", class_name="critical")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Main Row: Trend & Recent Alerts
    col_main_left, col_main_right = st.columns([7, 5])
    
    with col_main_left:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Daily Issue Trends <span style="font-size: 12px; font-weight: normal; color: #6B7B95;">(Last 14 Days)</span></div>', unsafe_allow_html=True)
        trend_df = get_issue_trends(filtered_issues)
        if not trend_df.empty and trend_df["Count"].sum() > 0:
            render_trend_chart(trend_df)
        else:
            st.info("No trend data matches the selected filters.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_main_right:
        st.markdown('<div class="ue-card" style="height: 350px; overflow-y: auto;">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Recent Alerts</div>', unsafe_allow_html=True)
        
        # Sort issues by time descending, pick top 5
        sorted_alerts = sorted(filtered_issues, key=lambda i: i.get("reported_at"), reverse=True)[:5]
        
        if sorted_alerts:
            for alert in sorted_alerts:
                time_dt = datetime.fromisoformat(alert.get("reported_at"))
                time_display = time_dt.strftime("%b %d, %H:%M")
                render_alert_row(
                    title=f"{alert.get('type')} in {alert.get('ward')}",
                    subtitle=alert.get("location_text"),
                    priority=alert.get("priority", "Medium"),
                    time_str=time_display
                )
        else:
            st.markdown('<div style="text-align: center; color: #6B7B95; padding-top: 50px;">No recent alerts found</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 4. Lower Row: Donut Chart & Map
    col_bottom_left, col_bottom_right = st.columns([5, 7])
    
    with col_bottom_left:
        st.markdown('<div class="ue-card" style="height: 380px;">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Issue Distribution</div>', unsafe_allow_html=True)
        
        dist_data = [
            {"Type": "Pothole", "Count": filtered_metrics["potholes"]},
            {"Type": "Garbage", "Count": filtered_metrics["garbage"]},
            {"Type": "Others", "Count": filtered_metrics["total"] - filtered_metrics["potholes"] - filtered_metrics["garbage"]}
        ]
        dist_df = pd.DataFrame(dist_data)
        dist_df = dist_df[dist_df["Count"] > 0]
        
        if not dist_df.empty:
            render_distribution_chart(dist_df)
        else:
            st.markdown('<div style="text-align: center; color: #6B7B95; padding-top: 80px;">No distribution data available</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_bottom_right:
        st.markdown('<div class="ue-card" style="height: 380px;">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">City Hotspot Overview</div>', unsafe_allow_html=True)
        
        # Render Leaflet static preview map
        if filtered_issues:
            leaflet_preview = generate_leaflet_preview_html(filtered_issues)
            components.html(leaflet_preview, height=290)
        else:
            st.markdown('<div style="text-align: center; color: #6B7B95; padding-top: 80px;">No coordinate issues found for the map</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
