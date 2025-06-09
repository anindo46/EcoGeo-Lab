import streamlit as st

def footer():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 13px; color: gray;'>
    🌍 <strong>EcoGeo Lab</strong> by <strong>Anindo Paul Sourav</strong><br>
    Geology & Mining, University of Barishal · Powered by Python & Streamlit 💻
    </p>
    """, unsafe_allow_html=True)
