import pandas as pd
import pandera.pandas as pa
from pandera import Column, DataFrameSchema, Check
from pandera.errors import SchemaError


class TransactionValidator:
    def __init__(self):
        self.schema = DataFrameSchema({
            "transaction_date": Column(
                object,
                Check(self.is_valid_date),
                nullable=False
            ),
            "sender_customer": Column(
                str,
                nullable=False
            ),
            "receiver_customer": Column(
                str,
                nullable=False
            ),
            "amount": Column(
                float,
                Check.gt(0),
                nullable=False
            ),
        })

    @staticmethod
    def is_valid_date(series: pd.Series) -> pd.Series:
        converted = pd.to_datetime(series, errors="coerce")
        return converted.notna()

    def validate(self, df: pd.DataFrame):
        """
        Validates the dataframe.

        Returns:
            dict:
                {
                    "is_valid": bool,
                    "errors": list[str],
                    "validated_df": pd.DataFrame | None
                }
        """
        errors = []

        try:
            # Pandera validation (with type coercion)
            validated_df = self.schema.validate(df, lazy=True)

        except SchemaError as e:
            # Collect all errors (lazy=True gives multiple)
            failure_cases = e.failure_cases

            for _, row in failure_cases.iterrows():
                column = row.get("column", "unknown")
                check = row.get("check", "validation error")
                value = row.get("failure_case", "")

                errors.append(
                    f"Column '{column}': {check} (value: {value})"
                )

            return {
                "is_valid": False,
                "errors": errors,
                "validated_df": None
            }

        return {
            "is_valid": True,
            "errors": [],
            "validated_df": validated_df
        }