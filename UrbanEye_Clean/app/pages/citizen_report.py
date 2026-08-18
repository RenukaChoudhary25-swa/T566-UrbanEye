import streamlit as st
import random
from datetime import datetime
from PIL import Image
import os
import time

from app.services.issues import add_issue, save_uploaded_file
from app.services.inference import run_detection
from app.services.priority import calculate_priority
from app.ui.components import render_timeline, priority_pill
from app.ui.shell import render_topbar

def render_citizen_report():
    render_topbar("Citizen Report", "File a new civic issue report from the community.")
    
    col_left, col_right = st.columns([5, 7])
    
    # Session state to store newly created citizen issue for timeline display
    if "latest_citizen_issue" not in st.session_state:
        st.session_state["latest_citizen_issue"] = None
        
    # Standard Streamlit session states for coordinates
    if "cit_lat" not in st.session_state:
        st.session_state["cit_lat"] = 12.9716
    if "cit_lon" not in st.session_state:
        st.session_state["cit_lon"] = 77.5946
        
    with col_left:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Upload Photo Evidence</div>', unsafe_allow_html=True)
        
        citizen_photo = st.file_uploader(
            "Upload incident photo (JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            key="citizen_img"
        )
        
        has_ai = False
        confidence = None
        result = None
        
        if citizen_photo:
            # Cache inference result per uploaded file
            file_key = f"det_{citizen_photo.name}_{citizen_photo.size}"
            if "last_citizen_photo_key" not in st.session_state or st.session_state["last_citizen_photo_key"] != file_key:
                image = Image.open(citizen_photo)
                with st.spinner("🔍 Auto-triaging evidence with YOLOv8..."):
                    result = run_detection(image)
                st.session_state["last_citizen_photo_key"] = file_key
                st.session_state["citizen_detection_result"] = result
                
                # Prefill category & description if issues detected
                detections = result["detections"]
                if detections:
                    primary_det = sorted(detections, key=lambda d: d["confidence"], reverse=True)[0]
                    st.session_state["cit_cat"] = primary_det["class_name"]
                    st.session_state["cit_desc"] = f"AI Auto-Detected {primary_det['class_name']} with {primary_det['confidence']:.1%} confidence."
                else:
                    st.session_state["cit_desc"] = ""
            
            result = st.session_state.get("citizen_detection_result")
            if result and result["detections"]:
                has_ai = True
                st.image(result["annotated_image"], caption="Annotated AI Detection", use_container_width=True)
                
                # Show confidence meter
                st.markdown("### AI Detections")
                for det in result["detections"]:
                    cls = det["class_name"]
                    conf = det["confidence"]
                    st.write(f"**{cls}** (Confidence: {conf:.1%})")
                    st.progress(conf)
            else:
                st.image(citizen_photo, caption="Uploaded Evidence Preview", use_container_width=True)
                st.info("No automatic AI classification found on this image.")
        else:
            st.info("Upload a photo to improve triage speed.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Incident Details Form</div>', unsafe_allow_html=True)
        
        # 3-step progress strip
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #E5EBF4;">
                <div style="color: #10B981; font-weight: 600; font-size: 13px; display: flex; align-items: center; gap: 6px;">
                    <span style="background: #10B981; color: white; border-radius: 50%; width: 18px; height: 18px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px;">1</span> Details
                </div>
                <div style="width: 30px; height: 1px; background: #E5EBF4;"></div>
                <div style="color: #10B981; font-weight: 600; font-size: 13px; display: flex; align-items: center; gap: 6px;">
                    <span style="background: #10B981; color: white; border-radius: 50%; width: 18px; height: 18px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px;">2</span> Location
                </div>
                <div style="width: 30px; height: 1px; background: #E5EBF4;"></div>
                <div style="color: #6B7B95; font-weight: 500; font-size: 13px; display: flex; align-items: center; gap: 6px;">
                    <span style="background: #F1F5F9; color: #6B7B95; border-radius: 50%; width: 18px; height: 18px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px;">3</span> Review
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Category Selector
        categories = ["Pothole", "Garbage", "Water Logging", "Streetlight Out", "Broken Pavement", "Traffic Signal Out", "Other"]
        
        # Prepopulate category if AI detected
        category = st.selectbox("Issue Category", categories, key="cit_cat")
        
        # Estimate severity based on YOLO or standard mapping
        severity = "Medium"
        if has_ai and result and result["detections"]:
            primary_det = sorted(result["detections"], key=lambda d: d["confidence"], reverse=True)[0]
            confidence = primary_det["confidence"]
            severity = primary_det["severity"]
        else:
            priority_map = {
                "Water Logging": "High",
                "Traffic Signal Out": "High",
                "Streetlight Out": "High",
                "Pothole": "Medium",
                "Garbage": "Medium",
                "Broken Pavement": "Low",
                "Other": "Low"
            }
            severity = priority_map.get(category, "Medium")
            
        description = st.text_area(
            "Description of the issue",
            placeholder="Please describe what is wrong, including any specific details that might help crews find or fix it...",
            key="cit_desc"
        )
        
        ward_options = [f"Ward {w}" for w in range(1, 11)]
        ward = st.selectbox("Ward / Zone", ward_options, key="cit_ward")
        
        location_text = st.text_input(
            "Location Details (Address / Landmarks)",
            placeholder="e.g. Near 4th Cross Lane, opposite grocery store",
            key="cit_loc"
        )
        
        col_gps1, col_gps2 = st.columns(2)
        with col_gps1:
            lat_input = st.number_input("Latitude", value=st.session_state["cit_lat"], format="%.6f", key="cit_lat_in")
        with col_gps2:
            lon_input = st.number_input("Longitude", value=st.session_state["cit_lon"], format="%.6f", key="cit_lon_in")
            
        if st.button("📍 Autofill GPS Coordinates", use_container_width=True):
            st.session_state["cit_lat"] = 12.9716 + random.uniform(-0.06, 0.06)
            st.session_state["cit_lon"] = 77.5946 + random.uniform(-0.06, 0.06)
            st.rerun()
            
        st.session_state["cit_lat"] = lat_input
        st.session_state["cit_lon"] = lon_input
        
        # Priority Engine evaluation
        p_info = calculate_priority(
            category=category,
            severity=severity,
            confidence=confidence,
            location_text=location_text,
            description=description
        )
        
        derived_priority = p_info["priority"]
        priority_reason = p_info["reason"]
        
        p_colors = {
            "Critical": "#D64545",
            "High": "#D64545",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }
        p_color = p_colors.get(derived_priority, "#10B981")
        
        st.markdown(
            f"""
            <div style="background-color: #F7F9FC; border-left: 4px solid {p_color}; padding: 14px; border-radius: 0 12px 12px 0; margin-top: 16px; margin-bottom: 16px; border-top: 1px solid #E5EBF4; border-right: 1px solid #E5EBF4; border-bottom: 1px solid #E5EBF4;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 13px; font-weight: 600; color: #10213D;">Dynamic Priority (Engine):</span>
                    <span class="ue-pill priority-{derived_priority.lower()}">{derived_priority} Priority</span>
                </div>
                <div style="font-size: 11px; color: #6B7B95; margin-top: 6px; line-height: 1.4;">
                    <strong>Reasoning:</strong> {priority_reason.replace(' • ', '<br/>• ')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()
        
        submit_disabled = not (description.strip() and location_text.strip())
        
        if st.button("Submit Report ▶", type="primary", use_container_width=True, disabled=submit_disabled):
            image_path = None
            if citizen_photo:
                timestamp = int(time.time())
                filename = f"citizen_{timestamp}_{citizen_photo.name}"
                
                # If YOLO detected something, save the annotated detection image, otherwise original
                if has_ai and result:
                    image_path = save_uploaded_file(result["annotated_image"], filename)
                else:
                    image_path = save_uploaded_file(citizen_photo, filename)
            
            # Save using add_issue
            new_issue = add_issue(
                issue_type=category,
                description=description,
                priority=severity, # pass estimated severity, engine determines final priority
                latitude=st.session_state["cit_lat"],
                longitude=st.session_state["cit_lon"],
                location_text=f"{location_text}, {ward}",
                ward=ward,
                confidence=confidence,
                image_path=image_path
            )
            st.session_state["latest_citizen_issue"] = new_issue
            st.success(f"🎉 Report submitted successfully! Issue ID: {new_issue['id']}")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Bottom: Timeline of latest submission
    latest_report = st.session_state.get("latest_citizen_issue")
    if latest_report:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="ue-card-title">Submission Lifecycle Timeline — {latest_report["id"]}</div>', unsafe_allow_html=True)
        
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            render_timeline(latest_report["status"])
        with col_t2:
            st.markdown("### Submission Tracking Summary")
            st.write(f"**Status:** {latest_report['status']}")
            st.write(f"**Type:** {latest_report['type']}")
            st.write(f"**Ward:** {latest_report['ward']}")
            st.write(f"**Reported At:** {datetime.fromisoformat(latest_report['reported_at']).strftime('%B %d, %Y at %I:%M %p')}")
            st.write(f"**Description:** {latest_report['description']}")
            st.write(f"**Location:** {latest_report['location_text']}")
            
            st.info("Demo Note: As this issue progresses from Pending to Assigned and Resolved, this timeline status will automatically advance.")
        st.markdown('</div>', unsafe_allow_html=True)

