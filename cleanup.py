import pandas as pd
import json

df = pd.read_csv('April_3.csv')

df.dropna(how='all', inplace=True)

def extract_and_convert(value):
    if not isinstance(value, str):
        return None
    
    try:
        # Replace single quotes with double quotes and load the string as JSON
        value_dict = json.loads(value.replace("'", "\""))
        # Extract the 'value' part and convert to a decimal number considering the 'decimals'
        converted_value = int(value_dict['value']) / (10 ** int(value_dict['decimals']))
        return converted_value
    except (json.JSONDecodeError, ValueError, TypeError):
        return None

columns_to_convert = ['volume_from', 'volume_to']

# Apply the conversion
for col in columns_to_convert:
    df[col] = df[col].apply(extract_and_convert)

df.to_csv('April_3_cleaned.csv', index=False)