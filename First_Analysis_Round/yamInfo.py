import pandas as pd

def transform_token_name(token_name):
    # Remove the prefix "REALTOKEN-S-"
    no_prefix = token_name.replace("REALTOKEN-S-", "")

    # Remove the last segment after the last dash
    no_suffix = '-'.join(no_prefix.split('-')[:-3])

    # Convert to lowercase
    short_name = no_suffix.lower()

    return short_name

df = pd.read_csv('sorted_transactions_3.csv')

df['short_name'] = df['token_symbol'].apply(transform_token_name)

df.to_csv('sorted_transactions_4.csv', index=False)