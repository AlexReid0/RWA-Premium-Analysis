

import pandas as pd

df = pd.read_csv('updated_transactions.csv')


import pandas as pd
import requests
import time

def get_token_info(token_address, token_info_cache):
    # Check if token info is already in the cache
    if token_address in token_info_cache:
        return token_info_cache[token_address]
    url = f"https://gnosis.blockscout.com/api/v2/search?q={token_address}"
    response = requests.get(url)
    time.sleep(2)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        if items:
            token_info = items[0]  
            symbol = token_info.get('symbol', '')
            total_supply = token_info.get('total_supply', 0)
            total_supply = float(total_supply) / 1e18

            token_info_cache[token_address] = (symbol, total_supply)
            return symbol, total_supply

    return '', 0

df = pd.read_csv('sorted_transactions.csv')
df['token_symbol'] = ''
df['adjusted_supply'] = 0
token_info_cache = {}
for i, row in df.iterrows():
    print(i)
    symbol, supply = get_token_info(row['house_token'], token_info_cache)
    df.at[i, 'token_symbol'] = symbol
    df.at[i, 'adjusted_supply'] = supply
df.to_csv('sorted_transactions_2.csv', index=False)

print("Updated data saved to 'sorted_transactions_2.csv'")