import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import ternary

def inject_css():
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #009999;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stDownloadButton>button {
            background-color: #006666;
            color: white;
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
    df["mia"] = (df["q"] / (df["q"] + df["k"] + df["p"])) * 100
    return df

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

def interpret_mia(value):
    if value > 75:
        return "Very high MIA suggests intense chemical weathering and sediment maturity—likely humid climatic influence."
    elif value > 50:
        return "Moderate to high MIA suggests recycling and intermediate weathering—possibly semi-humid to humid regions."
    elif value > 25:
        return "Low to moderate MIA may imply active tectonic input and less weathered detritus—transitional or semi-arid conditions."
    else:
        return "Very low MIA reflects immature sediments and minimal chemical weathering—likely arid conditions or direct arc origin."

def show_reference_diagram(selection):
    diagram_paths = {
        "QFL Provenance Diagram": "static/qfl_provenance.png",
        "Weathering Climate Diagram": "static/weathering_diagram.png",
        "Sandstone Classification Diagram": "static/sandstone_classification.png"
    }
    st.image(diagram_paths[selection], caption=selection, use_column_width=True)

def qfl_and_mia_tool():
    inject_css()
    st.header("🔍 QFL & MIA Tool")

    with st.expander("📘 How to Use"):
        st.markdown("""
        - Upload CSV or input manually: `Qm`, `Qp`, `K` or `Feldspar`, `P` or `Mica`, `Lm`, `Ls`, `Lv` or `Lithic Fragment`
        - Press **Next** to calculate QFL, MIA and see diagrams.
        - View reference diagrams from dropdown for provenance or climate insight.
        """)

    input_mode = st.radio("📥 Choose Input Method", ["Upload CSV", "Manual Entry"])
    df = None

    if input_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df = standardize_columns(df)
            st.dataframe(df, use_container_width=True)
    else:
        sample_data = pd.DataFrame({
            "Qm": [48.4, 50.2, 42.4],
            "Qp": [7.8, 5.8, 7.8],
            "Feldspar": [7.8, 5.2, 3.8],
            "Mica": [5.4, 2.4, 4.4],
            "Lm": [7.6, 7.8, 6.8],
            "Ls": [8, 5.6, 5.4],
            "Lithic Fragment": [0, 2, 0]
        })
        df = st.data_editor(sample_data, use_container_width=True, num_rows="dynamic", key="manual_input")
        df = standardize_columns(df)

    if df is not None and st.button("Next"):
        try:
            expected = ["qm", "qp", "k", "p", "lm", "ls", "lv"]
            missing = [col for col in expected if col not in df.columns]
            if missing:
                st.error(f"❌ Missing columns: {missing}")
                return

            df[expected] = df[expected].apply(pd.to_numeric, errors="coerce")
            df.dropna(subset=expected, inplace=True)

            df = calculate_qfl_components(df)
            df = calculate_mia(df)

            st.success("✅ QFL & MIA Calculated")
            st.dataframe(df[["qm", "qp", "k", "p", "lm", "ls", "lv", "q", "f", "l", "mia"]], use_container_width=True)

            st.markdown("### 📌 Highlighted Q, F, L Values")
            for i, row in df.iterrows():
                st.info(f"Sample {i+1} ➤ Q = {row['q']:.2f}, F = {row['f']:.2f}, L = {row['l']:.2f}")

            st.markdown("### 🧠 MIA Interpretation")
            for i, row in df.iterrows():
                st.warning(f"Sample {i+1}: MIA = {row['mia']:.2f}% → {interpret_mia(row['mia'])}")

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Results CSV", csv, file_name="qfl_mia_results.csv")

            st.markdown("### 🗺 Reference Diagram Viewer")
            diagram_choice = st.selectbox("Choose Diagram to View", [
                "QFL Provenance Diagram",
                "Weathering Climate Diagram",
                "Sandstone Classification Diagram"
            ])
            show_reference_diagram(diagram_choice)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
