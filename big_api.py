import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import csv
import time

def fetch_data_and_write(tx_hash, retry=0):
    url = f"https://gnosis.blockscout.com/api/v2/transactions/{tx_hash}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise an exception for 4XX/5XX responses
        data = response.json()
        if data.get("status", "Unknown") not in ["ok", "success"]:
            return None  # Skip this row if status is not 'ok' or 'success'
        
        volume_from = data.get("token_transfers", [{}])[0].get("total", "0")
        volume_to = data.get("token_transfers", [{}])[-1].get("total", "0")
        transaction_fee = data.get('fee', {}).get('value', '0')
        
        return {
            "tx_hash": tx_hash,
            "volume_from": volume_from,
            "volume_to": volume_to,
            "transaction_fee": transaction_fee
        }
    except Exception as e:
        if retry < 20:  # Retry up to 3 times
            print(f"Retry {retry + 1} for transaction {tx_hash} due to error: {e}")
            time.sleep(30)  # Wait for 5 seconds before retrying
            return fetch_data_and_write(tx_hash, retry + 1)  # Retry with incremented retry count
        else:
            print(f"Failed to fetch data for transaction {tx_hash} after multiple attempts: {e}")
            return None

df = pd.read_csv('April_2.csv')

output_file = 'April_3.csv'
if os.path.exists(output_file):
    os.remove(output_file)  # Ensure we're starting fresh

# Using ThreadPoolExecutor to fetch data in parallel
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(fetch_data_and_write, tx_hash) for tx_hash in df['tx_hash']]
    
    with open(output_file, 'a') as f_out:
        # Write headers
        writer = csv.writer(f_out)
        headers = list(df.columns) + ['volume_from', 'volume_to', 'transaction_fee']
        writer.writerow(headers)
        for future in as_completed(futures):
            result = future.result()
            if result:  # If not skipped
                original_row = df.loc[df['tx_hash'] == result['tx_hash']].iloc[0]
                row_data = [original_row[col] for col in df.columns] + [result['volume_from'], result['volume_to'], result['transaction_fee']]
                writer.writerow(row_data)


print("Process completed. Data written to 'April_3.csv'")