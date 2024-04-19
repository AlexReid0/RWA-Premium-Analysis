import pandas as pd

yamInfo = pd.read_csv('yamInfo_modified.csv')
sorted_transactions = pd.read_csv('sorted_transactions_6.csv')

merged_data = pd.merge(sorted_transactions, yamInfo, left_on='name_short', right_on='name_new', how='left')

merged_data.to_csv('merged_dataset.csv', index=False)

print("Merging complete. Output saved to 'merged_dataset.csv'.")

merged_data = pd.read_csv('merged_dataset.csv')


unique_short_names_with_empty_rmm = set(merged_data[merged_data['rmm'].isna()]['name_short'])

print(unique_short_names_with_empty_rmm)



