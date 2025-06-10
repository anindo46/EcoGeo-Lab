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

# QFL & MIA Tool import
from qfl_mia_tool import qfl_and_mia_tool  # Ensure this import works, qfl_mia_tool.py must exist

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
        "🧬 3D Visualization",
        "📊 QFL & MIA Tool"  # Added QFL tool here
    ])

    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#666;'>💡 Tip: Upload CSV or Excel data for each module</p>
    """, unsafe_allow_html=True)

# Home Page
def display_home():
    col1, col2 = st.columns([1, 2])
    with col1:
        lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_w98qte06.json")
        if lottie:
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
    st.success("👈 Select a tool from the sidebar to get started!")

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
elif module == "📊 QFL & MIA Tool":  # Add new module to the routing
    qfl_and_mia_tool()  # Calling the QFL and MIA tool

# Footer
footer()
