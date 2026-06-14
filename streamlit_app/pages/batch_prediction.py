import streamlit as st
import pandas as pd
import requests

from utils.api_client import predict_batch

st.set_page_config(
    page_title="Batch Prediction",
    page_icon="📁",
    layout="wide"
)

st.title("📁 Batch Fraud Prediction")

st.markdown("""
Upload a CSV file containing transaction records.

The model will score every transaction and return:

- Prediction
- Fraud Probability
- Risk Level
""")


# Sample CSV Download

# sample_df = pd.DataFrame({
#     "step": [1, 2, 3, 4, 5],
#     "type": ["TRANSFER", "CASH_OUT", "PAYMENT", "CASH_IN", "TRANSFER"],
#     "amount": [10000, 5000, 2500, 15000, 75000],
#     "oldbalanceOrg": [20000, 10000, 5000, 0, 80000],
#     "newbalanceOrig": [10000, 5000, 2500, 15000, 5000],
#     "oldbalanceDest": [0, 0, 1000, 10000, 0],
#     "newbalanceDest": [10000, 5000, 3500, 25000, 75000]
# })

sample_df = pd.read_csv("data/sample_transactions.csv")

csv = sample_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Sample CSV",
    data=csv,
    file_name="sample_transactions.csv",
    mime="text/csv"
)

st.divider()


# Upload CSV

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

required_columns = [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest"
]

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    if df.empty:
        st.warning("Uploaded CSV is empty")
        st.stop()

    st.subheader("Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    missing_cols = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_cols:

        st.error(
            f"Missing columns: {missing_cols}"
        )
        st.stop()

    st.info(
        f"Total Records: {len(df)}"
    )

    if st.button(
        "Run Batch Prediction",
        use_container_width=True
    ):

        try:

            records = df.to_dict(
                orient="records"
            )

            with st.spinner(
                "Scoring transactions..."
            ):

                api_response = predict_batch(records)

                if "results" not in api_response:
                    st.error("Invalid API response format")
                    st.json(api_response)
                    st.stop()

            result_df = pd.DataFrame(
                api_response["results"]
            )

            final_df = pd.concat(
                [
                    df.reset_index(drop=True),
                    result_df.reset_index(drop=True)
                ],
                axis=1
            )

            st.success(
                "Batch prediction completed successfully."
            )

            
            # Metrics
            
            fraud_count = (
                final_df["prediction"] == 1
            ).sum()

            legit_count = (
                final_df["prediction"] == 0
            ).sum()

            avg_probability = round(
                final_df["fraud_probability"].mean(),
                4
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Fraud Transactions",
                    fraud_count
                )

            with col2:
                st.metric(
                    "Legitimate Transactions",
                    legit_count
                )

            with col3:
                st.metric(
                    "Average Fraud Probability",
                    avg_probability
                )

            
            # Risk Level Distribution
            
            st.subheader(
                "Risk Level Distribution"
            )

            risk_counts = (
                final_df["risk_level"]
                .value_counts()
            )

            st.bar_chart(risk_counts)

            
            # Prediction Results
            
            st.subheader(
                "Prediction Results"
            )

            st.dataframe(
                final_df,
                use_container_width=True
            )

            
            # API Metadata
            
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

            
            # Download Results
            
            output_csv = (
                final_df
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                label="Download Predictions",
                data=output_csv,
                file_name="fraud_predictions.csv",
                mime="text/csv"
            )

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
                f"Prediction failed: {str(e)}"
            )