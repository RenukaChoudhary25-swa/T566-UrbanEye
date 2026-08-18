import streamlit as st
from PIL import Image
import numpy as np
import random
import os

from app.services.inference import run_detection
from app.services.issues import add_issue
from app.ui.components import action_card, render_stepper, render_confidence_block, priority_pill
from app.ui.shell import render_topbar

def render_ai_detection():
    render_topbar("AI Detection", "Detect and identify civic issues using AI")
    
    st.markdown('<div style="font-size: 12px; color: #6B7B95; margin-bottom: 16px;">YOLOv8n · Pothole + Garbage Detection</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📷 Image Detection", "🎥 Video Detection"])
    
    with tabs[0]:
        # Stepper state based on file uploader
        uploaded_file = st.file_uploader(
            "Drag and drop or browse files (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            key="ai_img_uploader",
            label_visibility="collapsed"
        )
        
        current_step = "Capture"
        if uploaded_file:
            current_step = "Result"
            
        render_stepper(current_step)
        
        col_left, col_right = st.columns([7, 5])
        
        with col_left:
            st.markdown('<div class="ue-card">', unsafe_allow_html=True)
            st.markdown('<div class="ue-card-title">Upload Evidence</div>', unsafe_allow_html=True)
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                
                with st.spinner("🔍 Running YOLOv8 detection..."):
                    result = run_detection(image)
                    
                st.image(result["annotated_image"], caption="Annotated AI Detection", use_container_width=True)
            else:
                st.info("Drag and drop or select an image file to analyze.")
            st.markdown('</div>', unsafe_allow_html=True)
                
        with col_right:
            if uploaded_file and 'result' in locals():
                st.markdown('<div class="ue-card">', unsafe_allow_html=True)
                st.markdown('<div class="ue-card-title">Detection Summary</div>', unsafe_allow_html=True)
                
                detections = result["detections"]
                
                if len(detections) > 0:
                    # Sort by confidence descending
                    primary_det = sorted(detections, key=lambda d: d["confidence"], reverse=True)[0]
                    render_confidence_block(primary_det['class_name'], primary_det['confidence'])
                    
                    st.markdown(f"**Severity:** {priority_pill(primary_det['severity'])}", unsafe_allow_html=True)
                    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
                    
                    action_card(result["recommended_action"], "AI Recommended Action")
                    
                    st.divider()
                    st.markdown("### Log Civic Issue")
                    
                    ward_options = [f"Ward {w}" for w in range(1, 11)]
                    selected_ward = st.selectbox("Assign Ward", ward_options, key="ai_ward")
                    
                    location_detail = st.text_input(
                        "Location Details (Address / Landmarks)",
                        placeholder="e.g. Ring Road, near Metro station",
                        key="ai_loc"
                    )
                    
                    description_prefill = f"AI Detected {primary_det['class_name']} with {primary_det['confidence']:.1%} confidence."
                    
                    description = st.text_area(
                        "Description",
                        value=description_prefill,
                        key="ai_desc"
                    )
                    
                    if st.button("💾 Save as Civic Issue", type="primary", use_container_width=True):
                        lat = 12.9716 + random.uniform(-0.06, 0.06)
                        lon = 77.5946 + random.uniform(-0.06, 0.06)
                        
                        new_issue = add_issue(
                            issue_type=primary_det['class_name'],
                            description=description,
                            priority=primary_det['severity'],
                            latitude=lat,
                            longitude=lon,
                            location_text=f"{location_detail}, {selected_ward}" if location_detail else f"{selected_ward} main road",
                            ward=selected_ward,
                            confidence=primary_det['confidence']
                        )
                        st.success(f"✅ Success! Logged as issue {new_issue['id']}. It is now live on the map.")
                else:
                    st.info("✅ No pothole or garbage detected.")
                    action_card(result["recommended_action"], "AI Recommendation")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="ue-card">', unsafe_allow_html=True)
                st.markdown('<div class="ue-card-title">Detection Panel</div>', unsafe_allow_html=True)
                st.info("Please upload an image to see detection details.")
                st.markdown('</div>', unsafe_allow_html=True)
                
    with tabs[1]:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Video Stream Analysis</div>', unsafe_allow_html=True)
        
        uploaded_video = st.file_uploader(
            "Upload an urban dashcam video (MP4)",
            type=["mp4", "avi", "mov"],
            key="ai_vid_uploader"
        )
        
        if uploaded_video:
            st.info("Video streaming and processing is optimized for demo. Click below to start detection simulation.")
            st.video(uploaded_video)
            
            if st.button("🎬 Run Video Inference Simulation", type="primary"):
                progress_text = "Analyzing video frames..."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    import time
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                st.success("✅ Video inference complete: 3 Potholes detected between timestamps 00:04 and 00:12.")
                
                st.markdown("### Detections Timeline")
                st.write("- **00:04** — Pothole (Medium Priority, 78% Confidence)")
                st.write("- **00:08** — Pothole (High Priority, 89% Confidence)")
                st.write("- **00:12** — Pothole (Low Priority, 65% Confidence)")
                
                action_card("Dispatch asphalt patching team to route.", "Simulated Video Action")
        else:
            st.info("Please upload a video to test stream detection.")
        st.markdown('</div>', unsafe_allow_html=True)
