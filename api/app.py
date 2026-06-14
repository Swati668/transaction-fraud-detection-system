from datetime import datetime, timezone
import logging
import os

import pandas as pd
from flask import Flask, request, jsonify

from fraud.fraud_model import Fraud

# Logging Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Initializing Pipeline

MODEL_VERSION = "v1"

pipeline = Fraud()


# Initializing Flask App

app = Flask(__name__)


# Required Input Columns

REQUIRED_COLUMNS = [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest"
]

# Root Endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
  "project": "Transaction Fraud Detection System",
  "status": "running",
  "model": "XGBoost",
  "version": "v1",
  "health_endpoint": "/health",
  "prediction_endpoint": "/fraud/predict"
})

# Health Check Endpoint

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "model_version": MODEL_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


# Fraud Prediction Endpoint

@app.route("/fraud/predict", methods=["POST"])
def fraud_predict():

    try:

        payload = request.get_json()

        if not payload:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        # Single record
        if isinstance(payload, dict):
            df = pd.DataFrame([payload])

        # Batch records
        elif isinstance(payload, list):
            df = pd.DataFrame(payload)

        else:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON format"
            }), 400

        # Validate columns
        missing_columns = [
            col for col in REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_columns:

            return jsonify({
                "status": "error",
                "message": "Missing required columns",
                "missing_columns": missing_columns
            }), 400

        logging.info(
            f"Received {len(df)} transaction(s)"
        )

        # Run prediction pipeline
        results_df = pipeline.predict(df)

        # Build response
        results = []

        for _, row in results_df.iterrows():

            results.append({
                "prediction": int(row["prediction"]),
                "prediction_label": (
                    "fraud"
                    if row["prediction"] == 1
                    else "legitimate"
                ),
                "fraud_probability": round(
                    float(row["fraud_probability"]),
                    4
                ),
                "risk_level": row["risk_level"]
            })

        logging.info(
            "Prediction completed successfully"
        )

        return jsonify({
            "status": "success",
            "model_version": MODEL_VERSION,
            "records_processed": len(results),
            "prediction_timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "risk_calculation": "percentile_based",
            "results": results
        })

    except Exception as e:

        logging.exception(
            "Prediction failed"
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



# Run Application

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5001)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )