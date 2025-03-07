import pandas as pd
import numpy as np
import joblib

class MachineLearningModel:
    def __init__(self):
        self._load_model()

    def _load_model(self):
        self.model = joblib.load("xgb_pipeline.pkl")

    def _custom_transformations(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.drop(columns=["sender", "receiver"])
        dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
        dataframe["timestamp"] = dataframe["timestamp"].apply(lambda timestamp_value: timestamp_value.value)
        return dataframe

    def get_account_score(self, transactions_df: pd.DataFrame) -> float:
        X = self._custom_transformations(transactions_df)
        y_proba = self.model.predict_proba(X)[:, 1]
        score = round(y_proba[np.argmax(y_proba)], 4)
        return score
