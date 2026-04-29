import streamlit as st

st.set_page_config(page_title="Paint R&D Versioning", layout="wide")

st.title("🎨 Paint R&D Versioning App")

st.markdown("""
This application supports paint formulation R&D.

Use the options below or the sidebar to navigate.
""")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ New Formulation"):
        st.switch_page("pages/1_New_Formulation.py")

with col2:
    if st.button("📊 View History"):
        st.switch_page("pages/2_History.py")

with col3:
    if st.button("🔍 Compare Versions"):
        st.switch_page("pages/3_Compare_Versions.py")