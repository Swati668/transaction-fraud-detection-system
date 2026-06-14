import streamlit as st
import requests

from utils.api_client import predict_transaction

st.set_page_config(
    page_title="Single Prediction",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Single Transaction Prediction")

st.markdown("""
Enter transaction details below and click **Predict Fraud**.
""")


# Input Form

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        step = st.number_input(
            "Step (Hour)",
            min_value=1,
            value=1
        )

        txn_type = st.selectbox(
            "Transaction Type",
            [
                "TRANSFER",
                "CASH_OUT",
                "PAYMENT",
                "DEBIT",
                "CASH_IN"
            ]
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            value=1000.0
        )

    with col2:

        oldbalanceOrg = st.number_input(
            "Old Balance Origin",
            min_value=0.0,
            value=10000.0
        )

        newbalanceOrig = st.number_input(
            "New Balance Origin",
            min_value=0.0,
            value=9000.0
        )

        oldbalanceDest = st.number_input(
            "Old Balance Destination",
            min_value=0.0,
            value=0.0
        )

        newbalanceDest = st.number_input(
            "New Balance Destination",
            min_value=0.0,
            value=1000.0
        )

    submitted = st.form_submit_button(
        "Predict Fraud",
        use_container_width=True
    )


# Prediction

if submitted:

    if amount <= 0:

        st.error(
            "Amount must be greater than zero."
        )

        st.stop()

    payload = {
        "step": int(step),
        "type": txn_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }

    try:

        with st.spinner(
            "Analyzing transaction..."
        ):

            api_response = predict_transaction(
                payload
            )

        result = api_response["results"][0]

        prediction = result["prediction"]

        probability = result[
            "fraud_probability"
        ]

        risk_level = result[
            "risk_level"
        ]

        prediction_label = result[
            "prediction_label"
        ]

        st.divider()

        
        
        if prediction == 1:

            st.error("""
            Potentially Fraudulent Transaction

            Review this transaction before approval.
            """)

        else:

            st.success("""
            Legitimate Transaction

            No significant fraud indicators detected.
            """)

        
        # Metrics
        
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Prediction",
                prediction_label.title()
            )

        with col2:

            st.metric(
                "Fraud Probability",
                f"{probability:.2%}"
            )

        with col3:

            st.metric(
                "Risk Level",
                risk_level.upper()
            )

        
        # Metadata
        
        st.subheader(
            "Prediction Metadata"
        )

        st.json({
            "model_version":
                api_response.get(
                    "model_version"
                ),

            "records_processed":
                api_response.get(
                    "records_processed"
                ),

            "prediction_timestamp":
                api_response.get(
                    "prediction_timestamp"
                )
        })

        
        # Raw Response
        
        with st.expander(
            "View Full API Response"
        ):

            st.json(api_response)

    except requests.exceptions.Timeout:

        st.error(
            "API request timed out."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to API."
        )

    except Exception as e:

        st.error(
            f"Prediction Failed: {str(e)}"
        )