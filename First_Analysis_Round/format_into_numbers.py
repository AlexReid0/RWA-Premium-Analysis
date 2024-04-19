import pandas as pd

df = pd.read_csv('merged_dataset_2.csv')

columns_to_modify = ["realt_price_original", "initial_market_cap", "volume_total"]
for column in columns_to_modify:
    df[column] = df[column].replace({'\$': '', ' ': ''}, regex=True)
    df[column] = pd.to_numeric(df[column], errors='coerce')

df.to_csv('merged_dataset_3.csv', index=False)

