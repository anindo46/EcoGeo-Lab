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

def calculate_qfl_components(df):
    df["q"] = df["qm"] + df["qp"]
    df["f"] = df["k"] + df["p"]
    df["l"] = df["lm"] + df["ls"] + df["lv"]
    return df

def calculate_mia(df):
    df["mia"] = (df["q"] / (df["q"] + df["k"] + df["p"])) * 100 if "k" in df.columns and "p" in df.columns else (df["q"] / (df["q"] + df["f"])) * 100
    return df

def interpret_mia(value):
    if value > 75:
        return "Very high MIA suggests intense chemical weathering and sediment maturity—likely humid climate."
    elif value > 50:
        return "Moderate to high MIA suggests recycled sources and semi-humid environments."
    elif value > 25:
        return "Moderate MIA implies moderate tectonic input—transitional or semi-arid settings."
    else:
        return "Low MIA indicates immature sediments, likely arid climates or tectonically active areas."

def plot_qfl_triangle(data):
    fig, tax = ternary.figure(scale=100)
    fig.set_size_inches(6, 6)
    tax.set_title("QFL Triangle", fontsize=15)
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="gray", multiple=10)
    tax.left_axis_label("F", fontsize=12)
    tax.right_axis_label("L", fontsize=12)
    tax.bottom_axis_label("Q", fontsize=12)

    for _, row in data.iterrows():
        total = row["q"] + row["f"] + row["l"]
        if total > 0:
            q = row["q"] / total * 100
            f = row["f"] / total * 100
            l = row["l"] / total * 100
            tax.scatter([(q, f, l)], marker="o", color="blue", s=30)

    tax.ticks(axis='lbr', multiple=10, linewidth=1)
    tax.clear_matplotlib_ticks()
    st.pyplot(fig)

def show_reference_diagram(selection):
    fig, ax = plt.subplots()
    ax.set_title(selection)
    ax.plot([0, 50, 100], [0, 100, 0], linestyle='--', label=selection)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.legend()
    st.pyplot(fig)

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
