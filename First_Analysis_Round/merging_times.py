import pandas as pd
from datetime import datetime

generated_csv_file = "properties_data.csv"
generated_data = pd.read_csv(generated_csv_file)

def convert_to_timestamp(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        return int(datetime.timestamp(date_obj))
    except ValueError:
        return None

generated_data['offering_date_timestamp'] = generated_data['offering_date'].apply(convert_to_timestamp)

merged_csv_file = "merged_dataset_3.csv"
merged_data = pd.read_csv(merged_csv_file)

# Merge the data based on house_token field
merged_data = pd.merge(merged_data, generated_data[['identifier', 'offering_date_timestamp']], left_on='house_token', right_on='identifier', how='left')

merged_data.to_csv("merged_dataset_4.csv", index=False)

print("Data merged and saved as merged_dataset_4.csv")
