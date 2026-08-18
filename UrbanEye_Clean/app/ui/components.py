import streamlit as st

def kpi_card(label, value, delta=None, delta_text="vs last week", delta_type="positive", icon="📄", class_name=""):
    delta_class = "positive" if delta_type == "positive" else "negative"
    delta_arrow = "↑" if delta_type == "positive" else "↓"
    
    delta_html = ""
    if delta is not None:
        delta_html = f'<div class="ue-kpi-delta {delta_class}"><span>{delta_arrow} {delta}</span> <span style="color: #6B7B95; font-weight: 400;">{delta_text}</span></div>'
        
    st.markdown(
        f"""
        <div class="ue-kpi-card {class_name}">
            <div class="ue-kpi-data">
                <div class="ue-kpi-label">{label}</div>
                <div class="ue-kpi-value">{value}</div>
                {delta_html}
            </div>
            <div class="ue-kpi-icon">{icon}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def status_pill(status):
    status_lower = status.lower()
    return f'<span class="ue-pill status-{status_lower}">{status}</span>'

def priority_pill(priority):
    priority_lower = priority.lower()
    return f'<span class="ue-pill priority-{priority_lower}">{priority}</span>'

def action_card(action_text, rationale="Recommended response action"):
    st.markdown(
        f"""
        <div class="ue-action-card">
            <div class="ue-action-title">{rationale}</div>
            <div class="ue-action-text">{action_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_alert_row(title, subtitle, priority, time_str):
    dot_class = priority.lower()
    st.markdown(
        f"""
        <div class="ue-alert-row">
            <div class="ue-alert-left">
                <span class="ue-alert-dot {dot_class}"></span>
                <div>
                    <div class="ue-alert-text">{title}</div>
                    <div class="ue-alert-sub">{subtitle}</div>
                </div>
            </div>
            <div class="ue-alert-time">{time_str}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_timeline(current_status):
    steps = [
        ("Submitted", "Incident logged in database"),
        ("Triaged", "YOLO confidence confirmed"),
        ("Assigned", "Dispatched to field team"),
        ("Resolved", "Issue verified fixed")
    ]
    
    status_map = {
        "Pending": 0,
        "Assigned": 2,
        "Resolved": 3
    }
    
    current_idx = status_map.get(current_status, 0)
    
    html = '<div class="ue-timeline">'
    for i, (title, desc) in enumerate(steps):
        if i < current_idx:
            dot_state = "completed"
        elif i == current_idx:
            dot_state = "active"
        else:
            dot_state = ""
            
        html += f"""
        <div class="ue-timeline-item">
            <span class="ue-timeline-dot {dot_state}"></span>
            <div class="ue-timeline-title">{title}</div>
            <div style="font-size: 11px; color: #6B7B95; margin-top: 2px;">{desc}</div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_stepper(current_step):
    steps = ["Capture", "Analyze", "Result"]
    step_map = {"Capture": 0, "Analyze": 1, "Result": 2}
    active_idx = step_map.get(current_step, 0)
    
    html = '<div class="ue-stepper">'
    for i, label in enumerate(steps):
        node_state = ""
        if i < active_idx:
            node_state = "completed"
        elif i == active_idx:
            node_state = "active"
            
        line_html = ""
        if i < len(steps) - 1:
            line_state = "completed" if i < active_idx else ""
            line_html = f'<div class="ue-step-line {line_state}"></div>'
            
        html += f"""
        <div class="ue-step {node_state}">
            <div class="ue-step-node">{i+1}</div>
            <div class="ue-step-label">{label}</div>
            {line_html}
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_confidence_block(class_name, confidence):
    st.markdown(
        f"""
        <div class="ue-confidence-block">
            <div style="display: flex; flex-direction: column;">
                <span style="font-size: 11px; color: #6B7B95; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Detected Issue</span>
                <span style="font-size: 20px; font-weight: 700; color: #10213D; margin-top: 4px;">{class_name}</span>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; color: #6B7B95; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; display: block; margin-bottom: 4px;">Confidence</span>
                <span class="ue-confidence-value">{confidence:.0%}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
