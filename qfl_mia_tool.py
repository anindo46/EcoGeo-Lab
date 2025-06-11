import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io
import ternary  # Requires python-ternary package

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
            tax.scatter([(q, f, l)], marker='o', color='blue', label='Sample', s=30)

    tax.ticks(axis='lbr', multiple=10, linewidth=1)
    tax.clear_matplotlib_ticks()
    tax.legend()
    st.pyplot(fig)

def qfl_and_mia_tool():
    st.header("🔍 QFL & MIA Tool")
    
    with st.expander("📘 How to Use"):
        st.markdown("""
        1. Upload a CSV or enter data manually with columns: `Qm`, `Qp`, `K`, `P`, `Lm`, `Ls`, `Lv`
        2. Click **Next** to calculate `Q`, `F`, `L` and `MIA`
        3. View the QFL triangle and download results
        """)
        st.markdown("📂 Sample Format:")
        st.code("Qm, Qp, K, P, Lm, Ls, Lv\n10, 5, 3, 2, 4, 1, 2", language="csv")

    input_mode = st.radio("Choose Input Method", ["Upload CSV", "Manual Entry"])

    if input_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data", df)
    else:
        sample_data = pd.DataFrame({
            "Qm": [10], "Qp": [5], "K": [3], "P": [2],
            "Lm": [4], "Ls": [1], "Lv": [2]
        })
        df = st.data_editor(sample_data, use_container_width=True, num_rows="dynamic", key="manual_editor")

    if 'df' in locals() and st.button("Next"):
        try:
            df = df.astype(float)
            df = calculate_qfl_components(df)
            df = calculate_mia(df)

            st.success("✅ Calculation Complete")

            st.write("### 📊 Result Table", df)

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "qfl_mia_results.csv", "text/csv")

            # QFL Triangle
            st.write("### 🔺 QFL Triangle")
            plot_qfl_triangle(df)

        except Exception as e:
            st.error(f"❌ Error: {e}")
