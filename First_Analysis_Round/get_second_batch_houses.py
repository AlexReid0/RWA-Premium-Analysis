import requests
from web3 import Web3
import json
import time
from decimal import Decimal
import csv

# Function to fetch transaction data using its hash
def fetch_logs(token_address, api_key, topic):
    url = f"https://api.gnosisscan.io/api?module=logs&action=getLogs&address={token_address}&topic0={topic}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        return None

# Function to decode transaction input data
def decode_transaction_input(web3, contract_abi, input_data):
    contract = web3.eth.contract(abi=contract_abi)
    return contract.decode_function_input(input_data)
# Function to fetch transactions for a given token address
def fetch_transactions(token_address, api_key):
    url = f"https://api.gnosisscan.io/api?module=account&action=txlist&address={token_address}&sort=asc&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        return None



def find_event_by_signature(web3, abi, event_signature_hash):
    for item in abi:
        if item['type'] == 'event':
            signature = web3.keccak(text=f"{item['name']}({','.join([input['type'] for input in item['inputs']])})").hex()
            if signature == event_signature_hash:
                return item
    return None
def fetch_abi(contract_address, api_key):
    url = f"https://api.gnosisscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200 and 'result' in response.json():
        return json.loads(response.json()['result'])
    else:
        return None
    
def main():
    api_key = "YOUR_GNOSISSCAN_API_KEY"
    web3 = Web3(Web3.HTTPProvider('https://YOUR_GNOSIS_RPC_ENDPOINT/'))
    abi = fetch_abi("0x5c4DE81a9c2b9290315cb6F379D91A49248C6536",api_key)
    contract = web3.eth.contract(address="0x13385924683d2a2D0ff5D54e3524EbE2D1dE79C3")
    transactions = fetch_transactions("0x13385924683d2a2D0ff5D54e3524EbE2D1dE79C3",api_key)
    created=[]
    

    for tx in transactions:
        receipt = web3.eth.get_transaction_receipt(tx['hash'])

        for log in receipt.logs:  # Assuming 'logs' is your list of log entries
            print("Original Log Topic:", log['topics'][0])
            event_signature_hash = log['topics'][0].hex()  # Convert to hex string
            print("Converted Log Topic:", event_signature_hash)

            event = find_event_by_signature(web3, abi, event_signature_hash)
            if event:
                # Decode the log
                decoded_log = web3.eth.abi.decode_log(event['inputs'], log['data'], log['topics'][1:])
                print("Decoded Log:", decoded_log)
            else:
                print("No matching event found for topic:", event_signature_hash)


    print(created)

        
if __name__ == "__main__":
    main()