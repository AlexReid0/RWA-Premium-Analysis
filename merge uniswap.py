import pandas as pd

# The path to your Excel file
file_path = 'uniswap_pre_2021.xlsx'

# List of sheet names to iterate through
sheet_names = [
    "Liberal15634", "Mansfield18900", "Andover25097", 
    "Appoline18276", "Schaefer8342", "Lesure20200", 
    "Appoline10024", "Patton9336", "Audubon5942", 
    "Fullerton16200", "Marlowe9943"
]

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# Iterate through each sheet name, read the sheet, and append the data to all_data
for sheet_name in sheet_names:
    # Read the current sheet
    sheet_data = pd.read_excel(file_path, sheet_name=sheet_name)
    # Append the data from the current sheet to all_data
    all_data = pd.concat([all_data, sheet_data], ignore_index=True)

# Now all_data contains all the rows from the specified sheets
# Write this combined data to a new Excel file with one sheet named "houses"
output_file_path = 'uniswap_pre_2021_2.xlsx'
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    all_data.to_excel(writer, index=False, sheet_name='houses')

print(f"Data combined into '{output_file_path}' successfully.")