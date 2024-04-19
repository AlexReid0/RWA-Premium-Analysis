import pandas as pd

# Paths to your CSV files
april_2_csv_path = 'April_2.csv'
april_3_csv_path = 'April_3.csv'

# Load the CSV files into DataFrames
april_2_df = pd.read_csv(april_2_csv_path)
april_3_df = pd.read_csv(april_3_csv_path)

april_3_df = april_3_df.drop_duplicates()

# Merge the DataFrames on 'tx_hash', including only the 'fee' and 'value' columns from April_3.csv
merged_df = pd.merge(april_2_df, april_3_df[['tx_hash', 'Fee', 'Value']], on='tx_hash', how='left')

# Save the merged DataFrame to a new CSV file
new_csv_path = 'april_merged.csv'
merged_df.to_csv(new_csv_path, index=False)

print(f'Data merged and saved to {new_csv_path}')