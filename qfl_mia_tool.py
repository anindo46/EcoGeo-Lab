import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import ternary

def inject_css():
    st.markdown("""
        <style>
        .stButton>button, .stDownloadButton>button {
            background-color: #009999;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .st-expander>summary {
            font-weight: bold;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

# Ensure this tool can be run standalone or imported into app.py
# Just define the tool function, and let app.py handle calling it.

# All functions remain unchanged, and we will now define qfl_and_mia_tool to prevent ImportError

def standardize_columns(df):
    df.columns = [c.strip().lower() for c in df.columns]
    rename_map = {
        "feldspar": "k",
        "mica": "p",
        "lithic fragment": "lv",
    }
    for old, new in rename_map.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# Place all other function definitions here (calculate_qfl_components, calculate_mia, interpret_mia, etc.)

# Final tool definition

def qfl_and_mia_tool():
    inject_css()
    st.header("🔍 QFL & MIA Tool")

    with st.expander("📘 How to Use This Tool"):
        st.markdown("""
    ### 🔹 Available Input Options:
    - **Full Mineral Data**: Use this if you have raw component data like `Qm`, `Qp`, `K`/`Feldspar`, `P`/`Mica`, `Lm`, `Ls`, `Lv`.
    - **Direct Q-F-L Values**: Use if you've already calculated or been given `Q`, `F`, `L`.

    ### 🧪 Steps for Full Mineral Data:
    1. Select "🔬 Full Mineral Data" from the top.
    2. Upload CSV or enter manually.
    3. Click **Next** to calculate Q, F, L and MIA.
    4. View triangle plot, interpretation, and reference diagrams.

    ### 📊 Steps for Direct Q-F-L Input:
    1. Select "📊 Direct Q-F-L Values" from the top.
    2. Upload or enter Q, F, L data directly.
    3. Click **Next** to analyze.

    ### 📁 Reference Diagrams:
    Use the dropdown at the bottom to switch between:
    - QFL Provenance
    - Weathering Climate
    - Sandstone Classification

    **📥 Download** results after processing, including Q, F, L and MIA.
    """)

# Automatically run the tool if script is executed directly
if __name__ == "__main__":
    qfl_and_mia_tool()
