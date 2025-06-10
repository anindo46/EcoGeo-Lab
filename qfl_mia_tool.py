import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

# QFL Plot
def qfl_plot(q, f, l):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Define the QFL triangle boundaries
    triangle = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    ax.fill(triangle[:,0], triangle[:,1], 'lightgrey', lw=2, zorder=0)
    ax.plot(triangle[:,0], triangle[:,1], 'black', lw=2)

    # Plotting QFL points
    ax.scatter(q, f, color="blue", label="QFL Data", s=60, zorder=1)

    # Annotating the diagram
    ax.text(0.5, 1.02, 'Quartz', ha='center', va='center', fontweight='bold', fontsize=12)
    ax.text(1.02, 0.5, 'Feldspar', ha='center', va='center', fontweight='bold', fontsize=12)
    ax.text(0, -0.05, 'Lithics', ha='center', va='center', fontweight='bold', fontsize=12)

    # Title
    ax.set_title('QFL Diagram')
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()
    st.pyplot(fig)

# MIA Calculation
def mia_calculation(q, f, l):
    total = q + f + l
    mia = (f + l) / total
    return mia

# Qp/(F+L) Plot
def qp_fl_plot(q, f, l):
    x = q / (f + l)
    y = (f + l) / (q + f + l)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x, y, c='green', s=100, marker='o')

    ax.set_xlabel("Q/(F+L)")
    ax.set_ylabel("(F+L)/(Q+F+L)")

    ax.set_title("Qp/(F+L) Plot")
    plt.show()
    st.pyplot(fig)

# Tool for QFL and MIA
def qfl_and_mia_tool():
    st.title("📊 QFL Diagram and MIA Calculation")

    # Provide instructions and usage example
    st.markdown("""
    ### 📝 **How to Use the QFL & MIA Tool:**
    1. **Manual Input**: Input the percentages of **Quartz (Q)**, **Feldspar (F)**, and **Lithics (L)** directly.
    2. **File Upload**: Alternatively, you can upload a **CSV/Excel file** that contains the columns: `Quartz`, `Feldspar`, and `Lithics`.
    3. The tool will automatically generate:
       - **QFL Diagram**: A triangular plot visualizing the proportions of Quartz, Feldspar, and Lithics.
       - **MIA (Mineralogical Index of Alteration)**: A value representing the degree of weathering based on the proportions of Feldspar and Lithics.
       - **Qp/(F+L) Plot**: A plot correlating weathering with the Q/(F+L) ratio.
    
    ### 🔎 **Real-Life Example**:
    Let's say you have a sediment sample with the following values:
    - Quartz (Q) = 60%
    - Feldspar (F) = 25%
    - Lithics (L) = 15%
    
    Based on this input, the tool will:
    1. Plot a **QFL Diagram** showing the proportion of these minerals.
    2. Calculate the **MIA** as:
    \[
    \text{MIA} = \frac{{F + L}}{{Q + F + L}} = \frac{{25 + 15}}{{60 + 25 + 15}} = \frac{{40}}{{100}} = 0.40
    \]
    The result will be shown as: **MIA = 0.40**.
    3. Generate a **Qp/(F+L) Plot** showing the correlation between weathering and mineral composition.
    
    --- 
    """, unsafe_allow_html=True)

    input_method = st.radio("Select Input Method", ["📤 Upload CSV/Excel", "✍️ Manual Entry"])

    if input_method == "✍️ Manual Entry":
        st.markdown("### ✍️ Enter your Q, F, and L values")
        q = st.number_input("Quartz (%)", min_value=0, max_value=100, value=50)
        f = st.number_input("Feldspar (%)", min_value=0, max_value=100, value=30)
        l = st.number_input("Lithics (%)", min_value=0, max_value=100, value=20)

        # Calculate and plot QFL diagram and MIA
        mia = mia_calculation(q, f, l)
        st.markdown(f"### MIA (Mineralogical Index of Alteration): {mia:.2f}")
        qfl_plot(q, f, l)
        qp_fl_plot(q, f, l)

    elif input_method == "📤 Upload CSV/Excel":
        uploaded_file = st.file_uploader("Upload CSV or Excel file with Q, F, and L data", type=["csv", "xlsx"])

        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.write("### Data Preview", df.head())

                # Assuming the CSV/Excel has Q, F, and L columns
                if "Quartz" in df.columns and "Feldspar" in df.columns and "Lithics" in df.columns:
                    for index, row in df.iterrows():
                        q, f, l = row['Quartz'], row['Feldspar'], row['Lithics']
                        mia = mia_calculation(q, f, l)
                        st.markdown(f"### MIA (Mineralogical Index of Alteration) for Row {index}: {mia:.2f}")
                        qfl_plot(q, f, l)
                        qp_fl_plot(q, f, l)
                else:
                    st.error("Please ensure the CSV has 'Quartz', 'Feldspar', and 'Lithics' columns.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.info("Upload a CSV/Excel file to continue.")

# Main function
qfl_and_mia_tool()
