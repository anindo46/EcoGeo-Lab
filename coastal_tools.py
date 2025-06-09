import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import random

def coastal_ndwi_viewer():
    st.subheader("🌊 NDWI Viewer (Normalized Difference Water Index)")

    input_method = st.radio("Select Input Method:", ["📤 Upload Green & NIR CSV", "✍️ Manual Entry"], key="ndwi_input_method")

    default_green = pd.DataFrame(np.random.randint(50, 100, size=(5, 5)), columns=[f"C{i}" for i in range(1, 6)])
    default_nir = pd.DataFrame(np.random.randint(50, 100, size=(5, 5)), columns=[f"C{i}" for i in range(1, 6)])

    if input_method == "✍️ Manual Entry":
        if "ndwi_green" not in st.session_state:
            st.session_state.ndwi_green = default_green.copy()
            st.session_state.ndwi_nir = default_nir.copy()
            st.session_state.ndwi_key = f"ndwi_{random.randint(1000,9999)}"

        # Clear All
        if st.button("🧹 Clear All Inputs"):
            st.session_state.ndwi_green = default_green.copy()
            st.session_state.ndwi_nir = default_nir.copy()
            st.session_state.ndwi_key = f"ndwi_{random.randint(1000,9999)}"
            st.rerun()

        st.markdown("#### ✅ Enter Green Band Values")
        green_df = st.data_editor(
            st.session_state.ndwi_green,
            use_container_width=True,
            key=f"{st.session_state.ndwi_key}_green"
        )

        st.markdown("#### ✅ Enter NIR Band Values")
        nir_df = st.data_editor(
            st.session_state.ndwi_nir,
            use_container_width=True,
            key=f"{st.session_state.ndwi_key}_nir"
        )

        if st.button("✅ Apply NDWI Calculation"):
            st.session_state.ndwi_green = green_df.copy()
            st.session_state.ndwi_nir = nir_df.copy()
            st.success("✅ Data applied")

        green = st.session_state.ndwi_green.to_numpy().astype(float)
        nir = st.session_state.ndwi_nir.to_numpy().astype(float)

    else:
        green_file = st.file_uploader("📤 Upload Green Band CSV", type=["csv"], key="green_csv")
        nir_file = st.file_uploader("📤 Upload NIR Band CSV", type=["csv"], key="nir_csv")

        if not green_file or not nir_file:
            st.warning("Upload both Green and NIR band CSVs to continue.")
            return

        try:
            green = pd.read_csv(green_file).to_numpy().astype(float)
            nir = pd.read_csv(nir_file).to_numpy().astype(float)
        except Exception as e:
            st.error(f"❌ Error loading files: {e}")
            return

    # --- Calculate NDWI ---
    try:
        denominator = (green + nir)
        denominator[denominator == 0] = 0.0001  # avoid division by zero
        ndwi = (green - nir) / denominator

        st.markdown("### 🖼️ NDWI Map Preview")
        fig, ax = plt.subplots(figsize=(6, 5))
        cax = ax.imshow(ndwi, cmap="BrBG", vmin=-1, vmax=1)
        fig.colorbar(cax, ax=ax, label="NDWI Value")
        ax.set_title("NDWI Map")
        st.pyplot(fig)

        # Export PNG
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("📥 Download NDWI Map (PNG)", buf.getvalue(), file_name="ndwi_map.png")

        # Export CSV
        ndwi_df = pd.DataFrame(ndwi.round(3))
        csv_buf = io.StringIO()
        ndwi_df.to_csv(csv_buf, index=False)
        st.download_button("📄 Download NDWI Values (CSV)", csv_buf.getvalue(), file_name="ndwi_values.csv")

    except Exception as e:
        st.error(f"⚠️ NDWI calculation failed: {e}")
