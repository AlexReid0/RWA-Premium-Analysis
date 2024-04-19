import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def wei_to_eth(wei):
    return wei / 10**18

def fetch_transaction_fee(tx_hash):
    api_url = f"{api_base_url}{tx_hash}"
    try:
        response = requests.get(api_url)
        response_json = response.json()

        # Extract the fee value (in wei) and convert it to eth
        fee_wei = int(response_json['fee']['value'])
        fee_eth = wei_to_eth(fee_wei)

        return tx_hash, fee_eth
    except Exception as e:
        print(f"Failed to process transaction {tx_hash}: {e}")
        return tx_hash, None

df = pd.read_csv('uniswap_7.csv')

# Prepare a new column for the transaction fees in eth
df['transaction_fee_eth'] = 0.0

api_base_url = "https://eth.blockscout.com/api/v2/transactions/"

# Using ThreadPoolExecutor to fetch data in parallel
with ThreadPoolExecutor(max_workers=7) as executor:
    futures = [executor.submit(fetch_transaction_fee, tx_hash) for tx_hash in df['tx_hash']]
    
    for future in as_completed(futures):
        tx_hash, fee_eth = future.result()
        if fee_eth is not None:
            index = df.index[df['tx_hash'] == tx_hash].tolist()[0]
            df.at[index, 'transaction_fee_eth'] = fee_eth
            print(index)

df.to_csv('uniswap_8.csv', index=False)