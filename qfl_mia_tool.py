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



    input_type = st.radio("Choose Input Type:", ["🔬 Full Mineral Data (Qm, Qp, K, P, etc.)", "📊 Direct Q-F-L Values"])

    df = None
    if input_type == "🔬 Full Mineral Data (Qm, Qp, K, P, etc.)":
        st.subheader("Full Component Input")
        input_mode = st.radio("Choose Method", ["Upload CSV", "Manual Entry"])
        if input_mode == "Upload CSV":
            uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                df = standardize_columns(df)
                st.dataframe(df)
        else:
            sample_data = pd.DataFrame({
                "Qm": [48.4], "Qp": [7.8], "Feldspar": [7.8],
                "Mica": [5.4], "Lm": [7.6], "Ls": [8], "Lithic Fragment": [0]
            })
            df = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)
            df = standardize_columns(df)

        if df is not None and st.button("Next"):
            try:
                expected = ["qm", "qp", "k", "p", "lm", "ls", "lv"]
                df[expected] = df[expected].apply(pd.to_numeric, errors="coerce")
                df.dropna(subset=expected, inplace=True)
                df = calculate_qfl_components(df)
                df = calculate_mia(df)
            except Exception as e:
                st.error(f"Error: {e}")
                return

    else:
        st.subheader("Direct Q-F-L Input")
        input_mode = st.radio("Choose Method", ["Upload CSV", "Manual Entry"])
        if input_mode == "Upload CSV":
            uploaded_file = st.file_uploader("Upload CSV with Q, F, L", type=["csv"])
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                df.columns = [c.strip().lower() for c in df.columns]
                st.dataframe(df)
        else:
            sample_data = pd.DataFrame({"Q": [60], "F": [30], "L": [10]})
            df = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)

        if df is not None and st.button("Next"):
            try:
                df.columns = [c.strip().lower() for c in df.columns]
                df = df.rename(columns={"q": "q", "f": "f", "l": "l"})
                df = df[["q", "f", "l"]].apply(pd.to_numeric, errors="coerce")
                df.dropna(inplace=True)
                df = calculate_mia(df)
            except Exception as e:
                st.error(f"Error: {e}")
                return

    if df is not None and "q" in df.columns and "f" in df.columns and "l" in df.columns:
        st.success("✅ QFL & MIA Calculated")
        st.dataframe(df, use_container_width=True)

        for i, row in df.iterrows():
            st.info(f"Sample {i+1}: Q = {row['q']:.2f}, F = {row['f']:.2f}, L = {row['l']:.2f}")

        st.markdown("### 🧠 MIA Interpretation")
        for i, row in df.iterrows():
            mia = row.get("mia", 0)
            st.warning(f"Sample {i+1}: MIA = {mia:.2f}% → {interpret_mia(mia)}")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Results CSV", csv, file_name="qfl_mia_results.csv")

        st.markdown("### 🔺 QFL Diagram")
        plot_qfl_triangle(df)

        st.markdown("### 📊 View Reference Diagram")
        diagram_choice = st.selectbox("Choose a diagram", [
            "QFL Provenance Diagram",
            "Weathering Climate Diagram",
            "Sandstone Classification Diagram"
        ])
        show_reference_diagram(diagram_choice)
