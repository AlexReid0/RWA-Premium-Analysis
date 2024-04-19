
import pandas as pd
import requests

df = pd.read_excel("uniswap_pre_2021_2.xlsx")

api_key = "censored"

def get_transaction_data(txn_hash, api_key):
    try:
        url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={txn_hash}&apikey={api_key}"
        response = requests.get(url, timeout=10)  # Added timeout for safety
        data = response.json()
        gas_price = int(data['result']['gasPrice'], 16) if data['result'] and 'gasPrice' in data['result'] else None
        value = int(data['result']['value'], 16) if data['result'] and 'value' in data['result'] else None
        return {"Txn Hash": txn_hash, "Gas Price": gas_price, "Value": value}
    except Exception as e:
        print(f"Error retrieving data for {txn_hash}: {e}")
        return {"Txn Hash": txn_hash, "Gas Price": None, "Value": None}

output_filename = "uniswap_pre_2021_3.csv"
pd.DataFrame(columns=["Txn Hash", "Gas Price", "Value"]).to_csv(output_filename, index=False)

for index, row in df.iterrows():
    txn_hash = row['Txn Hash']
    transaction_data = get_transaction_data(txn_hash, api_key)
    pd.DataFrame([transaction_data]).to_csv(output_filename, mode='a', header=False, index=False)
    print(f"Processed transaction count: {index + 1}")
