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

# Sidebar UI
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### 🧪 EcoGeo Lab")
    st.caption("By **Anindo Paul Sourav**  \nGeology & Mining, University of Barishal")
    st.markdown("---")

    module = st.selectbox("📦 Choose a Module", [
        "🏠 Home",
        "🪨 Geology Tools",
        "🧱 Soil Tools",
        "🌿 Botany Tools",
        "🌊 Coastal Tools",
        "📊 General Tools",
        "🤖 AI Predictions",
        "🧬 3D Visualization"
    ])

    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#666;'>💡 Tip: Upload CSV or Excel data for each module</p>
    """, unsafe_allow_html=True)


if module == "Home":
    st.title("🌍 Welcome to EcoGeo Lab")
    st.markdown("""
    <style>
    .big-title {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
    }
    .subtitle {
        font-size: 18px;
        color: #7f8c8d;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-title">🌍 EcoGeo Lab: Smart Toolkit for Environmental Sciences</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">📊 Visualize | 📈 Analyze | 🤖 Predict</p>', unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=150)

    st.markdown("""
    **EcoGeo Lab** integrates modern tools for:
    - 🪨 Geology
    - 🟫 Soil Science
    - 🌿 Botany
    - 🌊 Coastal Study
    - 📡 3D Visualization
    - 🤖 AI-based Forecasting

    👉 Use the sidebar to access modules  
    👉 Each tool includes real-life examples  
    👉 Export your results instantly (PNG, CSV)
    """)

    st.success("Start exploring from the sidebar 👈")



# Module Routing
if module == "🏠 Home":
    display_home()
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
elif module == "🧬 3D Visualization":
    visual_3d_tool()

# Footer
footer()
