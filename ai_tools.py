import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import random
from sklearn.linear_model import LinearRegression

def ai_prediction_tool():
    st.subheader("🤖 AI Prediction Tool")

    # --- How to Use Guide ---
    with st.expander("📘 How to Use (Example: NDVI Forecast)", expanded=False):
        st.markdown("""
        ### 🧪 Scenario:
        You've recorded **NDVI values** from 2015 to 2023 and want to predict for 2024–2030.

        | Year | NDVI |
        |------|------|
        | 2015 | 0.21  
        | 2016 | 0.23  
        | ...  | ...  
        | 2023 | 0.36  

        #### 🚀 Steps:
        - Choose `Manual Entry` or upload a CSV with Year & Value.
        - Click ✅ Apply.
        - Select how many **future years to predict**.
        - See the **forecast line**, table, and download results!

        #### 💡 Use For:
        - NDVI trends 🌿  
        - Rainfall 🌧️  
        - Erosion Index 🌊  
        - Population, emissions, etc.
        """)

    input_method = st.radio("Select Input Method", ["📤 Upload CSV", "✍️ Manual Entry"], key="ai_input_method")

    default_df = pd.DataFrame({
        "Year": list(range(2015, 2024)),
        "Value": [0.21, 0.23, 0.26, 0.28, 0.31, 0.29, 0.33, 0.35, 0.36]
    })

    if input_method == "✍️ Manual Entry":
        if "ai_df" not in st.session_state:
            st.session_state.ai_df = default_df.copy()
            st.session_state.ai_key = f"ai_{random.randint(1000,9999)}"

        if st.button("🧹 Clear All Inputs"):
            st.session_state.ai_df = default_df.copy()
            st.session_state.ai_key = f"ai_{random.randint(1000,9999)}"
            st.rerun()

        edited_df = st.data_editor(
            st.session_state.ai_df,
            use_container_width=True,
            num_rows="dynamic",
            key=st.session_state.ai_key
        )

        if st.button("✅ Apply Data"):
            st.session_state.ai_df = edited_df.copy()
            st.success("✅ Data Applied")

        df = st.session_state.ai_df.copy()

    else:
        uploaded = st.file_uploader("Upload a CSV with columns: Year, Value", type=["csv"])
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.write("📄 Uploaded Data", df)
                if st.button("🧹 Clear Uploaded File"):
                    del st.session_state["ai_input_method"]
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Upload Error: {e}")
                return
        else:
            st.info("Upload your CSV to proceed.")
            return

    # Prediction Settings
    try:
        df = df.dropna()
        df["Year"] = df["Year"].astype(int)
        df["Value"] = df["Value"].astype(float)

        min_year = df["Year"].max()
        years_to_predict = st.slider("How many future years to predict?", 1, 10, 5)
        future_years = np.array(list(range(min_year + 1, min_year + 1 + years_to_predict))).reshape(-1, 1)

        # Linear Regression
        model = LinearRegression()
        model.fit(df[["Year"]], df["Value"])
        future_preds = model.predict(future_years)

        # Combine
        full_years = pd.concat([df, pd.DataFrame({"Year": future_years.flatten(), "Value": future_preds})], ignore_index=True)

        # Plot
        st.markdown("### 📈 Forecast Plot")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df["Year"], df["Value"], label="Historical", marker='o')
        ax.plot(future_years, future_preds, label="Predicted", linestyle="--", marker='x')
        ax.set_title("Forecast using Linear Regression")
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        st.pyplot(fig)

        # Export Chart
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download Chart as PNG", buf.getvalue(), file_name="ai_forecast.png")

        # Export Table
        st.markdown("### 📋 Full Data Table")
        st.write(full_years)

        csv_buf = io.StringIO()
        full_years.to_csv(csv_buf, index=False)
        st.download_button("📄 Download Data as CSV", csv_buf.getvalue(), file_name="ai_forecast.csv")

    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
