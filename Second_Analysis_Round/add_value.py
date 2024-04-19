import pandas as pd

file_path = 'April_4.csv'
df = pd.read_csv(file_path)

target_token = '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d'

# Use apply with a lambda function to calculate the transaction_value
df['transaction_value'] = df.apply(
    lambda row: row['volume_bought'] if row['token_bought'] == target_token 
    else (row['volume_sold'] if row['token_sold'] == target_token else None),
    axis=1
)

# Save the updated DataFrame back to a CSV
df.to_csv('April_5.csv', index=False)
print( df['transaction_value'].isnull().sum())
print("New column 'transaction_value' added and saved to 'April_3_cleaned_with_transaction_value.csv'.")
