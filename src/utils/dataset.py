import pandas as pd

def get_network_analysis_dataset(sample: int=100000) -> pd.DataFrame:
    df = pd.read_csv("src/data/network_analysis_data.csv")
    return df.head(sample)