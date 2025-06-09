import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

def coastal_ndwi_viewer():
    st.subheader("🌊 NDWI & Shoreline Change Viewer")

    st.markdown("""
    Upload pre-processed **satellite band data** (e.g. Green and NIR) in CSV/Excel format  
    - Format: Each row should represent a pixel  
    - Columns required: `Green`, `NIR`
    """)

    uploaded_file = st.file_uploader("📤 Upload Satellite Pixel Data", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df.head())

            if not all(col in df.columns for col in ["Green", "NIR"]):
                st.error("⚠️ Required columns: Green, NIR")
                return

            df["NDWI"] = (df["Green"] - df["NIR"]) / (df["Green"] + df["NIR"])
            st.line_chart(df["NDWI"])

            st.markdown(f"""
            #### 📌 NDWI Summary:
            - **Min NDWI**: `{df["NDWI"].min():.4f}`
            - **Max NDWI**: `{df["NDWI"].max():.4f}`
            - **Mean NDWI**: `{df["NDWI"].mean():.4f}`
            """)

            csv_export = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download NDWI Data", csv_export, "ndwi_output.csv")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Upload Green/NIR data to calculate NDWI.")
