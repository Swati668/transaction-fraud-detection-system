import pandas as pd
from fraud.fraud_model import Fraud


def test_prediction():

    # Load model
    model = Fraud()

    # Sample transaction
    sample = pd.DataFrame([{
                "step": 1,
                "type": "PAYMENT",
                "amount": 100,
                "oldbalanceOrg": 15000,
                "newbalanceOrig": 5000,
            "oldbalanceDest": 0,
                "newbalanceDest": 10000
            }])
    sample2 = pd.DataFrame([
    {
        "step": 1,
        "type": "PAYMENT",
        "amount": 100,
        "oldbalanceOrg": 15000,
        "newbalanceOrig": 5000,
        "oldbalanceDest": 0,
        "newbalanceDest": 10000
    },
    {
        "step": 1,
        "type": "TRANSFER",
        "amount": 500000,
        "oldbalanceOrg": 500000,
        "newbalanceOrig": 0,
        "oldbalanceDest": 0,
        "newbalanceDest": 500000
    }
])

    # Predict
    result = model.predict(sample)

    # Schema Checks
    
    expected_columns = [
        "prediction",
        "fraud_probability",
        "risk_level"
    ]

    for col in expected_columns:
        assert col in result.columns

    assert len(result) == 1

    # Value Checks
    
    prediction = result["prediction"].iloc[0]
    probability = result["fraud_probability"].iloc[0]
    risk_level = result["risk_level"].iloc[0]

    assert prediction in [0, 1]
    assert 0 <= probability <= 1
    assert risk_level in ["Low", "Medium", "High"]

    print("Prediction test passed")


if __name__ == "__main__":
    test_prediction()