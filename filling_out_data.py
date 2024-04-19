import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

def fetch_fee_and_value(tx_hash):
    base_url = 'https://gnosis.blockscout.com/api/v2/transactions/'
    url = f"{base_url}{tx_hash}"
    try:
        response = requests.get(url, timeout=10)  # 10 seconds timeout
        response.raise_for_status()
        data = response.json()
        fee = data.get('fee', {}).get('value', '0')  
        value = data.get('value', '0')
    except Exception as e:
        print(f"Error fetching data for transaction {tx_hash}: {e}")
        fee, value = 'NaN', 'NaN'
    
    return fee, value


df = pd.read_csv('april_merged.csv')
new_file_path = 'april_merged_2.csv'
if os.path.exists(new_file_path):
    os.remove(new_file_path)  # Remove the file if it already exists to start fresh

for index, row in df.iterrows():
    if row['transaction_fee'] in ['0', '', 'NaN', 0] or pd.isna(row['transaction_fee']):
        # Fetch missing data
        fee, value = fetch_fee_and_value(row['tx_hash'])
        # Update the row
        row['transaction_fee'] = fee
        row['value'] = value
    
    # Append the row to the new file
    row.to_frame().T.to_csv(new_file_path, mode='a', header=not os.path.exists(new_file_path), index=False)

print("Processing complete. Data saved to 'april_merged_2.csv'")
