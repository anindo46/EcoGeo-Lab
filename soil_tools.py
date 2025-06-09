import streamlit as st
import pandas as pd
import ternary
import matplotlib.pyplot as plt
import io

def soil_texture_triangle():
    st.subheader("🟫 Soil Texture Triangle (USDA)")

    st.markdown("Upload a CSV/Excel file with **Sand**, **Silt**, and **Clay** percentages (must total ~100%)")

    uploaded_file = st.file_uploader("📤 Upload Soil Texture CSV or Excel", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df.head())

            if not all(col in df.columns for col in ["Sand", "Silt", "Clay"]):
                st.error("⚠️ Columns must include 'Sand', 'Silt', and 'Clay'")
                return

            fig, tax = ternary.figure(scale=100)
            tax.boundary()
            tax.gridlines(multiple=10, color="gray")

            tax.left_axis_label("Clay (%)", fontsize=12)
            tax.right_axis_label("Silt (%)", fontsize=12)
            tax.bottom_axis_label("Sand (%)", fontsize=12)
            tax.ticks(axis='lbr', multiple=10, linewidth=1)

            for i, row in df.iterrows():
                sand, silt, clay = row["Sand"], row["Silt"], row["Clay"]
                tax.scatter([(sand, silt, clay)], marker='o', label=f'Sample {i+1}')

            tax.legend()
            st.pyplot(fig)

            # Downloadable image
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Triangle Plot", data=buf.getvalue(), file_name="soil_texture_triangle.png")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Please upload soil composition data to begin.")
