import streamlit as st

from src.utils import load_data, load_model_files
from src.dashboard import show_dashboard
from src.prediction import show_prediction

st.set_page_config(
    page_title="E-Commerce Return Prediction System",
    layout="wide"
)

df = load_data()
model, feature_columns = load_model_files()

if "page" not in st.session_state:
    st.session_state.page = "Home"

# HOME PAGE
if st.session_state.page == "Home":

    st.markdown(
        "<h1 style='text-align:center;'>E-Commerce Return Prediction System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "An e-commerce analytics platform that helps businesses track sales performance, "
        "understand customer behavior, and assess the likelihood of product returns."
        "</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Open KPI Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

    with col2:
        if st.button("Open Prediction Center", use_container_width=True):
            st.session_state.page = "Prediction"
            st.rerun()

elif st.session_state.page == "Dashboard":

    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    show_dashboard(df)

elif st.session_state.page == "Prediction":

    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    show_prediction(df, model, feature_columns)