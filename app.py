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
        font-size: 16px;
        margin-top: 2rem;
        margin-bottom: -1.5rem;
        color: #4a4a4a;
    }
    .module-card {
        background: linear-gradient(120deg, #4e54c8, #8f94fb);
        padding: 1.5rem 1rem;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin: 2rem auto 1rem;
        width: 90%;
        max-width: 700px;
        color: white;
        text-align: center;
    }
    .module-card h3 {
        margin-bottom: 1rem;
        font-size: 22px;
        font-weight: 600;
    }
    .stSelectbox label {
        font-size: 16px;
        color: #333;
    }
    div[data-baseweb="select"] > div {
        border-radius: 10px;
        padding: 10px;
        font-size: 15px;
    }
    .block-container {
        padding-top: 2rem;
    }
    ul li {
        margin: 6px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Branding (Logo and Tips)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### 🧪 EcoGeo Lab")
    st.caption("A Smart Environmental Science Toolkit")
    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#666;'>💡 Tip: Upload CSV or Excel data for each module</p>
    """, unsafe_allow_html=True)

# Welcome Section
col1, col2 = st.columns([1, 2])
with col1:
    lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_w98qte06.json")
    if lottie:
        st_lottie(lottie, speed=1, loop=True, height=250)
    else:
        st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=200)
with col2:
    st.markdown("""
    <h2 style='color:#2c3e50; margin-bottom: 0;'>Welcome to <span style='color:#4B8BBE;'>EcoGeo Lab</span></h2>
    <p style='font-size:17px;'>An interactive web toolkit for Geoscience, Soil, Botany, Coastal, AI, and 3D Visualization.</p>
    <ul>
        <li>📂 Upload or manually enter your data</li>
        <li>📊 Instantly visualize results with professional charts</li>
        <li>📥 Export outcomes as PNG, CSV, or PDF</li>
    </ul>
    """, unsafe_allow_html=True)

# Module Selector Below Welcome
st.markdown("<div class='module-card'><h3>📦 Select Your Tool Module</h3>", unsafe_allow_html=True)
module = st.selectbox("Select Module", [
    "🏠 Home",
    "🪨 Geology Tools",
    "🧱 Soil Tools",
    "🌿 Botany Tools",
    "🌊 Coastal Tools",
    "📊 General Tools",
    "🤖 AI Predictions",
    "🦮 3D Visualization"
], index=0)
st.markdown("</div>", unsafe_allow_html=True)

# Credit
st.markdown("<div class='credit'>By Anindo Paul Sourav — Geology & Mining, University of Barishal</div>", unsafe_allow_html=True)

# Routing
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
