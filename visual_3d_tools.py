import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io
import random

def visual_3d_tool():
    st.subheader("📡 3D Visualization Tool (Point Cloud & Profiles)")

    # 📘 Real-Life Use Case
    with st.expander("📘 How to Use (Example: Soil Profile or Point Cloud)", expanded=False):
        st.markdown("""
        ### 🏞️ Scenario: Visualizing Soil Sample or Lidar Data  
        You collected elevation or depth data (X, Y, Z) from:

        - **Soil pit profiling**
        - **Lidar scans**
        - **Topographic surveys**

        #### 🚀 Steps:
        - Upload a CSV or input manually:
            - Columns = X, Y, Z (e.g., position & elevation/depth)
        - Click ✅ Apply.
        - 3D plot shows point cloud with depth/elevation.
        - Export image or data.

        #### 💡 Use For:
        - 3D terrain models
        - Lidar/lab profile points
        - Borehole/sample visualization
        """)

    input_method = st.radio("Select Input Method", ["📤 Upload CSV", "✍️ Manual Entry"], key="vis3d_input_method")

    default_df = pd.DataFrame({
        "X": [1, 2, 3, 4, 5],
        "Y": [10, 12, 14, 16, 18],
        "Z": [100, 105, 110, 115, 120]
    })

    if input_method == "✍️ Manual Entry":
        if "vis3d_df" not in st.session_state:
            st.session_state.vis3d_df = default_df.copy()
            st.session_state.vis3d_key = f"vis3d_{random.randint(1000,9999)}"

        if st.button("🧹 Clear All Inputs"):
            st.session_state.vis3d_df = default_df.copy()
            st.session_state.vis3d_key = f"vis3d_{random.randint(1000,9999)}"
            st.rerun()

        edited_df = st.data_editor(
            st.session_state.vis3d_df,
            use_container_width=True,
            num_rows="dynamic",
            key=st.session_state.vis3d_key
        )

        if st.button("✅ Apply Data"):
            st.session_state.vis3d_df = edited_df.copy()
            st.success("✅ Data Applied")

        df = st.session_state.vis3d_df.copy()

    else:
        uploaded = st.file_uploader("Upload CSV with 'X', 'Y', 'Z' columns", type=["csv"], key="vis3d_upload")

        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.write("📄 Uploaded Data", df)

                if st.button("🧹 Clear Uploaded File"):
                    del st.session_state["vis3d_upload"]
                    st.rerun()

            except Exception as e:
                st.error(f"❌ File Error: {e}")
                return
        else:
            st.info("Upload a valid CSV to proceed.")
            return

    # --- 3D Plotting ---
    try:
        fig = px.scatter_3d(
            df,
            x='X', y='Y', z='Z',
            color='Z',
            size_max=8,
            opacity=0.8,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(title="3D Point Cloud Visualization", margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig, use_container_width=True)

        # PNG Export
        st.download_button(
            "📥 Download Data as CSV",
            df.to_csv(index=False),
            file_name="3d_point_cloud.csv"
        )

    except Exception as e:
        st.error(f"⚠️ Visualization Error: {e}")
