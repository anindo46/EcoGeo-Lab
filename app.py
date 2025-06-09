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

# Custom CSS for Pro UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #e0eafc, #cfdef3);
    }
    .credit {
        text-align: center;
        font-size: 16px;
        margin-top: 1rem;
        color: #555;
    }
    .module-card {
        background: linear-gradient(135deg, #4b6cb7, #182848);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin: 2rem auto;
        width: 80%;
        color: white;
        text-align: center;
    }
    .module-card h3 {
        margin-bottom: 1.5rem;
        font-size: 26px;
        letter-spacing: 0.5px;
    }
    .stSelectbox {
        background: white;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] > div {
        border-radius: 10px;
        padding: 6px;
        font-size: 16px;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Branding (for logo and tips only)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### 🧪 EcoGeo Lab")
    st.caption("A Smart Environmental Science Toolkit")
    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#666;'>💡 Tip: Upload CSV or Excel data for each module</p>
    """, unsafe_allow_html=True)

# Welcome Section (optional visual or message)
def display_home():
    col1, col2 = st.columns([1, 2])
    with col1:
        lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_w98qte06.json")
        if lottie:
            st_lottie(lottie, speed=1, loop=True, height=250)
        else:
            st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=200)
    with col2:
        st.markdown("""
        <h2 style='color:#2c3e50;'>Welcome to <span style='color:#4B8BBE;'>EcoGeo Lab</span></h2>
        <p style='font-size:18px;'>All-in-one smart lab for Geoscience, Soil, Botany, Coastal & AI tools.</p>
        <ul>
            <li>📁 Upload or input data manually</li>
            <li>📊 Generate interactive plots</li>
            <li>📄 Export as PNG, CSV, or PDF</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown("<div class='module-card'><h3>📦 Select Your Tool Module</h3>", unsafe_allow_html=True)
    module = st.selectbox("", [
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

    return module

# Display Credit
st.markdown("<div class='credit'>By Anindo Paul Sourav — Geology & Mining, University of Barishal</div>", unsafe_allow_html=True)

# Routing
module = display_home()
if module == "🏠 Home":
    pass  # Already displayed
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
