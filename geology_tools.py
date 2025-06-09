import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import random

def grain_size_analysis():
    st.subheader("🪨 Grain Size Analysis (Folk & Ward Method)")

    # 📘 Real-Life Use Case Guide
    with st.expander("📘 How to Use (Example: Sediment Analysis)", expanded=False):
        st.markdown("""
        ### 🪨 Scenario: Riverbed Sediment Analysis  
        You're analyzing sediment samples from three river stations. You've sieved the sample and calculated the percentage retained per sieve size.

        | Sieve Size (mm) | % Retained |
        |-----------------|------------|
        | 2.0             | 5  
        | 1.0             | 15  
        | 0.5             | 25  
        | 0.25            | 35  
        | 0.125           | 15  
        | 0.063           | 5  

        #### 🚀 Steps:
        - Choose `✍️ Manual Entry` or upload a CSV like above.
        - Click ✅ Apply.
        - View grain size statistics (mean, sorting, skewness).
        - Export chart or CSV.

        #### 💡 Use For:
        - Soil mechanics, sedimentology, coastal deposits.
        """)

    input_method = st.radio("Select Input Method:", ["📤 Upload CSV/Excel", "✍️ Manual Entry"], key="input_method")

    if input_method == "✍️ Manual Entry":
        st.markdown("### ✍️ Enter Grain Sizes and Weights")

        default_df = pd.DataFrame({
            "Grain Size (mm)": [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015],
            "Weight (%)": [0]*8
        })

        if "manual_data" not in st.session_state:
            st.session_state.manual_data = default_df.copy()
            st.session_state.editor_key = f"editor_{random.randint(1,10000)}"

        if st.button("🧹 Clear All Inputs"):
            st.session_state.manual_data = default_df.copy()
            st.session_state.editor_key = f"editor_{random.randint(1,10000)}"
            st.rerun()

        edited_df = st.data_editor(
            st.session_state.manual_data,
            num_rows="fixed",
            use_container_width=True,
            key=st.session_state.editor_key
        )

        if st.button("✅ Apply Data"):
            st.session_state.manual_data = edited_df.copy()
            st.success("✅ Data applied!")

        df = st.session_state.manual_data.copy()

    else:
        uploaded_file = st.file_uploader("Upload CSV or Excel with 'Grain Size (mm)' and 'Weight (%)'", type=['csv', 'xlsx'], key="upload_file")

        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.write("### 📄 Uploaded Data", df)

                if st.button("🧹 Clear Uploaded File"):
                    del st.session_state["upload_file"]
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
                return
        else:
            st.info("Upload a file to continue.")
            return

    # --- GRAIN SIZE ANALYSIS ---
    try:
        size = df["Grain Size (mm)"].astype(float).values
        weight = df["Weight (%)"].astype(float).values

        phi = -np.log2(size)
        phi_sorted = np.sort(phi)
        weight_sorted = weight[np.argsort(phi)]
        cumulative_weight = np.cumsum(weight_sorted) / np.sum(weight_sorted) * 100

        def interpolate(x, y, percentile):
            return np.interp(percentile, y, x)

        phi16 = interpolate(phi_sorted, cumulative_weight, 16)
        phi50 = interpolate(phi_sorted, cumulative_weight, 50)
        phi84 = interpolate(phi_sorted, cumulative_weight, 84)
        phi5 = interpolate(phi_sorted, cumulative_weight, 5)
        phi95 = interpolate(phi_sorted, cumulative_weight, 95)

        mean = (phi16 + phi50 + phi84) / 3
        sorting = (phi84 - phi16) / 4 + (phi95 - phi5) / 6.6
        skewness = ((phi16 + phi84 - 2 * phi50) / (2 * (phi84 - phi16))) + ((phi5 + phi95 - 2 * phi50) / (2 * (phi95 - phi5)))

        st.markdown(f"""
        ### 📌 Folk & Ward Parameters:
        - **Mean (Mz)**: `{mean:.2f}`
        - **Sorting (σ)**: `{sorting:.2f}`
        - **Skewness (Sk)**: `{skewness:.2f}`
        """)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(phi_sorted, cumulative_weight, marker='o', linestyle='-')
        ax.set_title("Cumulative Grain Size Curve")
        ax.set_xlabel("Phi Scale")
        ax.set_ylabel("Cumulative % Weight")
        ax.grid(True)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download Plot as PNG", buf.getvalue(), file_name="grain_size_curve.png")

    except Exception as e:
        st.error(f"⚠️ Processing Error: {e}")
