import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

def grain_size_analysis():
    st.subheader("📊 Grain Size Analysis (Folk & Ward Method)")

    uploaded_file = st.file_uploader("Upload CSV/Excel with 'Grain Size (mm)' and 'Weight (%)'", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df.head())

            size = df["Grain Size (mm)"].values
            weight = df["Weight (%)"].values

            # Convert to phi scale
            phi = -np.log2(size)
            phi_sorted = np.sort(phi)
            weight_sorted = weight[np.argsort(phi)]

            cumulative_weight = np.cumsum(weight_sorted) / np.sum(weight_sorted) * 100

            # Interpolation for Folk & Ward parameters
            def interpolate(x, y, percentile):
                return np.interp(percentile, y, x)

            phi16 = interpolate(phi_sorted, cumulative_weight, 16)
            phi50 = interpolate(phi_sorted, cumulative_weight, 50)
            phi84 = interpolate(phi_sorted, cumulative_weight, 84)
            phi5 = interpolate(phi_sorted, cumulative_weight, 5)
            phi95 = interpolate(phi_sorted, cumulative_weight, 95)

            mean = (phi16 + phi50 + phi84) / 3
            sorting = (phi84 - phi16) / 4 + (phi95 - phi5) / 6.6
            skewness = ((phi16 + phi84 - 2*phi50)/(2*(phi84 - phi16))) + ((phi5 + phi95 - 2*phi50)/(2*(phi95 - phi5)))
            kurtosis = (phi95 - phi5) / (2.44 * (phi75 - phi25)) if 'phi75' in locals() else None

            st.markdown(f"""
            #### 📌 Folk & Ward Parameters:
            - Mean (Mz): `{mean:.2f}`
            - Sorting (σ): `{sorting:.2f}`
            - Skewness (Sk): `{skewness:.2f}`
            """)

            # Plot cumulative curve
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(phi_sorted, cumulative_weight, marker='o')
            ax.set_title("Cumulative Grain Size Distribution")
            ax.set_xlabel("Phi Scale")
            ax.set_ylabel("Cumulative % Weight")
            ax.grid(True)
            st.pyplot(fig)

            # Download plot
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Plot as Image", data=buf.getvalue(), file_name="grain_size_plot.png")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Please upload a dataset to begin.")
