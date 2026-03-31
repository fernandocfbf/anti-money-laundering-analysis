import pandas as pd
import re

class TransactionFeatures:
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        transaction_behavior_df = (
            X.groupby(by=["customer_id", "direction"], as_index=False)
                .agg(
                    transaction_count=("amount", "count"),
                    total_amount=("amount", "sum"),
                    median_amount=("amount", "median"),
                    std_amount=("amount", "std"),
                    max_amount=("amount", "max"),
                )
                .reset_index(drop=True)
                .pivot(index="customer_id", columns="direction")
                .fillna(0)
        )
        transaction_behavior_df.columns = [
            f"{metric}_{direction}"
            for metric, direction in transaction_behavior_df.columns
        ]
        transaction_behavior_df = transaction_behavior_df.reset_index()
        return transaction_behavior_df
    
class TimeFeatures:    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        time_df = X.copy()
        time_df["days_from_ref"] = (time_df["max_transaction_date"] - time_df["transaction_date"]).dt.days
        bins = [-1, 7, 30, 90]
        expected_windows = ["7d", "30d", "90d"]
        expected_directions = X["direction"].unique()
        expected_metrics = ["total_amount", "transaction_count"]
        multi_cols = pd.MultiIndex.from_product(
            [expected_metrics, expected_directions, expected_windows]
        )

        time_df["window"] = pd.cut(
            time_df["days_from_ref"],
            bins=bins,
            labels=expected_windows
        )
        time_df["window"] = time_df["window"].astype(str)
        
        time_behavior_df = (
            time_df
            .groupby(["customer_id", "direction", "window"], as_index=False)
            .agg(
                total_amount=("amount", "sum"),
                transaction_count=("transaction_count", "sum")
            )
            .pivot_table(
                index="customer_id",
                columns=["direction", "window"],
                values=["total_amount", "transaction_count"],
                fill_value=0
            )
        )
        time_behavior_df = time_behavior_df.reindex(columns=multi_cols, fill_value=0)
        time_behavior_df.columns = [f"{metric}_{direction}_{window}" for metric, direction, window in time_behavior_df.columns]
        time_behavior_df = time_behavior_df.reset_index()
        return time_behavior_df

class RatioFeatures:
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        ratio_df = X.copy()
        ratio_df["sent_received_ratio"] = ratio_df["total_amount_sent"]/(ratio_df["total_amount_received"] + 1)
        ratio_df["transaction_direction_ratio"] = ratio_df["transaction_count_sent"]/(ratio_df["transaction_count_received"] + 1)
        
        windows = {
            col.split("_")[-1]
            for col in ratio_df.columns
            if col.startswith(("total_amount_", "transaction_count_")) and col.count("_") >= 3
        }
        metrics = ["total_amount", "transaction_count"]
        for metric in metrics:
            for time_window in windows:
                ratio_df[f"{metric}_{time_window}_ratio"] = ratio_df[f"{metric}_sent_{time_window}"] / (ratio_df[f"{metric}_received_{time_window}"] + 1e-6)

        #ratio_df["total_amount_7d_ratio"] = ratio_df["total_amount_sent_7d"] / (ratio_df["total_amount_received_7d"] + 1e-6)
        #ratio_df["transaction_count_30d_ratio"] = ratio_df["transaction_count_sent_30d"] / (ratio_df["transaction_count_received_30d"] + 1e-6)
        #ratio_df["transaction_count_7d_ratio"] = ratio_df["transaction_count_sent_7d"] / (ratio_df["transaction_count_received_7d"] + 1e-6)
        return ratio_df
    
class FeatureGenerator:
    def __init__(self):
        self.transaction_features = TransactionFeatures()
        self.time_features = TimeFeatures()
        self.ratio_features = RatioFeatures()
    
    def _simplified_transaction_table(self, X:pd.DataFrame) -> pd.DataFrame:
        sent_df = X.assign(
            customer_id=X["sender_customer"],
            direction="sent",
            amount=X["amount"],
            transaction_count=1
        )[["customer_id", "transaction_date", "direction", "amount", "transaction_count"]]

        received_df = X.assign(
            customer_id=X["receiver_customer"],
            direction="received",
            amount=X["amount"],
            transaction_count=1
        )[["customer_id", "transaction_date", "direction", "amount", "transaction_count"]]
        simplified_df = pd.concat([sent_df, received_df], ignore_index=True)
        simplified_df["transaction_date"] = pd.to_datetime(simplified_df["transaction_date"])
        max_transaction_date_df = (
            simplified_df
                .groupby(by="customer_id", as_index=False)
                .agg(
                    max_transaction_date=("transaction_date", "max")
                )
        )
        return simplified_df.merge(max_transaction_date_df, on="customer_id", how="left", validate="many_to_one")

    def fit(self, X, y=None):
        return self

    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        simplified_x = self._simplified_transaction_table(X)
        
        transactions_features_df = self.transaction_features.transform(simplified_x)
        time_features_df = self.time_features.transform(simplified_x)
        features_df = transactions_features_df.merge(time_features_df, on="customer_id", how="left", validate="1:1")
        
        ratio_features_df = self.ratio_features.transform(features_df)

        return ratio_features_df