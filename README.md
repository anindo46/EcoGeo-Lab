# 🌍 EcoGeo Lab

**EcoGeo Lab** is a browser-based smart platform built with Streamlit for students, researchers, and professionals in **Geology, Soil Science, Botany, Coastal Studies**, and **Environmental Monitoring**.  
It offers interactive modules for analysis, visualization, and prediction — all in one unified interface.

> 🎓 **Developed by:** Anindo Paul Sourav  
> Department of Geology & Mining, University of Barishal

---

## 🚀 Features

- Upload or manually enter CSV/Excel data
- Generate professional plots, 3D models, and indices
- Predict environmental trends using AI (experimental)
- Export: PNG, CSV, PDF (where applicable)
- Light/Dark mode toggle
- Modular & scalable Streamlit application

---

## 🧰 Tools & Modules

### 1. 🪨 Grain Size Analysis (Folk & Ward Method)
- Calculates statistical parameters: Mean (Mz), Sorting (σ), Skewness (Sk)
- Cumulative phi-weight grain size curve
- Manual entry or CSV upload

**Use Case:** Sedimentology labs, sediment classification

---

### 2. 🟫 Soil Texture Triangle Tool
- USDA-based classification using sand, silt, and clay
- Ternary diagram visualization with automatic texture prediction
- Supports manual and CSV inputs

**Use Case:** Soil science fieldwork, classification of soil samples

---

### 3. 🌿 Biodiversity Index Calculator
- Computes Shannon Index, Simpson Index, and Evenness (J)
- Bar plot of species counts
- Manual input and CSV upload options

**Use Case:** Biodiversity survey data from forests, wetlands, or coastal zones

---

### 4. 🌊 NDWI Viewer (Normalized Difference Water Index)
- Uses Green and NIR bands to map water bodies
- Visual NDWI map with color scale
- Manual input or satellite band CSVs

**Use Case:** Flood detection, wetland monitoring using Sentinel-2 or custom bands

---

### 5. 📡 3D Visualization Tool
- Plots 3D point clouds for topography, LiDAR, or soil profiles
- Input via CSV or manual 3D coordinates
- Interactive rendering via Plotly

**Use Case:** Soil profile depth visualization, borehole plots, terrain mapping

---

### 6. 🧠 AI Prediction Tool *(Experimental)*
- Forecasts vegetation, rainfall, or trendlines from past data
- Line chart with trend fitting and prediction
- Supports time series CSV input

**Use Case:** NDVI prediction, rainfall modeling from past satellite/weather data

---

## 🖥️ How to Run (Locally)

1. Clone the repo:
```bash
git clone https://github.com/yourusername/eco-geo-lab.git
cd eco-geo-lab
