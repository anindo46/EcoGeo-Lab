import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def visual_3d_tool():
    st.subheader("🧱 3D Visualization Tool – Soil / Point Cloud / Surface")

    st.markdown("""
    Upload a CSV or Excel file with:
    - For **Point Cloud**: `X`, `Y`, `Z`
    - For **Soil Profile**: `Depth`, `Soil Property` (e.g., Texture, pH, Color Index)
    """)

    uploaded_file = st.file_uploader("📤 Upload 3D Data (CSV/XLSX)", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df.head())

            columns = df.columns.tolist()
            viz_type = st.radio("Choose Visualization Type", ["Point Cloud", "Soil Profile"])

            if viz_type == "Point Cloud":
                x = st.selectbox("Select X axis", columns)
                y = st.selectbox("Select Y axis", columns)
                z = st.selectbox("Select Z axis", columns)

                fig = go.Figure(data=[go.Scatter3d(
                    x=df[x], y=df[y], z=df[z],
                    mode='markers',
                    marker=dict(size=4, color=df[z], colorscale='Viridis', opacity=0.8)
                )])

                fig.update_layout(scene=dict(xaxis_title=x, yaxis_title=y, zaxis_title=z),
                                  title="3D Point Cloud Viewer")
                st.plotly_chart(fig, use_container_width=True)

            elif viz_type == "Soil Profile":
                depth = st.selectbox("Select Depth Axis", columns)
                prop = st.selectbox("Select Property to Color By", [col for col in columns if col != depth])

                fig = go.Figure(data=go.Scatter3d(
                    x=[1]*len(df),  # Dummy X for vertical profile
                    y=[1]*len(df),
                    z=df[depth],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=df[prop],
                        colorscale='Earth',
                        showscale=True
                    )
                ))
                fig.update_layout(scene=dict(
                    xaxis_title="Profile",
                    yaxis_title="",
                    zaxis_title=depth
                ), title="3D Soil Profile")

                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Upload a valid file with appropriate columns.")
