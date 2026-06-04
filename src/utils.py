import pandas as pd
import joblib
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_data.csv")

@st.cache_resource
def load_model_files():

    model = joblib.load("models/model.pkl")

    feature_columns = joblib.load(
        "models/feature_columns.pkl"
    )

    return model, feature_columns