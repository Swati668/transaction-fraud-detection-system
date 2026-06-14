import pandas as pd
import requests
from pathlib import Path


URL = "http://127.0.0.1:5001/fraud/predict"

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data/raw" / "fraud_0.1origbase.csv")

# Single Transaction Test

def test_single_transaction():

    sample_txn = (df.iloc[5, :-2].to_dict())
    response = requests.post(
        URL,json=sample_txn)
    
    assert response.status_code == 200

    response_json = response.json()

    assert response_json["status"] == "success"

    result = response_json["results"][0]

    assert "prediction" in result
    assert "fraud_probability" in result
    assert "risk_level" in result

    assert result["prediction"] in [0, 1]

    assert (0<= result["fraud_probability"]<= 1)

    assert result["risk_level"] in ["Low","Medium","High"]
    print("Single transaction test passed")



# Batch Transaction Test

def test_batch_transactions():

    sample_batch = (df.iloc[:5, :-2].to_dict(orient="records"))
    response = requests.post(URL,json=sample_batch)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["status"] == "success"

    assert (response_json["records_processed"] == 5)
    assert (len(response_json["results"]) == 5)

    print("Batch transaction test passed")



# Missing Column Test

def test_missing_columns():

    bad_payload = {"amount": 1000}

    response = requests.post(URL,json=bad_payload)
    assert response.status_code == 400

    print("Missing column test passed")


if __name__ == "__main__":

    test_single_transaction()
    test_batch_transactions()
    test_missing_columns()

    print("\n All API tests passed")