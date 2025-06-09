import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import random

def general_data_tools():
    st.subheader("📊 General Data Tools")

    input_method = st.radio("Choose Data Input Method:", ["📤 Upload CSV/Excel", "✍️ Manual Entry"], key="general_input_method")

    # Default manual table
    default_df = pd.DataFrame({
        "Item": ["Sample A", "Sample B", "Sample C"],
        "Value": [0, 0, 0]
    })

    # Manual Input
    if input_method == "✍️ Manual Entry":
        if "general_df" not in st.session_state:
            st.session_state.general_df = default_df.copy()
            st.session_state.general_key = f"gen_{random.randint(1000,9999)}"

        # Clear All Button
        if st.button("🧹 Clear All"):
            st.session_state.general_df = default_df.copy()
            st.session_state.general_key = f"gen_{random.randint(1000,9999)}"
            st.rerun()

        edited_df = st.data_editor(
            st.session_state.general_df,
            use_container_width=True,
            num_rows="dynamic",
            key=st.session_state.general_key
        )

        if st.button("✅ Apply Data"):
            st.session_state.general_df = edited_df.copy()
            st.success("✅ Data Applied")

        df = st.session_state.general_df.copy()

    # File Upload
    else:
        file = st.file_uploader("📤 Upload CSV or Excel", type=["csv", "xlsx"], key="general_upload")

        if file:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                st.write("📄 Uploaded Data", df)

                if st.button("🧹 Clear Uploaded File"):
                    del st.session_state["general_upload"]
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
                return
        else:
            st.info("Upload a file to proceed.")
            return

    # Data Summary
    st.markdown("### 📈 Data Summary")
    st.write(df.describe(include='all').fillna("-"))

    # Column Selection for Plot
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if numeric_cols:
        st.markdown("### 📊 Quick Chart")
        col_to_plot = st.selectbox("Select Column to Plot", numeric_cols)

        fig, ax = plt.subplots(figsize=(6, 4))
        df[col_to_plot].plot(kind="bar", ax=ax, color="cornflowerblue")
        ax.set_title(f"{col_to_plot} Chart")
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download Chart as PNG", buf.getvalue(), file_name="chart.png")

    # Download table
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button("📄 Download Table as CSV", csv_buf.getvalue(), file_name="table.csv")
