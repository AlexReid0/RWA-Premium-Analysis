import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

def fetch_fee_and_value(tx_hash, index, total_transactions):
    base_url = 'https://gnosis.blockscout.com/api/v2/transactions/'
    url = f"{base_url}{tx_hash}"
    
    try:
        response = requests.get(url)
        data = response.json()
        fee = data.get('fee', {}).get('value', '0')
        value = data.get('value', '0')
    except Exception as e:
        print(f"Error fetching data for transaction {tx_hash}: {e}")
        fee, value = 'NaN', 'NaN'
    
    # Print the progress
    print(f"Completed {index + 1}/{total_transactions}")
    return {"Fee": fee, "Value": value, "tx_hash": tx_hash}

df = pd.read_csv('April_2.csv')
total_transactions = len(df['tx_hash'])

# Check if the output file already exists to decide whether to write headers
output_file = 'April_3.csv'
write_header = not os.path.exists(output_file)

with ThreadPoolExecutor(max_workers=20) as executor:
    future_to_tx = {executor.submit(fetch_fee_and_value, tx_hash, i, total_transactions): i for i, tx_hash in enumerate(df['tx_hash'])}
    
    for future in as_completed(future_to_tx):
        result = future.result()
        # Open the file in append mode and write the result
        with open(output_file, 'a', newline='') as file:
            df_result = pd.DataFrame([result])
            df_result.to_csv(file, header=write_header, index=False)
            if write_header:  # Ensure header is only written once
                write_header = False

print("Finished updating the dataset with transaction fees and values, saved to 'April_3.csv'.")
