# import os
# import requests

# API_URL = os.getenv(
#     "API_URL",
#     "https://fraud-detection-api-dzc8.onrender.com"
# )

# def predict_transaction(payload):

#     response = requests.post(
#         f"{API_URL}/fraud/predict",
#         json=payload,
#         timeout=60
#     )

#     response.raise_for_status()

#     return response.json()

# def predict_batch(payload):
#     url = f"{API_URL}/fraud/predict"
#     response = requests.post(url, json=payload, timeout=120)
#     response.raise_for_status()
#     return response.json()

import os
import requests

API_URL = os.getenv(
    "API_URL",
    "https://fraud-detection-api-dzc8.onrender.com"
)

PREDICT_ENDPOINT = f"{API_URL}/fraud/predict"

print("DEBUG API_URL:", API_URL)
print("DEBUG ENDPOINT:", PREDICT_ENDPOINT)
def predict_transaction(payload):
    response = requests.post(
        PREDICT_ENDPOINT,
        json=payload,
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def predict_batch(payload):
        
    response = requests.post(
        PREDICT_ENDPOINT,
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()