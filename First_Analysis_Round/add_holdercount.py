import requests
import pandas as pd

def get_holder_count(token_address, holder_data):
    if token_address in holder_data:
        return holder_data[token_address]

    api_url = f"https://gnosis.blockscout.com/api/v2/tokens/{token_address}/holders"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            if item['token']['address'] == token_address:
                holders_count = item['token']['holders']
                holder_data[token_address] = holders_count
                return holders_count

    print(f"Failed to retrieve data for token address: {token_address}")
    return None

csv_file = 'merged_dataset.csv'
df = pd.read_csv(csv_file)

holder_data = {}

df['holders_count'] = df['house_token'].apply(lambda x: get_holder_count(x, holder_data))

updated_csv_file = 'merged_dataset_2.csv'
df.to_csv(updated_csv_file, index=False)
print(f"Updated CSV file has been saved as '{updated_csv_file}'.")