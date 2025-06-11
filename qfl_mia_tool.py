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
    # Generate placeholder diagrams dynamically using matplotlib
    if selection == "QFL Provenance Diagram":
        fig, ax = plt.subplots()
        ax.set_title("QFL Provenance Diagram")
        ax.plot([15, 50, 37], [13, 50, 25], 'k--')  # Placeholder lines
        ax.fill_between([0, 15], 0, 100, color='#cce5df', label='Continental Block')
        ax.fill_between([15, 50], 0, 50, color='#e6f2ff', label='Magmatic Arc')
        ax.fill_between([15, 50], 50, 100, color='#eee', label='Recycled Orogen')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.legend()
        st.pyplot(fig)

    elif selection == "Weathering Climate Diagram":
        fig, ax = plt.subplots()
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title("Weathering Climate Diagram")
        ax.set_xlabel("Q / (F + L)")
        ax.set_ylabel("Qp / (F + L)")
        ax.text(0.2, 0.01, 'ARID', fontsize=10)
        ax.text(1.5, 0.03, 'SEMI ARID', fontsize=10)
        ax.text(5, 0.1, 'SEMI HUMID', fontsize=10)
        ax.text(20, 0.3, 'HUMID', fontsize=10)
        ax.arrow(1, 0.01, 15, 0.2, head_width=0.01, head_length=2, fc='gray', ec='gray')
        ax.set_xlim(0.1, 100)
        ax.set_ylim(0.001, 1)
        st.pyplot(fig)

    elif selection == "Sandstone Classification Diagram":
        fig, tax = ternary.figure(scale=100)
        fig.set_size_inches(6, 6)
        tax.boundary()
        tax.gridlines(multiple=25, color="gray")
        tax.set_title("Sandstone Classification Diagram", fontsize=15)
        tax.left_axis_label("Feldspar", fontsize=12)
        tax.right_axis_label("Lithics", fontsize=12)
        tax.bottom_axis_label("Quartz", fontsize=12)
        st.pyplot(fig)
