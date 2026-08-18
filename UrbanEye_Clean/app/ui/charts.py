import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_trend_chart(df):
    fig = px.line(
        df,
        x="Date",
        y="Count",
        color="Issue Type",
        color_discrete_map={
            "Pothole": "#2563EB",
            "Garbage": "#F59E0B",
            "Others": "#7357D8"
        },
        title=None
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        xaxis=dict(
            showline=True,
            showgrid=False,
            linecolor='#E5EBF4',
            tickfont=dict(family="Inter", size=11, color="#6B7B95")
        ),
        yaxis=dict(
            showline=False,
            showgrid=True,
            gridcolor='#E5EBF4',
            tickfont=dict(family="Inter", size=11, color="#6B7B95"),
            dtick=1
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Inter", size=11, color="#10213D")
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_distribution_chart(df):
    labels = df["Type"].tolist()
    values = df["Count"].tolist()
    
    # Dynamic color mapping based on labels
    color_map = {
        "Critical": "#D64545",
        "High": "#FF6B6B",
        "Medium": "#F59E0B",
        "Low": "#2563EB",
        "Pothole": "#2563EB",
        "Garbage": "#F59E0B",
        "Others": "#7357D8"
    }
    colors = [color_map.get(lbl, "#7357D8") for lbl in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.6,
        marker=dict(colors=colors),
        textinfo='percent',
        hoverinfo='label+value'
    )])
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(family="Inter", size=11, color="#10213D")
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_ward_comparison(df):
    fig = go.Figure()
    
    pothole_y = df["Pothole"].tolist() if "Pothole" in df else [0]*len(df)
    garbage_y = df["Garbage"].tolist() if "Garbage" in df else [0]*len(df)
    others_y = df["Others"].tolist() if "Others" in df else [0]*len(df)
    
    fig.add_trace(go.Bar(
        x=df["Ward"],
        y=pothole_y,
        name='Pothole',
        marker_color='#2563EB'
    ))
    fig.add_trace(go.Bar(
        x=df["Ward"],
        y=garbage_y,
        name='Garbage',
        marker_color='#F59E0B'
    ))
    fig.add_trace(go.Bar(
        x=df["Ward"],
        y=others_y,
        name='Others',
        marker_color='#7357D8'
    ))
    
    fig.update_layout(
        barmode='stack',
        margin=dict(l=20, r=20, t=10, b=20),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickfont=dict(family="Inter", size=11, color="#6B7B95"),
            linecolor='#E5EBF4'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5EBF4',
            tickfont=dict(family="Inter", size=11, color="#6B7B95")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Inter", size=11, color="#10213D")
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
