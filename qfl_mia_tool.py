import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import ternary

# 🌟 Inject Custom CSS for Style
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

# ✅ Standardize & resolve column conflicts
def standardize_columns(df):
    df.columns = [c.strip().lower() for c in df.columns]

    rename_map = {
        "feldspar": "k",
        "mica": "p",
        "lithic fragment": "lv",
    }

    # Only rename if target column not already present
    for old, new in rename_map.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})

    # Drop duplicate columns if still exists
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# ➕ QFL/MIA Calculations
def calculate_qfl_components(df):
    df["q"] = df["qm"] + df["qp"]
    df["f"] = df["k"] + df["p"]
    df["l"] = df["lm"] + df["ls"] + df["lv"]
    return df

def calculate_mia(df):
    df["mia"] = (df["q"] / (df["q"] + df["k"] + df["p"])) * 100
    return df

# 🔺 Triangle Plot
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

# 🧪 Main Tool
def qfl_and_mia_tool():
    inject_css()
    st.header("🔍 QFL & MIA Tool")

    with st.expander("📘 How to Use"):
        st.markdown("""
        - Upload CSV or use manual input. Allowed headers:  
          `Qm`, `Qp`, `K` or `Feldspar`, `P` or `Mica`, `Lm`, `Ls`, `Lv` or `Lithic Fragment`
        - Press **Next** to view QFL plot and MIA result.
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
            "Feldspar": [7.8, 5.2, 3.8],     # will become 'k'
            "Mica": [5.4, 2.4, 4.4],         # will become 'p'
            "Lm": [7.6, 7.8, 6.8],
            "Ls": [8, 5.6, 5.4],
            "Lithic Fragment": [0, 2, 0]     # will become 'lv'
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

            st.success("✅ Done! Here’s your QFL + MIA data.")
            st.dataframe(df[["qm", "qp", "k", "p", "lm", "ls", "lv", "q", "f", "l", "mia"]], use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Results CSV", csv, file_name="qfl_mia_results.csv")

            st.write("### 🔺 QFL Triangle Plot")
            plot_qfl_triangle(df)

        except Exception as e:
            st.error(f"❌ Error occurred: {str(e)}")
