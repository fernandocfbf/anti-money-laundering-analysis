import pandas as pd

def get_network_analysis_dataset(sample: int=100000) -> pd.DataFrame:
    df = pd.read_csv("src/data/network_analysis_data.csv")
    return df.head(sample)

def get_machine_learning_dataset() -> pd.DataFrame:
    return pd.read_csv("src/data/machine_learning_data.csv")