import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

def ai_prediction_tool():
    st.subheader("🤖 AI Prediction – Linear Trend Forecasting")

    st.markdown("""
    Upload a CSV or Excel file with at least two columns:
    - `Year` (or any time unit)
    - `Value` (e.g., NDVI, erosion rate, species count)
    """)

    uploaded_file = st.file_uploader("📤 Upload Time-Series Data", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Data", df.head())

            x_col = st.selectbox("Select Time Column (e.g., Year)", df.columns)
            y_col = st.selectbox("Select Value Column", df.columns)

            X = df[[x_col]].values
            y = df[y_col].values

            # Train model
            model = LinearRegression()
            model.fit(X, y)

            # Predict future values
            future_years = st.slider("Predict up to how many steps into future?", 1, 50, 10)
            last_year = int(df[x_col].max())
            future_X = np.arange(last_year + 1, last_year + 1 + future_years).reshape(-1, 1)
            future_y = model.predict(future_X)

            # Combine old + new
            future_df = pd.DataFrame({x_col: future_X.flatten(), y_col: future_y})
            full_df = pd.concat([df[[x_col, y_col]], future_df], ignore_index=True)

            st.markdown("### 📈 Prediction Chart")
            fig = px.line(full_df, x=x_col, y=y_col, markers=True, title="Trend Forecast")
            st.plotly_chart(fig, use_container_width=True)

            # Export CSV
            out_csv = full_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Full Data with Prediction", out_csv, "forecast_output.csv")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Upload time-series data to generate predictions.")
