from pathlib import Path
import streamlit as st


# Page Configuration

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide"
)


# Image Path

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = (
    BASE_DIR
    / "reports"
    / "figures"
    / "feature_engineering_pipeline.png"
)


#  Description Section

st.title("🛡️ Transaction Fraud Detection System")

st.markdown("""
### Real-Time Financial Fraud Detection using Machine Learning

This project demonstrates an end-to-end production-style fraud detection system built using:

- XGBoost Classifier
- Flask REST API
- Docker Containerization
- Streamlit Dashboard
- Feature Engineering Pipeline

The system predicts whether a transaction is fraudulent or legitimate in real time.
""")

st.divider()


# Project Overview

st.subheader("Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Model", "XGBoost")

with col2:
    st.metric("Backend", "Flask API")

with col3:
    st.metric("Frontend", "Streamlit")

with col4:
    st.metric("Deployment", "Docker")

st.divider()


# System Architecture

st.subheader("System Architecture")

st.code("""
User
  ↓
Streamlit Dashboard
  ↓
Flask REST API
  ↓
Feature Engineering Pipeline
  ↓
XGBoost Model
  ↓
Fraud Prediction
""")

st.divider()


# Feature Engineering Pipeline

st.subheader("Feature Engineering Pipeline")

if image_path.exists():
    st.image(
        str(image_path),
        use_container_width=True
    )
else:
    st.warning(
        f"Image not found at:\n{image_path}"
    )

st.divider()



# Feature Engineering

st.subheader("Feature Engineering")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
#### Raw Transaction Features

- step
- type
- amount
- oldbalanceOrg
- newbalanceOrig
- oldbalanceDest
- newbalanceDest
""")

with col2:

    st.markdown("""
#### Engineered Features

- step_days
- step_weeks
- diff_new_old_balance
- diff_new_old_dest
""")

st.caption(
    "Additional features were engineered to better capture time-based patterns and variations in transaction behavior."
)

st.divider()


# Model Performance

st.divider()

st.subheader("Model Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "ROC-AUC",
        "0.9998"
    )

with col2:
    st.metric(
        "PR-AUC",
        "0.9326"
    )

with col3:
    st.metric(
        "Balanced Accuracy",
        "0.93"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Precision",
        "0.892"
    )

with col5:
    st.metric(
        "Recall",
        "0.860"
    )

with col6:
    st.metric(
        "F1 Score",
        "0.876"
    )

st.caption(
    "Model performance was evaluated using a separate held-out test dataset to ensure unbiased assessment."
)

#Key Capabilities

st.subheader("Key Capabilities")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    - Real-Time Fraud Prediction

    - Single Transaction Scoring

    - Batch CSV Processing

    - Risk Level Assessment
    """)

with col2:

    st.markdown("""
    - REST API Inference

    - Interactive Analytics

    - Downloadable Results

    - Dockerized Deployment
    """)

st.divider()


# Footer

st.caption(
    "Fraud detection platform built with XGBoost, Flask, Docker, and Streamlit."
)


