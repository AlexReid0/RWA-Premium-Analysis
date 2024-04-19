import pandas as pd

# The path to the Excel file containing the "houses" sheet
file_path = 'uniswap_pre_2021_2.xlsx'

# Read the "houses" sheet into a DataFrame
df = pd.read_excel(file_path, sheet_name='houses')

# Generate the "token_symbol" column based on the condition
df['token_symbol'] = df.apply(lambda x: x['Token (In)'] if str(x['Token (In)']).startswith('REAL') else x['Token (Out)'], axis=1)

# Save the modified DataFrame back to the same Excel file, overwriting the "houses" sheet
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, index=False, sheet_name='houses')

print(f"Updated '{file_path}' successfully with the 'token_symbol' column.")