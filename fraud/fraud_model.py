# from pathlib import Path

# import joblib
# import inflection
# import pandas as pd


# class Fraud:

#     def __init__(self):

#         self.base_dir = Path(__file__).resolve().parent.parent
#         self.model = joblib.load(self.base_dir / "artifacts" 
#                                  / "xgboost_fraud_detector.joblib")

#         print("Model loaded successfully")

#     def data_cleaning(self, df):

#         df = df.copy()

#         df.columns = [inflection.underscore(col) for col in df.columns]
#         return df

#     def feature_engineering(self, df):

#         df["diff_new_old_balance"] = (df["newbalance_orig"] 
#                                       - df["oldbalance_org"])

#         df["diff_new_old_dest"] = (df["newbalance_dest"] 
#                                    - df["oldbalance_dest"]
#         )
#         return df

#     def get_risk_level(self, probability):

#         if probability < 0.30:
#             return "Low"

#         elif probability < 0.70:
#             return "Medium"

#         return "High"

#     def predict(self, df):

#         # Cleaning
#         df1 = self.data_cleaning(df)

#         # Feature Engineering
#         df2 = self.feature_engineering(df1)

#         predictions = self.model.predict(df2)

#         probabilities = self.model.predict_proba(df2)[:, 1]

#         result = df.copy()

#         result["prediction"] = predictions

#         result["fraud_probability"] = probabilities

#         result["risk_level"] = [self.get_risk_level(prob) 
#                                 for prob in probabilities
#         ]

#         return result


from pathlib import Path
import joblib
import inflection
import pandas as pd
import numpy as np


class Fraud:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent
        self.model = joblib.load(
            self.base_dir / "artifacts" / "xgboost_fraud_detector.joblib"
        )

        print("Model loaded successfully")

    
    # DATA CLEANING
    
    def data_cleaning(self, df):

        df = df.copy()
        df.columns = [inflection.underscore(col) for col in df.columns]

        return df

    
    # FEATURE ENGINEERING
    
    def feature_engineering(self, df):

        df = df.copy()

        df["diff_new_old_balance"] = (
            df["newbalance_orig"] - df["oldbalance_org"]
        )

        df["diff_new_old_dest"] = (
            df["newbalance_dest"] - df["oldbalance_dest"]
        )

        # Safety: replace inf / NaN
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)

        return df

    
    # RISK SCORING 
    
    def get_risk_level(self, probability, p90=None, p99=None):

        # Default fallback if percentiles not provided
        if p90 is None:
            p90 = 0.01
        if p99 is None:
            p99 = 0.05

        if probability < p90:
            return "Low"
        elif probability < p99:
            return "Medium"
        else:
            return "High"

    
    # MAIN PREDICTION PIPELINE
    
    def predict(self, df):

        # 1. Clean
        df_clean = self.data_cleaning(df)

        # 2. Feature engineering
        df_feat = self.feature_engineering(df_clean)

        # 3. Prediction
        predictions = self.model.predict(df_feat)
        probabilities = self.model.predict_proba(df_feat)[:, 1]

        # 4. Build result
        result = df.copy()
        result["prediction"] = predictions
        result["fraud_probability"] = probabilities

        
        # 5. Dynamic risk thresholds
        
        p90 = np.percentile(probabilities, 90)
        p99 = np.percentile(probabilities, 99)

        result["risk_level"] = [
            self.get_risk_level(prob, p90, p99)
            for prob in probabilities
        ]

        return result