import streamlit as st
import pandas as pd
import plotly.express as px

def general_data_tools():
    st.subheader("📊 General Data Tools: Plot & Table Viewer")

    uploaded_file = st.file_uploader("📤 Upload a CSV or Excel file", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("### 📄 Uploaded Table")
            st.dataframe(df)

            st.markdown("### 📈 Create a Custom Plot")
            chart_type = st.selectbox("Select chart type", ["Line", "Bar", "Scatter", "Pie"])

            x_col = st.selectbox("X-Axis", df.columns)
            y_col = st.selectbox("Y-Axis", df.columns)

            if chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, title="Line Plot")
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, title="Bar Chart")
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, title="Scatter Plot")
            elif chart_type == "Pie":
                fig = px.pie(df, names=x_col, values=y_col, title="Pie Chart")

            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Data as CSV", csv, "table_data.csv")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("Upload a file to begin.")
