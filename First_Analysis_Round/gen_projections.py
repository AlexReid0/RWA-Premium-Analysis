import pandas as pd
from datetime import datetime
import numpy as np

# Load datasets
merged_data = pd.read_csv('merged_dataset_4.csv')
monthly_data = pd.read_csv('Monthly Data.csv', parse_dates=['DATE'], dayfirst=True)
quarterly_data = pd.read_csv('Quarterly Data.csv', parse_dates=['DATE'], dayfirst=True)

monthly_data['DATE'] = pd.to_datetime(monthly_data['DATE'], dayfirst=True)
quarterly_data['DATE'] = pd.to_datetime(quarterly_data['DATE'], dayfirst=True)

def unix_to_date(unix_time):
    return datetime.utcfromtimestamp(int(unix_time))

def get_indices_and_growth_rate(region, offering_date, transaction_date, is_monthly):
    data = monthly_data if is_monthly else quarterly_data

    offering_date = pd.to_datetime(offering_date)
    transaction_date = pd.to_datetime(transaction_date)

    prev_offering_idx = data[data['DATE'] <= offering_date].tail(1)[region].values[0]
    prev_transaction_idx = data[data['DATE'] <= transaction_date].tail(1)[region].values[0]

    growth_rate = prev_transaction_idx / prev_offering_idx if prev_offering_idx else np.nan

    return prev_offering_idx, prev_transaction_idx, growth_rate

region_mapping = {
    'detroit': ('Detroit', True),
    'cleveland': ('Cleveland', True),
    'chicago': ('Chicago', True),
    'birmingham': ('Birmingham', False),
    'toledo': ('Toledo', False),
    'kissimmee': ('Kissimmee', False),
    'miami': ('Miami', True),
    'rochester': ('Rochester', False),
    'highland park': ('Chicago', True),
    'east cleveland': ('Cleveland', True),
    'deerfield beach': ('Miami', True),
    'akron': ('Akron', False),
    'dearborn heights': ('Detroit', True),
    'jackson': ('Jackson', False)
}

initial_indices = []
transaction_indices = []
growth_rates = []
valuations = []

for index, row in merged_data.iterrows():
    region = row['city'].lower()
    if region in region_mapping:
        index_name, is_monthly = region_mapping[region]
        offering_date = unix_to_date(row['offering_date_timestamp'])
        transaction_date = unix_to_date(row['timeStamp'])

        # Get the index values and growth rate
        offering_idx, transaction_idx, growth_rate = get_indices_and_growth_rate(index_name, offering_date, transaction_date, is_monthly)

        # Debug output
        print(f"Row {index}: {region} | Offering Date: {offering_date} | Transaction Date: {transaction_date}")
        print(f"Initial Index: {offering_idx} | Transaction Index: {transaction_idx} | Growth Rate: {growth_rate}")

        initial_indices.append(offering_idx)
        transaction_indices.append(transaction_idx)
        growth_rates.append(growth_rate)

        # Calculate valuation
        valuation_t = row['initial_market_cap_without_premium'] * growth_rate if growth_rate else np.nan
        valuations.append(valuation_t)
    else:
        initial_indices.append(np.nan)
        transaction_indices.append(np.nan)
        growth_rates.append(np.nan)
        valuations.append(np.nan)

# Add the new columns to the dataset
merged_data['initial_index_value'] = initial_indices
merged_data['transaction_index_value'] = transaction_indices
merged_data['growth_rate'] = growth_rates
merged_data['valuation_t'] = valuations

# Save the new dataset
merged_data.to_csv('merged_dataset_5.csv', index=False)
