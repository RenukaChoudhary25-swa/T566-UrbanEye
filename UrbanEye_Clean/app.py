import streamlit as st

# Configure the Streamlit Page first (must be the first command)
st.set_page_config(
    page_title="UrbanEye AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from app.ui.styles import inject_styles
from app.ui.shell import render_sidebar
from app.pages.dashboard import render_dashboard
from app.pages.ai_detection import render_ai_detection
from app.pages.citizen_report import render_citizen_report
from app.pages.civic_map import render_civic_map
from app.pages.analytics import render_analytics

# 1. Inject custom CSS stylesheet overrides
inject_styles()

# 2. Sync Query Parameters with Session State for Routing
query_params = st.query_params
if "page" in query_params:
    st.session_state["active_page"] = query_params["page"]
elif "active_page" not in st.session_state:
    st.session_state["active_page"] = "dashboard"

# 3. Render Custom Sidebar Layout
render_sidebar()

# 4. Main content router logic
active_page = st.session_state["active_page"]

if active_page == "dashboard":
    render_dashboard()
elif active_page == "ai_detection":
    render_ai_detection()
elif active_page == "citizen_report":
    render_citizen_report()
elif active_page == "civic_map":
    render_civic_map()
elif active_page == "analytics":
    render_analytics()
else:
    # Fallback to dashboard
    render_dashboard()