import streamlit as st
import pandas as pd
import requests

from utils.api_client import API_URL

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Fraud Analytics Dashboard")

st.markdown("""
Analyze transaction risk patterns and fraud predictions.

Upload a transaction dataset and generate interactive fraud insights.
""")

st.divider()


# Upload Dataset

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
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

    st.subheader("Dataset Preview")

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
            f"Missing required columns: {missing_cols}"
        )
        st.stop()

    if st.button(
        "Generate Analytics",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Running predictions..."
            ):

                response = requests.post(
                    f"{API_URL}/fraud/predict",
                    json=df.to_dict(
                        orient="records"
                    ),
                    timeout=120
                )

                response.raise_for_status()

                api_response = response.json()

            results_df = pd.DataFrame(
                api_response["results"]
            )

            analytics_df = pd.concat(
                [
                    df.reset_index(drop=True),
                    results_df.reset_index(drop=True)
                ],
                axis=1
            )

            st.success(
                "Analytics generated successfully."
            )

            st.divider()

            
            # KPIs
            
            total_transactions = len(
                analytics_df
            )

            fraud_count = (
                analytics_df["prediction"] == 1
            ).sum()

            legitimate_count = (
                analytics_df["prediction"] == 0
            ).sum()

            fraud_rate = round(
                fraud_count
                / total_transactions
                * 100,
                2
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Transactions",
                    total_transactions
                )

            with col2:
                st.metric(
                    "Frauds",
                    fraud_count
                )

            with col3:
                st.metric(
                    "Legitimate",
                    legitimate_count
                )

            with col4:
                st.metric(
                    "Fraud Rate",
                    f"{fraud_rate}%"
                )

            st.divider()

            
            # Risk Level Distribution
            
            st.subheader(
                "Risk Level Distribution"
            )

            risk_counts = (
                analytics_df["risk_level"]
                .value_counts()
            )

            st.bar_chart(
                risk_counts
            )

            
            # Fraud vs Legitimate
            
            st.subheader(
                "Fraud vs Legitimate"
            )

            prediction_counts = (
                analytics_df[
                    "prediction_label"
                ]
                .value_counts()
            )

            st.bar_chart(
                prediction_counts
            )

            
            # Transaction Type Distribution
            
            st.subheader(
                "Transaction Types"
            )

            txn_counts = (
                analytics_df["type"]
                .value_counts()
            )

            st.bar_chart(
                txn_counts
            )

            
            # Fraud by Transaction Type
            
            st.subheader(
                "Fraud by Transaction Type"
            )

            fraud_by_type = (
                analytics_df[
                    analytics_df[
                        "prediction"
                    ] == 1
                ]
                .groupby("type")
                .size()
                .sort_values(
                    ascending=False
                )
            )

            if len(fraud_by_type):

                st.bar_chart(
                    fraud_by_type
                )

            else:

                st.info(
                    "No fraudulent transactions detected."
                )

            
            # Fraud Probability Distribution
            
            st.subheader(
                "Fraud Probability Distribution"
            )

            probability_data = (
                analytics_df[
                    "fraud_probability"
                ]
            )

            st.line_chart(
                probability_data
            )

            
            # High Risk Transactions
            
            st.subheader(
                "High Risk Transactions"
            )

            high_risk = analytics_df[
                analytics_df[
                    "risk_level"
                ].str.lower()
                == "high"
            ]

            if len(high_risk):

                st.dataframe(
                    high_risk,
                    use_container_width=True
                )

            else:

                st.success(
                    "No high-risk transactions found."
                )

            st.divider()

            
            # Download Analytics
            
            output_csv = (
                analytics_df
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                label="Download Analytics Dataset",
                data=output_csv,
                file_name="analytics_results.csv",
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
                f"Analytics generation failed: {str(e)}"
            )