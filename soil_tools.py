import streamlit as st
import pandas as pd
import plotly.express as px

def soil_texture_triangle():
    st.subheader("🧱 Soil Texture Triangle (USDA Approximation)")

    st.markdown("""
    Upload a CSV/Excel file with **Sand**, **Silt**, and **Clay** percentages.  
    Columns must be named exactly: `Sand`, `Silt`, `Clay`  
    Values should total ~100.
    """)

    uploaded_file = st.file_uploader("📤 Upload Soil Texture Data", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df)

            if not all(col in df.columns for col in ["Sand", "Silt", "Clay"]):
                st.error("❌ Columns must include: Sand, Silt, Clay")
                return

            # Normalize to 100% if needed
            df_total = df[["Sand", "Silt", "Clay"]].sum(axis=1)
            df["Sand"] = df["Sand"] / df_total * 100
            df["Silt"] = df["Silt"] / df_total * 100
            df["Clay"] = df["Clay"] / df_total * 100

            fig = px.scatter_ternary(df,
                                     a="Clay", b="Silt", c="Sand",
                                     color="Clay",
                                     size_max=10,
                                     hover_name=df.index.astype(str),
                                     title="Soil Texture Triangle (Simplified View)")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Upload a CSV or Excel file to begin.")
