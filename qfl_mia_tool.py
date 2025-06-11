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
    diagram_paths = {
        "QFL Provenance Diagram": "static/qfl_provenance.png",
        "Weathering Climate Diagram": "static/weathering_diagram.png",
        "Sandstone Classification Diagram": "static/sandstone_classification.png"
    }
    st.image(diagram_paths[selection], caption=selection, use_column_width=True)

# rest of the code remains unchanged
