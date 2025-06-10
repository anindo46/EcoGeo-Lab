import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.tri import Triangulation

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

def mia_calculation(q, f, l):
    total = q + f + l
    mia = (f + l) / total
    return mia

def qfl_and_mia_tool():
    st.title("QFL Diagram and MIA Calculation")
    
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
                else:
                    st.error("Please ensure the CSV has 'Quartz', 'Feldspar', and 'Lithics' columns.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.info("Upload a CSV/Excel file to continue.")
    
qfl_and_mia_tool()
