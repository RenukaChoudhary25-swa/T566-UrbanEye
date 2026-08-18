import streamlit as st
import pandas as pd

from app.services.issues import load_issues
from app.services.analytics import get_basic_metrics, get_issue_trends, get_ward_distribution, get_severity_distribution, get_area_resolution_table
from app.ui.components import kpi_card
from app.ui.charts import render_trend_chart, render_distribution_chart, render_ward_comparison
from app.ui.shell import render_topbar

def render_analytics():
    # Page Header
    render_topbar("Analytics", "Municipal performance indicators, resolution timelines and SLA status.")
    
    # Load all issues
    issues = load_issues()
    
    # Metrics
    metrics = get_basic_metrics(issues)
    
    # Row 1: KPI strip
    st.markdown('<div class="ue-kpi-container">', unsafe_allow_html=True)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        kpi_card("Resolution Rate", f"{metrics['resolution_rate']:.1f}%", delta="4.2%", delta_type="positive", icon="✅")
    with kpi_col2:
        kpi_card("Avg Response Time", f"{metrics['avg_response_hours']:.1f} hrs", delta="-2.1 hrs", delta_type="positive", delta_text="lower is better", icon="⏱️", class_name="potholes")
    with kpi_col3:
        kpi_card("SLA Compliance", f"{metrics['sla_met_pct']:.1f}%", delta="1.5%", delta_type="positive", icon="🛡️", class_name="garbage")
    with kpi_col4:
        kpi_card("Total Logged Issues", metrics["total"], delta="18", delta_type="negative", delta_text="new today", icon="📋")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Trends and Ward stack chart
    col_r2_left, col_r2_right = st.columns([1, 1])
    
    with col_r2_left:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Issues Trend Over Time</div>', unsafe_allow_html=True)
        trend_df = get_issue_trends(issues, days_back=14)
        if not trend_df.empty:
            render_trend_chart(trend_df)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r2_right:
        st.markdown('<div class="ue-card">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Ward-wise Issue Distribution</div>', unsafe_allow_html=True)
        ward_df = get_ward_distribution(issues)
        if not ward_df.empty:
            render_ward_comparison(ward_df)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Row 3: Priority distribution and Area-wise resolution table
    col_r3_left, col_r3_right = st.columns([4, 8])
    
    with col_r3_left:
        st.markdown('<div class="ue-card" style="height: 380px;">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Severity Breakdown</div>', unsafe_allow_html=True)
        sev_df = get_severity_distribution(issues)
        if not sev_df.empty:
            # Reformat severity dataframe for Pie chart component
            pie_data = sev_df.rename(columns={"Priority": "Type"})
            render_distribution_chart(pie_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r3_right:
        st.markdown('<div class="ue-card" style="height: 380px; overflow-y: auto;">', unsafe_allow_html=True)
        st.markdown('<div class="ue-card-title">Area-wise Resolution Summary</div>', unsafe_allow_html=True)
        
        area_df = get_area_resolution_table(issues)
        
        if not area_df.empty:
            # Build custom HTML table for premium look
            table_html = """
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; font-family: 'Inter', sans-serif;">
                <thead>
                    <tr style="border-bottom: 2px solid #E5EBF4; color: #6B7B95; font-weight: 600;">
                        <th style="padding: 10px 8px;">Ward / Area</th>
                        <th style="padding: 10px 8px; text-align: center;">Open Issues</th>
                        <th style="padding: 10px 8px; text-align: center;">Resolved</th>
                        <th style="padding: 10px 8px; text-align: center;">Avg Response</th>
                        <th style="padding: 10px 8px; text-align: right;">SLA Compliance</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for index, row in area_df.iterrows():
                # Color code SLA
                sla_val = float(row["SLA Compliance"].replace("%", ""))
                if sla_val >= 90:
                    sla_style = "color: #12805C; font-weight: 600;"
                elif sla_val >= 75:
                    sla_style = "color: #C57A10; font-weight: 600;"
                else:
                    sla_style = "color: #D64545; font-weight: 600;"
                    
                table_html += f"""
                <tr style="border-bottom: 1px solid #E5EBF4; color: #10213D;">
                    <td style="padding: 12px 8px; font-weight: 500;">{row['Ward']}</td>
                    <td style="padding: 12px 8px; text-align: center; color: #D64545; font-weight: 600;">{row['Open']}</td>
                    <td style="padding: 12px 8px; text-align: center; color: #12805C; font-weight: 600;">{row['Resolved']}</td>
                    <td style="padding: 12px 8px; text-align: center; color: #6B7B95;">{row['Avg Response']}</td>
                    <td style="padding: 12px 8px; text-align: right; {sla_style}">{row['SLA Compliance']}</td>
                </tr>
                """
                
            table_html += """
                </tbody>
            </table>
            """
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.write("No area-wise data available.")
        st.markdown('</div>', unsafe_allow_html=True)
