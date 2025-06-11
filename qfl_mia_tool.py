import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io
import ternary  # python-ternary must be installed

def calculate_qfl_components(df):
    df['Q'] = df['Qm'] + df['Qp']
    df['F'] = df['K'] + df['P']
    df['L'] = df['Lm'] + df['Ls'] + df['Lv']
    return df

def calculate_mia(df):
    df['MIA'] = (df['Q'] / (df['Q'] + df['K'] + df['P'])) * 100
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

    # Plot points
    for _, row in data.iterrows():
        total = row['Q'] + row['F'] + row['L']
        if total > 0:
            q = row['Q'] / total * 100
            f = row['F'] / total * 100
            l = row['L'] / total * 100
            tax.scatter([(q, f, l)], marker='o', color='blue', s=30)

    tax.ticks(axis='lbr', multiple=10, linewidth=1)
    tax.clear_matplotlib_ticks()
    st.pyplot(fig)

def qfl_and_mia_tool():
    st.header("🔍 QFL & MIA Tool")

    with st.expander("📘 How to Use"):
        st.markdown("""
        1. Upload a CSV or enter data manually with columns: `Qm`, `Qp`, `K`, `P`, `Lm`, `Ls`, `Lv`
        2. Do not include a header row inside the data body.
        3. Click **Next** to calculate Q, F, L and MIA index.
        4. View results, plot and download CSV.
        """)
        st.code("Qm, Qp, K, P, Lm, Ls, Lv\n48.4, 7.8, 7.8, 5.4, 7.6, 8, 0", language="csv")

    input_mode = st.radio("Choose Input Method", ["Upload CSV", "Manual Entry"])

    df = None

    if input_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data", df)

    else:
        sample_data = pd.DataFrame({
            "Qm": [48.4, 51, 50.8, 48.4, 32],
            "Qp": [7.8, 9.8, 6.2, 10.2, 8],
            "K": [7.8, 5.2, 2.2, 4.2, 7.2],
            "P": [5.4, 2.4, 3.4, 3.4, 2.6],
            "Lm": [7.6, 6.4, 5.2, 5.2, 12],
            "Ls": [8, 7.2, 6, 3.4, 10.2],
            "Lv": [0, 0, 0, 0, 0]
        })
        df = st.data_editor(sample_data, use_container_width=True, num_rows="dynamic", key="manual_table")

    if df is not None and st.button("Next"):
        try:
            # Remove any accidental header rows (e.g., Qm as a string inside the data)
            df = df[df['Qm'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]

            # Convert all relevant columns to float
            cols_needed = ["Qm", "Qp", "K", "P", "Lm", "Ls", "Lv"]
            df[cols_needed] = df[cols_needed].astype(float)

            df = calculate_qfl_components(df)
            df = calculate_mia(df)

            st.success("✅ Calculation Complete")

            st.write("### 📊 Result Table")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Result CSV", csv, "qfl_mia_result.csv", "text/csv")

            st.write("### 🔺 QFL Triangle Plot")
            plot_qfl_triangle(df)

        except Exception as e:
            st.error(f"❌ Error: {e}")
