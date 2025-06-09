import streamlit as st
from PIL import Image

# Module imports
from geology_tools import grain_size_analysis
from soil_tools import soil_texture_triangle
from botany_tools import biodiversity_index_calculator
from coastal_tools import coastal_ndwi_viewer
from general_tools import general_data_tools
from ai_tools import ai_prediction_tool
from visual_3d_tools import visual_3d_tool
from footer import footer

# Optional Lottie
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page Config
st.set_page_config(
    page_title="EcoGeo Lab | By Anindo Paul Sourav",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Pro UI Styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #e0eafc, #f7fbff);
        font-family: 'Segoe UI', sans-serif;
    }
    .credit {
        text-align: center;
        font-size: 14px;
        margin-top: 2rem;
        color: #444;
    }
    .module-card {
        background: linear-gradient(120deg, #4e54c8, #8f94fb);
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        margin: 1.5rem auto;
        width: 90%;
        max-width: 650px;
        color: white;
        text-align: center;
    }
    .module-card h3 {
        margin-bottom: 0.8rem;
        font-size: 17px;
        font-weight: 600;
    }
    .block-container {
        padding-top: 2rem;
    }
    ul li {
        margin: 6px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Branding (Logo, Tips, and Description)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### 🧪 EcoGeo Lab")
    st.caption("A Smart Environmental Science Toolkit")
    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#555;'>EcoGeo Lab is a browser-based research toolkit designed for students and scientists in Geology, Soil, Botany, Coastal Science, and AI-powered environmental studies. Use each module to visualize, analyze, and export your data seamlessly.</p>
    <p style='font-size:14px; color:#666;'>💡 Tip: Upload CSV or Excel data for each module</p>
    """, unsafe_allow_html=True)

# Welcome Section
st.markdown("""
<div class='module-card'>
    <h2 style='margin-bottom:0.4rem;'>Welcome to <span style='color:#f9f9f9;'>EcoGeo Lab</span></h2>
    <p style='font-size:13px;'>An all-in-one toolkit for Geoscience, Botany, Soil, Coastal, AI, and 3D Visualization.</p>
</div>
""", unsafe_allow_html=True)

# Routing
module = st.selectbox("📦 Select Your Tool Module", [
    "🏠 Home",
    "🪨 Geology Tools",
    "🧱 Soil Tools",
    "🌿 Botany Tools",
    "🌊 Coastal Tools",
    "📊 General Tools",
    "🤖 AI Predictions",
    "🦮 3D Visualization"
], index=0)

# Instruction at the end
st.markdown("""
---
### ℹ️ How to Use EcoGeo Lab:
- Choose a tool module from the list above
- Upload your dataset (CSV/Excel) or enter values manually
- Analyze data using built-in calculations
- Download charts and reports with one click

Use it for class projects, research, or exploration — all from your browser 🚀
""")

# Credit
st.markdown("""
<div class='credit'>
    Made with ❤️ by <strong>Anindo Paul Sourav</strong><br>
    Student, Department of Geology & Mining,<br>
    University of Barishal — Climate Innovator | GIS & Remote Sensing Enthusiast
</div>
""", unsafe_allow_html=True)

# Module execution
if module == "🏠 Home":
    pass
elif module == "🪨 Geology Tools":
    grain_size_analysis()
elif module == "🧱 Soil Tools":
    soil_texture_triangle()
elif module == "🌿 Botany Tools":
    biodiversity_index_calculator()
elif module == "🌊 Coastal Tools":
    coastal_ndwi_viewer()
elif module == "📊 General Tools":
    general_data_tools()
elif module == "🤖 AI Predictions":
    ai_prediction_tool()
elif module == "🦮 3D Visualization":
    visual_3d_tool()

# Footer
footer()
