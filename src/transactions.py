import pandas as pd
from src.utils.dataset import get_dataset

class Transactions:

    def _apply_transformations(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        relationships_df = transactions_df.groupby(["sender", "receiver"], as_index=False).agg({"amount":  "sum"})
        relationships_df.columns = ['sender','receiver','sum']
        relationships_df = relationships_df.rename(columns={"sum": "value"})
        relationships_df["title"] = relationships_df.apply(lambda df: f"from: {df.sender}\nto: {df.receiver}\namount (BRL): {df.value}", axis=1)
        return relationships_df

    def load_data(self) -> pd.DataFrame:
        transactions_df = get_dataset()
        return self._apply_transformations(transactions_df)
