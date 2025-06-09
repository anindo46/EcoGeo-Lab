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

# Sidebar UI (branding only)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### 🧪 EcoGeo Lab")
    st.caption("By **Anindo Paul Sourav**  \nGeology & Mining, University of Barishal")
    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#666;'>💡 Tip: Upload CSV or Excel data for each module</p>
    """, unsafe_allow_html=True)

# 🌈 Gradient CSS styling for module selector
st.markdown("""
    <style>
    .module-select {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .stSelectbox label {
        font-size: 18px !important;
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# 🎯 Main Page Module Selector
st.markdown("<div class='module-select'><h2>Select a Tool Module</h2></div>", unsafe_allow_html=True)

module = st.selectbox("", [
    "🏠 Home",
    "🪨 Geology Tools",
    "🧱 Soil Tools",
    "🌿 Botany Tools",
    "🌊 Coastal Tools",
    "📊 General Tools",
    "🤖 AI Predictions",
    "🧬 3D Visualization"
], index=0)

# Home Page
def display_home():
    col1, col2 = st.columns([1, 2])
    with col1:
        lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_w98qte06.json")
        if lottie:
            from streamlit_lottie import st_lottie
            st_lottie(lottie, speed=1, loop=True, height=250)
        else:
            st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=200)
    with col2:
        st.markdown("<h1 style='color:#4B8BBE;'>Welcome to EcoGeo Lab</h1>", unsafe_allow_html=True)
        st.markdown("""
        <p style='font-size:18px;'>Your all-in-one smart science lab for Geology, Soil, Botany, and Coastal Research.</p>
        <ul>
            <li>📁 Upload datasets easily</li>
            <li>📊 Get instant analysis & plots</li>
            <li>📥 Export results as image, CSV, or PDF</li>
        </ul>
        """, unsafe_allow_html=True)
    st.success("👇 Select a tool module above to get started!")

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
