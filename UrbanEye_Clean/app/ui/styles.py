import streamlit as st

def inject_styles():
    st.markdown(
        """
        <style>
        /* Fonts and General layout */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #F7F9FC !important;
            color: #10213D !important;
        }
        
        h1, h2, h3, .ue-title-font {
            font-family: 'Outfit', sans-serif !important;
        }
        
        /* Hide default Streamlit headers, footers and navigation links */
        [data-testid="stHeader"] {
            display: none !important;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        footer {
            visibility: hidden !important;
            height: 0 !important;
            padding: 0 !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #F7F9FC;
        }
        ::-webkit-scrollbar-thumb {
            background: #D1D5DB;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #9CA3AF;
        }
        
        /* Sidebar styling overrides */
        [data-testid="stSidebar"] {
            background-color: #0B1730 !important;
            min-width: 248px !important;
            max-width: 248px !important;
            border-right: 1px solid #101F3D !important;
        }
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        
        /* Style native Streamlit buttons in the sidebar to look like custom nav items */
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            color: rgba(255, 255, 255, 0.8) !important;
            text-align: left !important;
            padding: 10px 16px !important;
            width: 100% !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            justify-content: flex-start !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
            margin-bottom: 4px !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: rgba(255, 255, 255, 0.06) !important;
            color: white !important;
        }
        /* Active nav item */
        [data-testid="stSidebar"] button[kind="primary"] {
            background-color: #10B981 !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15) !important;
        }
        
        /* Native Streamlit Buttons Styling */
        button[data-testid="stBaseButton-primary"] {
            background-color: #10B981 !important;
            border: 1px solid #10B981 !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 8px 18px !important;
            font-size: 14px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1) !important;
        }
        button[data-testid="stBaseButton-primary"]:hover {
            background-color: #059669 !important;
            border-color: #059669 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25) !important;
        }
        button[data-testid="stBaseButton-primary"]:active {
            transform: translateY(0px) !important;
        }
        
        button[data-testid="stBaseButton-secondary"] {
            background-color: white !important;
            border: 1px solid #E5EBF4 !important;
            color: #10213D !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            padding: 8px 18px !important;
            font-size: 14px !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }
        button[data-testid="stBaseButton-secondary"]:hover {
            border-color: #10B981 !important;
            color: #10B981 !important;
            background-color: #ECFDF5 !important;
            transform: translateY(-1px) !important;
        }
        
        /* File Uploader styling overrides to look like a premium dropzone */
        [data-testid="stFileUploader"] {
            border: 2px dashed #E5EBF4 !important;
            background-color: #F8FAFC !important;
            border-radius: 12px !important;
            padding: 16px !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #10B981 !important;
            background-color: #ECFDF5 !important;
        }
        [data-testid="stFileUploaderDropzone"] {
            background: transparent !important;
            border: none !important;
        }
        
        /* Selectbox and Input overrides */
        div[data-baseweb="select"] {
            border-radius: 10px !important;
        }
        div[data-baseweb="select"] > div {
            border-radius: 10px !important;
            border: 1px solid #E5EBF4 !important;
            background-color: white !important;
            color: #10213D !important;
        }
        div[data-baseweb="select"]:focus-within > div {
            border-color: #10B981 !important;
        }
        input, textarea {
            border-radius: 10px !important;
            border: 1px solid #E5EBF4 !important;
            background-color: white !important;
            color: #10213D !important;
            font-size: 14px !important;
        }
        input:focus, textarea:focus {
            border-color: #10B981 !important;
            box-shadow: 0 0 0 1px #10B981 !important;
        }
        
        /* Health module */
        .ue-health-card {
            background-color: #101F3D;
            border-radius: 12px;
            padding: 14px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 32px;
        }
        .ue-health-title {
            font-size: 11px;
            color: #6B7B95;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }
        .ue-health-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 6px;
        }
        .ue-health-row:last-child {
            margin-bottom: 0;
        }
        .ue-dot {
            height: 8px;
            width: 8px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 6px #10B981;
        }
        
        /* Operator profile in header */
        .ue-operator-profile {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .ue-operator-avatar {
            width: 36px;
            height: 36px;
            background-color: #ECFDF5;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            color: #10B981;
            font-size: 14px;
            border: 1px solid rgba(16, 185, 129, 0.15);
        }
        .ue-operator-info {
            display: flex;
            flex-direction: column;
        }
        .ue-operator-name {
            font-size: 13px;
            font-weight: 600;
            color: #10213D;
        }
        .ue-operator-role {
            font-size: 11px;
            color: #6B7B95;
        }
        
        /* Reusable Card Shells */
        .ue-card {
            background-color: white;
            border-radius: 16px;
            border: 1px solid #E5EBF4;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(16,33,61,.02);
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .ue-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(16,33,61,.05);
        }
        .ue-card-title {
            font-size: 16px;
            font-weight: 600;
            color: #10213D;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* KPI Cards Strip */
        .ue-kpi-container {
            margin-bottom: 8px;
        }
        .ue-kpi-card {
            background-color: white;
            border-radius: 16px;
            border: 1px solid #E5EBF4;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(16,33,61,.02);
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
            transition: all 0.2s ease;
        }
        .ue-kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(16,33,61,.05);
            border-color: rgba(16, 185, 129, 0.2);
        }
        .ue-kpi-data {
            display: flex;
            flex-direction: column;
        }
        .ue-kpi-label {
            font-size: 13px;
            color: #6B7B95;
            font-weight: 500;
            margin-bottom: 8px;
        }
        .ue-kpi-value {
            font-size: 32px;
            font-weight: 700;
            color: #10213D;
            line-height: 1;
            font-variant-numeric: tabular-nums;
        }
        .ue-kpi-delta {
            margin-top: 8px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 500;
        }
        .ue-kpi-delta.positive {
            color: #12805C;
        }
        .ue-kpi-delta.negative {
            color: #D64545;
        }
        .ue-kpi-icon {
            font-size: 24px;
            padding: 10px;
            border-radius: 12px;
            background-color: #F7F9FC;
        }
        .ue-kpi-card.potholes .ue-kpi-icon {
            background-color: #EAF2FF;
            color: #2563EB;
        }
        .ue-kpi-card.garbage .ue-kpi-icon {
            background-color: #FFFBEB;
            color: #F59E0B;
        }
        .ue-kpi-card.critical .ue-kpi-icon {
            background-color: #FDF2F2;
            color: #D64545;
        }
        
        /* Custom Stepper Component */
        .ue-stepper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 16px 0 24px 0;
            padding: 10px;
            background: #F8FAFC;
            border-radius: 12px;
            border: 1px solid #E5EBF4;
        }
        .ue-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            position: relative;
        }
        .ue-step-node {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: white;
            border: 2px solid #E5EBF4;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            color: #6B7B95;
            z-index: 2;
            transition: all 0.3s ease;
        }
        .ue-step.active .ue-step-node {
            border-color: #10B981;
            background: #10B981;
            color: white;
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
        }
        .ue-step.completed .ue-step-node {
            border-color: #10B981;
            background: #ECFDF5;
            color: #10B981;
        }
        .ue-step-label {
            font-size: 11px;
            font-weight: 600;
            color: #6B7B95;
            margin-top: 6px;
        }
        .ue-step.active .ue-step-label {
            color: #10B981;
        }
        .ue-step-line {
            position: absolute;
            height: 2px;
            background: #E5EBF4;
            width: 100%;
            top: 12px;
            left: 50%;
            z-index: 1;
        }
        .ue-step-line.completed {
            background: #10B981;
        }
        
        /* Segment Control / Tabs buttons */
        .ue-segment-control {
            display: flex;
            gap: 8px;
            background-color: #F1F5F9;
            padding: 4px;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
            margin-bottom: 12px;
        }
        .ue-segment-btn {
            flex: 1;
            text-align: center;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            color: #6B7B95;
            cursor: pointer;
            transition: all 0.15s ease;
            background: transparent;
            border: none;
        }
        .ue-segment-btn:hover {
            color: #10213D;
        }
        .ue-segment-btn.active {
            background-color: white;
            color: #10213D;
            font-weight: 600;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        }
        
        /* High Fidelity Confidence Block */
        .ue-confidence-block {
            background-color: #ECFDF5;
            border-radius: 12px;
            padding: 16px;
            border: 1px solid rgba(16, 185, 129, 0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .ue-confidence-title {
            font-size: 13px;
            font-weight: 500;
            color: #065F46;
        }
        .ue-confidence-value {
            background-color: #10B981;
            color: white;
            font-weight: 700;
            font-size: 20px;
            padding: 6px 14px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);
        }
        
        /* Pills */
        .ue-pill {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        .ue-pill.status-pending {
            background-color: #FEF3C7;
            color: #D97706;
            border: 1px solid rgba(217, 119, 6, 0.15);
        }
        .ue-pill.status-assigned {
            background-color: #E0F2FE;
            color: #0284C7;
            border: 1px solid rgba(2, 132, 199, 0.15);
        }
        .ue-pill.status-resolved {
            background-color: #D1FAE5;
            color: #059669;
            border: 1px solid rgba(5, 150, 105, 0.15);
        }
        .ue-pill.priority-critical {
            background-color: #FEE2E2;
            color: #DC2626;
            border: 1px solid #DC2626;
            font-weight: 700 !important;
        }
        .ue-pill.priority-high {
            background-color: #FEE2E2;
            color: #DC2626;
            border: 1px solid rgba(220, 38, 38, 0.15);
        }
        .ue-pill.priority-medium {
            background-color: #FEF3C7;
            color: #D97706;
            border: 1px solid rgba(217, 119, 6, 0.15);
        }
        .ue-pill.priority-low {
            background-color: #F1F5F9;
            color: #475569;
            border: 1px solid rgba(71, 85, 105, 0.15);
        }
        
        /* Action Card */
        .ue-action-card {
            background-color: #ECFDF5;
            border-left: 4px solid #10B981;
            padding: 16px;
            border-radius: 0 12px 12px 0;
            margin-top: 16px;
            margin-bottom: 16px;
            border-top: 1px solid rgba(16, 185, 129, 0.1);
            border-right: 1px solid rgba(16, 185, 129, 0.1);
            border-bottom: 1px solid rgba(16, 185, 129, 0.1);
        }
        .ue-action-title {
            font-size: 11px;
            font-weight: 600;
            color: #10B981;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .ue-action-text {
            font-size: 13px;
            color: #10213D;
            line-height: 1.4;
        }
        
        /* Alert Row */
        .ue-alert-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            border-radius: 12px;
            background-color: #F8FAFC;
            margin-bottom: 8px;
            border: 1px solid #E5EBF4;
            transition: all 0.2s ease;
        }
        .ue-alert-row:hover {
            border-color: rgba(16, 185, 129, 0.3);
            background-color: #ECFDF5;
            transform: translateX(2px);
        }
        .ue-alert-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .ue-alert-dot {
            height: 8px;
            width: 8px;
            border-radius: 50%;
        }
        .ue-alert-dot.critical {
            background-color: #D64545;
            box-shadow: 0 0 0 3px rgba(214, 69, 69, 0.2);
        }
        .ue-alert-dot.high {
            background-color: #D64545;
        }
        .ue-alert-dot.medium {
            background-color: #F59E0B;
        }
        .ue-alert-dot.low {
            background-color: #6B7B95;
        }
        .ue-alert-text {
            font-size: 13px;
            font-weight: 500;
            color: #10213D;
        }
        .ue-alert-sub {
            font-size: 11px;
            color: #6B7B95;
            margin-top: 2px;
        }
        .ue-alert-time {
            font-size: 12px;
            color: #6B7B95;
        }
        
        /* Timeline */
        .ue-timeline {
            position: relative;
            padding-left: 24px;
            margin-top: 16px;
        }
        .ue-timeline::before {
            content: '';
            position: absolute;
            top: 4px;
            left: 5px;
            bottom: 4px;
            width: 2px;
            background-color: #E5EBF4;
        }
        .ue-timeline-item {
            position: relative;
            margin-bottom: 20px;
        }
        .ue-timeline-item:last-child {
            margin-bottom: 0;
        }
        .ue-timeline-dot {
            position: absolute;
            left: -24px;
            top: 4px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: white;
            border: 2px solid #E5EBF4;
            box-sizing: border-box;
        }
        .ue-timeline-dot.active {
            border-color: #10B981;
            background-color: #10B981;
            box-shadow: 0 0 6px rgba(16, 185, 129, 0.4);
        }
        .ue-timeline-dot.completed {
            border-color: #12805C;
            background-color: #12805C;
        }
        .ue-timeline-title {
            font-size: 13px;
            font-weight: 600;
            color: #10213D;
        }
        
        /* Drawer Detail Panel */
        .ue-drawer {
            border: 1px solid #E5EBF4;
            border-radius: 16px;
            background-color: white;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(16,33,61,.08);
        }
        .ue-drawer-header {
            border-bottom: 1px solid #E5EBF4;
            padding-bottom: 16px;
            margin-bottom: 16px;
        }
        .ue-drawer-title {
            font-size: 18px;
            font-weight: 600;
            color: #10213D;
        }
        .ue-drawer-subtitle {
            font-size: 12px;
            color: #6B7B95;
            margin-top: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
