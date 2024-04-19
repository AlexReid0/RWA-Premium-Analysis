import pandas as pd
import numpy as np
from datetime import datetime
import time

def to_unix_time(dt_str):
    dt = datetime.strptime(dt_str, '%d/%m/%Y %H:%M')
    return int(time.mktime(dt.timetuple()))

april_start = pd.read_csv('uniswap_6.csv')
crypto_market_cap = pd.read_csv('Crypto_Total_Market_Cap.csv')

crypto_market_cap['DateTime'] = crypto_market_cap['DateTime'].apply(to_unix_time)

crypto_market_cap.rename(columns={'DateTime': 'timestamp', 'Market cap': 'Market Cap'}, inplace=True)

april_start.sort_values('timestamp', inplace=True)
crypto_market_cap.sort_values('timestamp', inplace=True)

merged_df = april_start.copy()
merged_df['total_crypto_market_cap'] = np.nan  

for i, row in merged_df.iterrows():
    filter_condition = crypto_market_cap['timestamp'] <= row['timestamp']
    filtered_crypto = crypto_market_cap[filter_condition]
    
    if not filtered_crypto.empty:
        merged_df.at[i, 'total_crypto_market_cap'] = filtered_crypto.iloc[-1]['Market Cap']

merged_df.to_csv('uniswap_7.csv', index=False)

print("The merge is complete and the result is saved to 'April_2.csv'.")