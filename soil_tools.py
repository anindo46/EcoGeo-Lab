import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import io

# Texture classification function (approximate)
def predict_soil_texture(sand, silt, clay):
    if clay > 40:
        return "Clay"
    elif clay >= 27 and silt >= 28 and silt < 40:
        return "Clay Loam"
    elif clay >= 20 and clay < 27 and silt > 28:
        return "Loam"
    elif sand >= 70 and silt < 30 and clay < 15:
        return "Sandy"
    elif silt >= 80 and clay < 12:
        return "Silt"
    elif silt >= 50 and clay >= 12 and clay < 27:
        return "Silty Loam"
    else:
        return "Loam"

def soil_texture_triangle():
    st.subheader("🧱 Soil Texture Triangle (with Prediction + Export)")

    option = st.radio("Select Input Method:", ["📤 Upload CSV/Excel", "✍️ Manual Entry"])

    if option == "📤 Upload CSV/Excel":
        uploaded_file = st.file_uploader("Upload CSV or Excel with columns: Sand, Silt, Clay", type=['csv', 'xlsx'])

        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.write("### 📄 Uploaded Data", df)

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
                return
        else:
            st.info("Please upload a file to continue.")
            return

    else:
        st.markdown("### ✍️ Enter up to 5 samples manually")
        manual_data = {
            "Sample": [f"Sample {i+1}" for i in range(5)],
            "Sand": [0]*5,
            "Silt": [0]*5,
            "Clay": [0]*5
        }
        df = pd.DataFrame(manual_data)
        df = st.data_editor(df, use_container_width=True, num_rows="fixed")
        df.dropna(inplace=True)

    # Validation
    if not all(col in df.columns for col in ["Sand", "Silt", "Clay"]):
        st.error("⚠️ Columns must include Sand, Silt, and Clay")
        return

    try:
        # Normalize
        df_total = df[["Sand", "Silt", "Clay"]].sum(axis=1)
        df["Sand"] = df["Sand"] / df_total * 100
        df["Silt"] = df["Silt"] / df_total * 100
        df["Clay"] = df["Clay"] / df_total * 100

        # Add prediction
        df["Texture"] = df.apply(lambda row: predict_soil_texture(row["Sand"], row["Silt"], row["Clay"]), axis=1)

        st.write("### 🧪 Analyzed Data with Predicted Texture")
        st.dataframe(df)

        # Plot
        fig = px.scatter_ternary(df,
                                 a="Clay", b="Silt", c="Sand",
                                 color="Texture",
                                 symbol="Texture",
                                 hover_name=df["Sample"] if "Sample" in df.columns else df.index.astype(str),
                                 size_max=10,
                                 title="Soil Texture Triangle (with Prediction)")
        st.plotly_chart(fig, use_container_width=True)

        # PNG Export
        buffer = io.BytesIO()
        pio.write_image(fig, buffer, format='png', width=800, height=600, engine="kaleido")
        st.download_button("📥 Download Triangle Plot as PNG", buffer.getvalue(), file_name="soil_texture_triangle.png")

        # CSV Export
        st.download_button("📥 Download Table as CSV", df.to_csv(index=False).encode('utf-8'), file_name="soil_texture_data.csv")

    except Exception as e:
        st.error(f"⚠️ Processing Error: {e}")
