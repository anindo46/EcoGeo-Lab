import streamlit as st
from PIL import Image
import pandas as pd
from footer import footer  # Ensure this import is correct

# Optional Lottie
from streamlit_lottie import st_lottie
import requests

# QFL & MIA Tool import
from qfl_mia_tool import qfl_and_mia_tool  # Ensure this import works, qfl_mia_tool.py must exist

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
        "📊 QFL & MIA Tool"
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

# QFL & MIA Tool
def qfl_mia_tool():
    st.title("📊 QFL & MIA Tool")

    # CSV Upload or Manual Input
    input_method = st.radio("Select Input Method:", ["📤 Upload CSV/Excel", "✍️ Manual Entry"], key="input_method")

    if input_method == "📤 Upload CSV/Excel":
        uploaded_file = st.file_uploader("Upload CSV or Excel with 'Q', 'F', and 'L' values", type=['csv', 'xlsx'])

        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Check for necessary columns
                required_columns = ['Q', 'F', 'L']
                if not all(col in df.columns for col in required_columns):
                    st.error("❌ Please ensure the CSV contains 'Q', 'F', and 'L' columns.")
                else:
                    st.write("### Data Preview", df)

                    # Generate QFL and MIA Tool outputs
                    df, plot_buf = qfl_and_mia_tool(df)

                    # Show updated dataframe with MIA column
                    st.write("### Updated Data with MIA", df)

                    # Provide downloadable chart
                    st.download_button("📥 Download Plot as PNG", plot_buf.getvalue(), file_name="qfl_plot.png")

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")

    elif input_method == "✍️ Manual Entry":
        st.write("Enter your Q, F, L values manually:")

        # Input fields for Q, F, L values
        q_values = st.text_area("Enter Q values (comma separated)").split(',')
        f_values = st.text_area("Enter F values (comma separated)").split(',')
        l_values = st.text_area("Enter L values (comma separated)").split(',')

        # Ensure that the values are numeric
        try:
            q_values = [float(val.strip()) for val in q_values]
            f_values = [float(val.strip()) for val in f_values]
            l_values = [float(val.strip()) for val in l_values]

            # Create a DataFrame
            df = pd.DataFrame({'Q': q_values, 'F': f_values, 'L': l_values})

            # Show Data Preview
            st.write("### Data Preview", df)

            # Generate QFL and MIA Tool outputs
            df, plot_buf = qfl_and_mia_tool(df)

            # Show updated dataframe with MIA column
            st.write("### Updated Data with MIA", df)

            # Provide downloadable chart
            st.download_button("📥 Download Plot as PNG", plot_buf.getvalue(), file_name="qfl_plot.png")

        except ValueError:
            st.error("❌ Please enter valid numeric values.")

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
elif module == "📊 QFL & MIA Tool":
    qfl_mia_tool()

# Footer
footer()
