import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# QFL & MIA Tool import
from qfl_mia_tool import qfl_and_mia_tool  # Ensure this import works, qfl_mia_tool.py must exist

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

# QFL & MIA Tool
def qfl_mia_tool():
    st.title("📊 QFL & MIA Tool")

    # CSV Upload or Manual Input
    input_method = st.radio("Select Input Method:", ["📤 Upload CSV/Excel", "✍️ Manual Entry"], key="input_method")

    if input_method == "📤 Upload CSV/Excel":
        uploaded_file = st.file_uploader("Upload CSV or Excel with 'Qm', 'Qp', and 'F' values", type=['csv', 'xlsx'])

        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Check for necessary columns
                required_columns = ['Qm', 'Qp', 'F']
                if not all(col in df.columns for col in required_columns):
                    st.error("❌ Please ensure the CSV contains 'Qm', 'Qp', and 'F' columns.")
                else:
                    st.write("### Data Preview", df)

                    # Generate Q, F, L from Qm and Qp
                    df['Q'] = df['Qm'] / (df['Qm'] + df['Qp']) * 100
                    df['F'] = df['F']  # We assume F is already given
                    df['L'] = 100 - df['Q'] - df['F']

                    # Show updated dataframe with Q, F, L values
                    st.write("### Updated Data with Q, F, L", df)

                    # Generate QFL and MIA Tool outputs
                    df, plot_buf = qfl_and_mia_tool(df)

                    # Show updated dataframe with MIA column
                    st.write("### Updated Data with MIA", df)

                    # Provide downloadable chart
                    st.download_button("📥 Download Plot as PNG", plot_buf.getvalue(), file_name="qfl_plot.png")

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")

    elif input_method == "✍️ Manual Entry":
        st.write("Enter your Qm, Qp, and F values manually:")

        # Input fields for Qm, Qp, and F values
        q_values = st.text_area("Enter Qm values (comma separated)").split(',')
        qp_values = st.text_area("Enter Qp values (comma separated)").split(',')
        f_values = st.text_area("Enter F values (comma separated)").split(',')

        # Ensure that the values are numeric
        try:
            q_values = [float(val.strip()) for val in q_values]
            qp_values = [float(val.strip()) for val in qp_values]
            f_values = [float(val.strip()) for val in f_values]

            # Calculate Q, F, L
            q = [(q / (q + qp)) * 100 for q, qp in zip(q_values, qp_values)]
            f = f_values
            l = [100 - q_f - f_f for q_f, f_f in zip(q, f)]

            # Create a DataFrame
            df = pd.DataFrame({'Qm': q_values, 'Qp': qp_values, 'F': f_values, 'Q': q, 'F': f, 'L': l})

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
