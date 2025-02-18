import pandas as pd

def get_account_details(account_details_df: pd.DataFrame, account_id: int) -> dict[str: str]:
    acc_details = account_details_df.query("account_id == @account_id")
    return acc_details.iloc[0].to_dict()