# app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import pytz
import time

# Set page configuration
st.set_page_config(
    page_title="Advanced Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    :root {
        --primary-color: #3498db;
        --secondary-color: #2c3e50;
        --accent-color: #1abc9c;
        --bg-color: #0f172a;
        --card-bg: #1e293b;
    }
    
    /* Main page styling */
    .stApp {
        background: linear-gradient(135deg, var(--bg-color), #0c1424);
        color: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(30, 41, 59, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card styling */
    .card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Title styling */
    .title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(26, 188, 156, 0.4);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        background: rgba(30, 41, 59, 0.7) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        padding: 10px 15px;
    }
    
    /* Metric styling */
    .metric {
        text-align: center;
        padding: 15px;
        border-radius: 16px;
        background: rgba(26, 188, 156, 0.1);
        border: 1px solid rgba(26, 188, 156, 0.2);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent-color);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Weather icon animations */
    .weather-icon {
        font-size: 4rem;
        text-align: center;
        animation: pulse 3s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--card-bg) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        margin: 0 5px !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color)) !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .title {
            font-size: 2rem;
        }
        .col {
            flex-direction: column;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Mock weather data for demonstration
def mock_weather_data(location="New York"):
    # Current weather
    current = {
        "temp": 72,
        "feels_like": 74,
        "humidity": 65,
        "wind_speed": 8,
        "wind_direction": "NE",
        "pressure": 1012,
        "uv_index": 5,
        "visibility": 10,
        "description": "Partly Cloudy",
        "icon": "⛅",
        "sunrise": "06:24 AM",
        "sunset": "08:17 PM"
    }
    
    # Hourly forecast
    now = datetime.now()
    hourly = []
    for i in range(24):
        hour = (now + timedelta(hours=i)).strftime("%I %p")
        hourly.append({
            "time": hour,
            "temp": 70 + i - i//2,
            "precip": i % 5,
            "icon": "🌤️" if i < 8 else "🌙" if i > 18 else "☀️"
        })
    
    # Daily forecast
    daily = []
    days = ["Today", "Tomorrow", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(7):
        daily.append({
            "day": days[i],
            "high": 78 + i,
            "low": 62 + i,
            "precip": 20 * (i % 3),
            "icon": "🌤️" if i % 4 == 0 else "☀️" if i % 4 == 1 else "🌧️" if i % 4 == 2 else "⛈️"
        })
    
    return {
        "location": location,
        "current": current,
        "hourly": hourly,
        "daily": daily
    }

# Get real weather data from OpenWeatherMap API
def get_real_weather_data(location, api_key):
    # In a real implementation, we would use the OpenWeatherMap API
    # For this demo, we'll return mock data
    return mock_weather_data(location)

# Function to get geolocation
def get_geolocation():
    # This would use browser geolocation in a real app
    return {"latitude": 40.7128, "longitude": -74.0060}  # Default to New York

# Main application
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style="text-align:center; margin-bottom:30px;">
                <h2 style="color: #1abc9c; margin-bottom:5px;">🌤️ Advanced Weather</h2>
                <p style="color: #94a3b8;">Real-time weather insights and forecasts</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Location input
        location = st.text_input("Enter Location", "New York", key="location_input")
        
        # Unit selection
        unit = st.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"], index=1)
        
        # Additional options
        st.checkbox("Show Precipitation", True)
        st.checkbox("Show Wind Map", True)
        st.checkbox("Show UV Index", True)
        
        # Divider
        st.markdown("---")
        
        # Weather alerts
        with st.expander("Weather Alerts", expanded=True):
            st.info("No active alerts in your area")
            
        # About section
        st.markdown("""
            <div style="margin-top: 30px; color: #94a3b8; font-size: 0.8rem;">
                <p>Advanced Weather Dashboard v1.0</p>
                <p>Data updates every 15 minutes</p>
                <p>© 2023 Weather Analytics Inc.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<div class="title">Advanced</div>', unsafe_allow_html=True)
        st.markdown('<div class="title">Weather</div>', unsafe_allow_html=True)
        st.markdown("""
            <p style="font-size: 1.1rem; color: #94a3b8; margin-top: -10px;">
                Real-time weather insights and predictive forecasts
            </p>
        """, unsafe_allow_html=True)
        
        # Location and date
        st.markdown(f"""
            <div style="margin-top: 30px; margin-bottom: 20px;">
                <h2>{location}</h2>
                <p style="color: #94a3b8;">{datetime.now().strftime("%A, %B %d, %Y")}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Current conditions card
        weather_data = mock_weather_data(location)
        current = weather_data["current"]
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                st.markdown(f"""
                    <div class="weather-icon">{current["icon"]}</div>
                    <h2 style="text-align: center; font-size: 3.5rem; margin-top: -15px;">
                        {current["temp"]}°{'F' if unit == 'Fahrenheit' else 'C'}
                    </h2>
                    <p style="text-align: center; color: #94a3b8; margin-top: -15px;">
                        Feels like {current["feels_like"]}°
                    </p>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <p style="font-size: 1.2rem; margin-top: 20px;">{current["description"]}</p>
                    <div style="display: flex; margin-top: 20px;">
                        <div style="flex: 1;">
                            <p style="color: #94a3b8;">Sunrise</p>
                            <p>{current["sunrise"]}</p>
                        </div>
                        <div style="flex: 1;">
                            <p style="color: #94a3b8;">Sunset</p>
                            <p>{current["sunset"]}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Weather metrics
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            st.markdown("""
                <div class="metric">
                    <div class="metric-value">65%</div>
                    <div class="metric-label">Humidity</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric">
                    <div class="metric-value">8 mph</div>
                    <div class="metric-label">Wind</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
                <div class="metric">
                    <div class="metric-value">1012 hPa</div>
                    <div class="metric-label">Pressure</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
                <div class="metric">
                    <div class="metric-value">5</div>
                    <div class="metric-label">UV Index</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Temperature chart
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3>24-Hour Temperature Forecast</h3>', unsafe_allow_html=True)
            
            # Create temperature data
            hours = [f"{(i % 12) or 12}{'AM' if i < 12 else 'PM'}" for i in range(24)]
            temps = [68, 67, 66, 65, 65, 66, 68, 72, 75, 78, 80, 82, 
                     83, 84, 84, 83, 81, 78, 75, 73, 71, 70, 69, 68]
            
            # Create chart
            fig = px.line(
                x=hours,
                y=temps,
                labels={"x": "Time", "y": "Temperature (°F)"},
                height=300
            )
            
            # Customize chart
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#f0f2f6",
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
            )
            
            fig.update_traces(
                line=dict(color="#1abc9c", width=3),
                mode="lines+markers",
                marker=dict(size=8, color="#3498db")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Forecast tabs
        tab1, tab2 = st.tabs(["Hourly Forecast", "7-Day Forecast"])
        
        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3>Hourly Weather Conditions</h3>', unsafe_allow_html=True)
            
            # Create hourly forecast
            cols = st.columns(8)
            for i, hour in enumerate(weather_data["hourly"][:8]):
                with cols[i % 8]:
                    st.markdown(f"""
                        <div style="text-align: center; padding: 10px 0;">
                            <div>{hour['time']}</div>
                            <div style="font-size: 1.5rem;">{hour['icon']}</div>
                            <div style="font-weight: 600;">{hour['temp']}°</div>
                            <div style="font-size: 0.8rem; color: #94a3b8;">
                                {hour['precip']}% 💧
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3>7-Day Weather Forecast</h3>', unsafe_allow_html=True)
            
            # Create daily forecast
            for day in weather_data["daily"]:
                col_day, col_icon, col_temp, col_precip = st.columns([1, 1, 2, 1])
                
                with col_day:
                    st.markdown(f"**{day['day']}**")
                
                with col_icon:
                    st.markdown(f"<div style='font-size: 1.5rem;'>{day['icon']}</div>", unsafe_allow_html=True)
                
                with col_temp:
                    st.markdown(f"{day['low']}° - {day['high']}°")
                    st.progress((day['high'] - 60) / 30)
                
                with col_precip:
                    st.markdown(f"{day['precip']}% 💧")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Map section
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3>Weather Radar Map</h3>', unsafe_allow_html=True)
            
            # Create map
            map_center = [40.7128, -74.0060]  # New York coordinates
            m = folium.Map(location=map_center, zoom_start=11, tiles="CartoDB dark_matter")
            
            # Add markers
            folium.Marker(
                location=map_center,
                popup="New York",
                icon=folium.Icon(color="blue", icon="cloud")
            ).add_to(m)
            
            # Add radar overlay (simulated)
            folium.Circle(
                location=map_center,
                radius=5000,
                color="#1abc9c",
                fill=True,
                fill_color="#1abc9c",
                fill_opacity=0.2
            ).add_to(m)
            
            folium_static(m, height=300)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
