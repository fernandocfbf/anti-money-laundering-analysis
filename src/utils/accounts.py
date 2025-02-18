import pandas as pd

def get_account_details(account_details_df: pd.DataFrame, account_id: int) -> dict[str: str]:
    acc_details = account_details_df.query("account_id == @account_id")
    return acc_details.iloc[0].to_dict()

def get_account_transactions_details(transactions_df: pd.DataFrame, account_id: int) -> dict[str: str]:
    amount_sent = round(transactions_df.query("sender == @account_id").amount_paid.sum(), 2)
    amount_received = round(transactions_df.query("receiver == @account_id").amount_paid.sum(), 2)
    transactions_count = transactions_df.shape[0]
    return {"amount_sent": amount_sent, "amount_received": amount_received, "transactions_count": transactions_count}