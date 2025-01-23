import pandas as pd

def get_dataset() -> pd.DataFrame:
    df = pd.read_csv("src/data/transactions.csv", usecols=["SENDER_ACCOUNT_ID", "RECEIVER_ACCOUNT_ID", "TX_AMOUNT"])
    df = df.rename(columns={
        "SENDER_ACCOUNT_ID": "sender",
        "RECEIVER_ACCOUNT_ID": "receiver",
        "TX_AMOUNT": "amount"
    })
    return df