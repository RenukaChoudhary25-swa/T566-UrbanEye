import streamlit as st

def render_sidebar():
    # Render customized title inside the sidebar
    st.sidebar.markdown(
        """
        <div style="padding-top: 10px; margin-bottom: 32px;">
            <div style="font-size: 22px; font-weight: 700; color: white; display: flex; align-items: center; gap: 10px;">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12C2.73 16.39 7 19.5 12 19.5C17 19.5 21.27 16.39 23 12C21.27 7.61 17 4.5 12 4.5ZM12 17C9.24 17 7 14.76 7 12C7 9.24 9.24 7 12 7C14.76 7 17 9.24 17 12C17 14.76 14.76 17 12 17ZM12 9C10.34 9 9 10.34 9 12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12C15 10.34 13.66 9 12 9Z" fill="#10B981"/>
                </svg>
                <span>UrbanEye</span>
            </div>
            <div style="font-size: 11px; color: #6B7B95; margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">
                AI Civic Monitoring
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    pages = [
        ("dashboard", "📊 Dashboard"),
        ("ai_detection", "🔍 AI Detection"),
        ("citizen_report", "✍️ Citizen Report"),
        ("civic_map", "🗺️ Civic Map"),
        ("analytics", "📈 Analytics")
    ]
    
    active_page = st.session_state.get("active_page", "dashboard")
    
    for page_id, label in pages:
        is_active = (active_page == page_id)
        if st.sidebar.button(
            label, 
            key=f"nav_btn_{page_id}", 
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state["active_page"] = page_id
            st.query_params["page"] = page_id
            st.rerun()
            
    # System health card at the bottom
    st.sidebar.markdown(
        """
        <div class="ue-health-card">
            <div class="ue-health-title">System Health</div>
            <div class="ue-health-row">
                <span>Inference Engine</span>
                <span style="display: flex; align-items: center; gap: 6px; color: #10B981; font-weight: 500;">
                    <span class="ue-dot"></span> Active
                </span>
            </div>
            <div class="ue-health-row">
                <span>Database Sync</span>
                <span style="color: #10B981; font-weight: 500;">Online</span>
            </div>
            <div class="ue-health-row">
                <span>YOLOv8 Model</span>
                <span style="color: #10B981; font-weight: 500;">v8.0</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_topbar(title, subtitle=""):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"""
            <div style="margin-bottom: 24px;">
                <h1 style="font-size: 24px; font-weight: 700; color: #10213D; margin: 0; line-height: 1.2;">
                    {title}
                </h1>
                <p style="font-size: 13px; color: #6B7B95; margin: 4px 0 0 0;">
                    {subtitle}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 12px; height: 100%;">
                <div class="ue-operator-profile">
                    <div class="ue-operator-avatar">A</div>
                    <div class="ue-operator-info">
                        <div class="ue-operator-name">Ananya Sharma</div>
                        <div class="ue-operator-role">Command Center Operator</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
