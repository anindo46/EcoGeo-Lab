import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import random
import ternary  # You must have 'python-ternary' installed

def soil_texture_triangle():
    st.subheader("🧪 Soil Texture Triangle Tool")

    # 📘 Real-Life Use Case Guide
    with st.expander("📘 How to Use (Example: Soil Classification)", expanded=False):
        st.markdown("""
        ### 🌱 Scenario: Field Soil Classification  
        After lab testing a soil sample, you found:
        
        - **Sand:** 30%  
        - **Silt:** 50%  
        - **Clay:** 20%

        #### 🚀 Steps:
        - Manually input values or upload a CSV with Sand/Silt/Clay columns.
        - Click ✅ Apply.
        - View the triangle and predicted texture class (e.g., Loam).
        - Export PNG or result CSV.

        #### 💡 Use For:
        - Agriculture, irrigation, hydrology, soil profiling.
        """)

    input_method = st.radio("Select Input Method", ["📤 Upload CSV/Excel", "✍️ Manual Entry"], key="soil_input_method")

    default_df = pd.DataFrame({
        "Sand": [30],
        "Silt": [50],
        "Clay": [20]
    })

    if input_method == "✍️ Manual Entry":
        if "soil_df" not in st.session_state:
            st.session_state.soil_df = default_df.copy()
            st.session_state.soil_key = f"soil_{random.randint(1000,9999)}"

        if st.button("🧹 Clear All Inputs"):
            st.session_state.soil_df = default_df.copy()
            st.session_state.soil_key = f"soil_{random.randint(1000,9999)}"
            st.rerun()

        edited_df = st.data_editor(
            st.session_state.soil_df,
            use_container_width=True,
            num_rows="dynamic",
            key=st.session_state.soil_key
        )

        if st.button("✅ Apply Data"):
            st.session_state.soil_df = edited_df.copy()
            st.success("✅ Data Applied")

        df = st.session_state.soil_df.copy()

    else:
        uploaded = st.file_uploader("Upload a CSV with Sand, Silt, and Clay columns", type=["csv"])
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.write("📄 Uploaded Data", df)
                if st.button("🧹 Clear Uploaded File"):
                    del st.session_state["soil_input_method"]
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Upload Error: {e}")
                return
        else:
            st.info("Upload your CSV to proceed.")
            return

    try:
        fig, tax = ternary.figure(scale=100)
        fig.set_size_inches(6, 6)

        for index, row in df.iterrows():
            point = (row["Sand"], row["Clay"], row["Silt"])
            tax.plot([point], marker='o', label=f"Sample {index+1}")

        tax.boundary(linewidth=1.5)
        tax.gridlines(color="gray", multiple=10)
        tax.left_axis_label("Clay %", offset=0.14)
        tax.right_axis_label("Silt %", offset=0.14)
        tax.bottom_axis_label("Sand %", offset=0.10)
        tax.ticks(axis='lbr', linewidth=1, multiple=10)

        tax.clear_matplotlib_ticks()
        tax._redraw_labels()
        tax.legend()
        tax.set_title("Soil Texture Triangle")

        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download Triangle as PNG", buf.getvalue(), file_name="soil_texture_triangle.png")

    except Exception as e:
        st.error(f"❌ Error: {e}")
