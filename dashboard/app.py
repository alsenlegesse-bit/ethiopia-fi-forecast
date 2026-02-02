import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📊 Ethiopia Financial Inclusion Forecasting System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Scenario selection
    scenario = st.selectbox(
        "Select Scenario",
        ["Baseline", "Optimistic", "Pessimistic"]
    )
    
    # Year range
    year_range = st.slider(
        "Forecast Years",
        min_value=2025,
        max_value=2027,
        value=(2025, 2027)
    )
    
    # Indicator selection
    indicators = st.multiselect(
        "Select Indicators",
        ["Account Ownership", "Digital Payment Usage", "Mobile Money Accounts"],
        default=["Account Ownership", "Digital Payment Usage"]
    )

# Page 1: Overview
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Forecasts", "Projections"])

with tab1:
    st.header("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Account Ownership (2024)",
            value="49%",
            delta="+3pp since 2021"
        )
    
    with col2:
        st.metric(
            label="Digital Payment Usage",
            value="35%",
            delta="+20pp since 2017"
        )
    
    with col3:
        st.metric(
            label="Mobile Money Penetration",
            value="9.45%",
            delta="+4.75pp since 2021"
        )
    
    with col4:
        st.metric(
            label="P2P/ATM Crossover Ratio",
            value="1.2",
            delta="Digital > Cash"
        )
    
    # Event timeline
    st.subheader("Key Events Timeline")
    events_data = pd.DataFrame({
        'Event': ['Telebirr Launch', 'M-Pesa Entry', 'Interoperability'],
        'Date': ['2021-05-01', '2023-08-01', '2022-01-01'],
        'Impact': ['High', 'Medium', 'High']
    })
    
    fig = px.timeline(events_data, x_start="Date", y="Event", color="Impact")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Historical Trends")
    
    # Sample historical data
    historical = pd.DataFrame({
        'Year': [2011, 2014, 2017, 2021, 2024],
        'Account Ownership': [14, 22, 35, 46, 49],
        'Digital Payments': [5, 10, 15, 25, 35],
        'Mobile Money': [0, 1, 4.7, 9.45, 9.45]
    })
    
    # Interactive chart
    fig = px.line(
        historical, 
        x='Year', 
        y=indicators,
        title="Financial Inclusion Trends 2011-2024"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Gender gap if available
    st.subheader("Gender Analysis")
    gender_data = pd.DataFrame({
        'Year': [2021, 2024],
        'Male': [48, 51],
        'Female': [44, 47],
        'Gap': [4, 4]
    })
    
    fig = px.bar(
        gender_data,
        x='Year',
        y=['Male', 'Female'],
        barmode='group',
        title="Account Ownership by Gender"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Forecasts 2025-2027")
    
    # Sample forecast data
    forecast_data = pd.DataFrame({
        'Year': [2025, 2026, 2027],
        'Account Ownership Baseline': [51.5, 53.8, 56.0],
        'Account Ownership Optimistic': [53.0, 56.5, 60.0],
        'Account Ownership Pessimistic': [50.0, 51.0, 52.0],
        'Digital Payments Baseline': [38.0, 41.0, 44.0],
        'Digital Payments Optimistic': [40.0, 45.0, 50.0],
        'Digital Payments Pessimistic': [36.0, 37.0, 38.0]
    })
    
    # Scenario-based chart
    if scenario == "Baseline":
        cols = ['Account Ownership Baseline', 'Digital Payments Baseline']
    elif scenario == "Optimistic":
        cols = ['Account Ownership Optimistic', 'Digital Payments Optimistic']
    else:
        cols = ['Account Ownership Pessimistic', 'Digital Payments Pessimistic']
    
    fig = go.Figure()
    
    for col in cols:
        if col in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['Year'],
                y=forecast_data[col],
                name=col.replace(scenario.lower(), '').strip(),
                mode='lines+markers'
            ))
    
    fig.update_layout(
        title=f"{scenario} Scenario Forecasts",
        xaxis_title="Year",
        yaxis_title="Percentage (%)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display forecast table
    st.subheader("Forecast Table")
    st.dataframe(forecast_data.style.format("{:.1f}%"), use_container_width=True)

with tab4:
    st.header("Inclusion Projections")
    
    # Progress toward 60% target
    st.subheader("Progress Toward NFIS-II Target (60% by 2027)")
    
    progress_data = pd.DataFrame({
        'Year': [2021, 2024, 2025, 2026, 2027],
        'Actual/Forecast': [46, 49, 52, 55, 58],
        'Target': [46, 50, 54, 57, 60]
    })
    
    fig = px.line(
        progress_data,
        x='Year',
        y=['Actual/Forecast', 'Target'],
        title="Progress Toward 60% Financial Inclusion Target"
    )
    
    # Add shaded area for target achievement
    fig.add_hrect(y0=0, y1=60, line_width=0, fillcolor="green", opacity=0.1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Answer key questions
    st.subheader("Answers to Consortium Questions")
    
    with st.expander("What drives financial inclusion in Ethiopia?"):
        st.markdown("""
        - **Mobile money expansion**: Telebirr and M-Pesa have been key drivers
        - **Interoperability**: P2P transfers surpassing ATM withdrawals
        - **Infrastructure**: 4G coverage and smartphone penetration
        - **Policy support**: National Financial Inclusion Strategy (NFIS-II)
        """)
    
    with st.expander("How do events affect inclusion outcomes?"):
        st.markdown("""
        - **Product launches**: Telebirr added 5pp to mobile money adoption
        - **Market entries**: M-Pesa increased competition and innovation
        - **Policy changes**: Interoperability boosted digital payments
        """)
    
    with st.expander("2025-2027 Outlook"):
        st.markdown("""
        - **2025**: Account ownership expected to reach 51-53%
        - **2026**: Digital payments projected at 41-45%
        - **2027**: Potential to reach 58-60% inclusion with continued growth
        """)

# Footer
st.markdown("---")
st.caption("Ethiopia Financial Inclusion Forecasting System | Selam Analytics Challenge 2026")
