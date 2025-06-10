import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# Function to calculate MIA
def calculate_mia(q, k, p):
    """Calculate MIA using the formula: MIA = (Q / (Q + (K + P))) * 100"""
    return (q / (q + (k + p))) * 100

# Function to process CSV and perform QFL & MIA calculations
def qfl_and_mia_tool():
    # File Upload
    uploaded_file = st.file_uploader("Upload your CSV with 'Q', 'F', and 'L' values", type=['csv', 'xlsx'], key="upload_file")

    if uploaded_file:
        try:
            # Read the uploaded CSV file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Display the uploaded CSV Data
            st.write("### Data Preview", df.head())

            # Ensure the CSV contains the required columns 'Q', 'F', and 'L'
            if 'Q' not in df.columns or 'F' not in df.columns or 'L' not in df.columns:
                st.error("⚠️ Please ensure the CSV contains 'Q', 'F', and 'L' columns.")
                return

            # Extract necessary columns
            df['Q'] = df['Q'].astype(float)
            df['F'] = df['F'].astype(float)
            df['L'] = df['L'].astype(float)

            # Calculate MIA for each row
            df['MIA'] = calculate_mia(df['Q'], df['F'], df['L'])
            
            # Generate QFL diagram
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(df['Q'], df['F'], label="Q vs F")
            ax.plot(df['F'], df['L'], label="F vs L")
            ax.set_xlabel("Quartz (Q)")
            ax.set_ylabel("Feldspar (F) / Lithics (L)")
            ax.legend(loc="best")
            st.pyplot(fig)

            # Allow the user to download the result
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Result as CSV", csv, file_name="qfl_mia_results.csv")

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    else:
        st.info("Please upload a CSV file containing 'Q', 'F', and 'L' values to proceed.")

