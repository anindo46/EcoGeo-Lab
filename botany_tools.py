import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import random

def biodiversity_index_calculator():
    st.subheader("🌿 Biodiversity Index Calculator")

    # 📘 Real-Life Use Case Guide
    with st.expander("📘 How to Use (Example: Forest Species Diversity)", expanded=False):
        st.markdown("""
        ### 🌿 Scenario: Forest Species Count  
        You recorded species counts in a quadrat study:

        | Species | Count |
        |---------|-------|
        | Teak    | 10  
        | Sal     | 15  
        | Mahogany| 5  
        | Bamboo  | 20  

        #### 🚀 Steps:
        - Use `✍️ Manual Entry` or upload a CSV.
        - Click ✅ Apply.
        - Tool calculates Shannon Index, Simpson Index, Evenness.
        - See bar chart & export PNG/CSV.

        #### 💡 Use For:
        - Vegetation studies, habitat richness, ecological research.
        """)

    input_method = st.radio("Select Input Method:", ["📤 Upload CSV", "✍️ Manual Entry"], key="biodiv_input_method")

    default_df = pd.DataFrame({
        "Species": [f"Species {i+1}" for i in range(5)],
        "Count": [0]*5
    })

    # Manual Entry Method
    if input_method == "✍️ Manual Entry":
        if "biodiv_data" not in st.session_state:
            st.session_state.biodiv_data = default_df.copy()
            st.session_state.biodiv_key = f"biodiv_{random.randint(1000,9999)}"

        if st.button("🧹 Clear All Inputs"):
            st.session_state.biodiv_data = default_df.copy()
            st.session_state.biodiv_key = f"biodiv_{random.randint(1000,9999)}"
            st.rerun()

        edited_df = st.data_editor(
            st.session_state.biodiv_data,
            use_container_width=True,
            num_rows="dynamic",
            key=st.session_state.biodiv_key
        )

        if st.button("✅ Apply Data"):
            st.session_state.biodiv_data = edited_df.copy()
            st.success("✅ Data Applied")

        df = st.session_state.biodiv_data.copy()

    # File Upload Method
    else:
        uploaded = st.file_uploader("Upload CSV with 'Species' and 'Count'", type=["csv"], key="biodiv_upload")

        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.write("📄 Uploaded Data", df)

                if st.button("🧹 Clear Uploaded File"):
                    del st.session_state["biodiv_upload"]
                    st.rerun()

            except Exception as e:
                st.error(f"❌ File Error: {e}")
                return
        else:
            st.info("Upload a valid CSV to proceed.")
            return

    # --- Calculation Section ---
    try:
        df.dropna(inplace=True)
        df["Count"] = df["Count"].astype(int)

        N = df["Count"].sum()
        if N == 0:
            st.warning("Total count is zero. Please enter valid species counts.")
            return

        df["pi"] = df["Count"] / N
        df["pi_ln_pi"] = df["pi"] * np.log(df["pi"])
        df["pi_sq"] = df["pi"] ** 2

        H = -df["pi_ln_pi"].sum()
        D = 1 - df["pi_sq"].sum()
        S = len(df)
        J = H / np.log(S) if S > 1 else 0

        st.markdown(f"""
        ### 📊 Biodiversity Metrics
        - **Shannon Index (H’)**: `{H:.3f}`
        - **Simpson Index (1 - D)**: `{D:.3f}`
        - **Evenness (J)**: `{J:.3f}`
        """)

        # Plotting Chart
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(df["Species"], df["Count"], color="forestgreen")
        ax.set_title("Species Abundance")
        ax.set_xlabel("Species")
        ax.set_ylabel("Count")
        plt.xticks(rotation=30)
        st.pyplot(fig)

        # PNG Export
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download Chart as PNG", buf.getvalue(), file_name="biodiversity_chart.png")

        # CSV Export
        csv_buf = io.StringIO()
        df[["Species", "Count"]].to_csv(csv_buf, index=False)
        st.download_button("📄 Download Table as CSV", csv_buf.getvalue(), file_name="biodiversity_data.csv")

    except Exception as e:
        st.error(f"⚠️ Calculation error: {e}")
