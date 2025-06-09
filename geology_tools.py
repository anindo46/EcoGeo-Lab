import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

def grain_size_analysis():
    st.subheader("🪨 Grain Size Analysis (Folk & Ward Method)")

    # --- Input Method Selection ---
    input_method = st.radio("Select Input Method:", ["📤 Upload CSV/Excel", "✍️ Manual Entry"], key="input_method")

    # --- Manual Entry ---
    if input_method == "✍️ Manual Entry":
        st.markdown("### ✍️ Enter Grain Sizes and Weights")

        default_df = pd.DataFrame({
            "Grain Size (mm)": [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015],
            "Weight (%)": [0]*8
        })

        # Initialize session
        if "manual_data" not in st.session_state:
            st.session_state.manual_data = default_df.copy()

        # Editable table
        edited_df = st.data_editor(
            st.session_state.manual_data,
            num_rows="fixed",
            use_container_width=True
        )

        # Apply / Clear buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Apply Data"):
                st.session_state.manual_data = edited_df.copy()
                st.success("Data applied successfully ✅")

        with col2:
            if st.button("🧹 Clear All Inputs"):
                st.session_state.manual_data = default_df.copy()
                st.rerun()

        df = st.session_state.manual_data.copy()

    # --- File Upload Entry ---
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

    # --- Grain Size Analysis ---
    try:
        size = df["Grain Size (mm)"].astype(float).values
        weight = df["Weight (%)"].astype(float).values

        # Phi scale and cumulative % calculation
        phi = -np.log2(size)
        phi_sorted = np.sort(phi)
        weight_sorted = weight[np.argsort(phi)]
        cumulative_weight = np.cumsum(weight_sorted) / np.sum(weight_sorted) * 100

        def interpolate(x, y, percentile):
            return np.interp(percentile, y, x)

        # Folk & Ward stats
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

        # Plot curve
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(phi_sorted, cumulative_weight, marker='o', linestyle='-')
        ax.set_title("Cumulative Grain Size Curve")
        ax.set_xlabel("Phi Scale")
        ax.set_ylabel("Cumulative % Weight")
        ax.grid(True)
        st.pyplot(fig)

        # Export PNG
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download Plot as PNG", buf.getvalue(), file_name="grain_size_curve.png")

    except Exception as e:
        st.error(f"⚠️ Processing Error: {e}")
