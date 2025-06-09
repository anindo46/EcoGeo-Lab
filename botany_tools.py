import streamlit as st
import pandas as pd
import numpy as np

def biodiversity_index_calculator():
    st.subheader("🌿 Biodiversity Index Calculator")
    st.markdown("Upload a CSV or Excel file with **Species** and **Abundance** columns")

    uploaded_file = st.file_uploader("📤 Upload Biodiversity Data", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df.head())

            if not all(col in df.columns for col in ["Species", "Abundance"]):
                st.error("⚠️ Columns must include 'Species' and 'Abundance'")
                return

            total_abundance = df["Abundance"].sum()
            df["Proportion"] = df["Abundance"] / total_abundance

            # Shannon-Wiener Index (H')
            shannon_index = -np.sum(df["Proportion"] * np.log(df["Proportion"]))

            # Simpson's Index (D)
            simpson_index = np.sum(df["Proportion"] ** 2)

            # Evenness
            species_count = df.shape[0]
            evenness = shannon_index / np.log(species_count)

            st.markdown(f"""
            #### 📌 Biodiversity Indices:
            - **Shannon-Wiener Index (H')**: `{shannon_index:.4f}`
            - **Simpson’s Index (D)**: `{simpson_index:.4f}`
            - **Evenness (E)**: `{evenness:.4f}`
            """)

            st.bar_chart(df.set_index("Species")["Abundance"])

            # Download Results
            df["Shannon"] = df["Proportion"] * np.log(df["Proportion"])
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Analysis CSV", csv, "biodiversity_analysis.csv")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Please upload species data to begin.")
