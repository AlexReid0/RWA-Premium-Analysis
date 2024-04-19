import pandas as pd
import requests
import time

def get_token_info(token_address, token_info_cache):
    if token_address in token_info_cache:
        return token_info_cache[token_address]

    url = f"https://gnosis.blockscout.com/api/v2/search?q={token_address}"
    response = requests.get(url)
    time.sleep(0.7)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        if items:
            token_info = items[0]  
            name = token_info.get('name', '') 

            token_info_cache[token_address] = name
            return name

    return ''

df = pd.read_csv('sorted_transactions_4.csv')

df['token_name'] = ''

token_info_cache = {}

for i, row in df.iterrows():
    print(i)
    name = get_token_info(row['house_token'], token_info_cache)
    df.at[i, 'token_name'] = name

df.to_csv('sorted_transactions_5.csv', index=False)



