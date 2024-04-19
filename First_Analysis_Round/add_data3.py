import pandas as pd

# Load the spreadsheet
df = pd.read_csv('sorted_transactions_5.csv')

# Function to process the token_name column
def process_token_name(name):
    parts = name.split()
    # Remove first 2 and last 3 terms
    if len(parts) > 5:
        short_name = '-'.join(parts[2:-3])
    else:
        short_name = ''
    return short_name.lower()

# Apply the function to create the new column
df['name_short'] = df['token_name'].apply(process_token_name)

# Define the mappings for replacements
replacements = {
    '4338-4340-east': '4340-east-71',
    '19751-marx-st': '19751-marx',
    '1521-1523-s.drake': '1521-1523-s-drake',
    '305-moss-st': '305-moss',
    '10604': '10604-somerset',
    '16007-nelacrest-rd': '16007-nelacrest',
    '16049-16081-e-seven': '16049-16081-e-seven-mile',
    '19144-riopelle-st': '19144-riopelle',
    '14825-wilfried': '14825-wilfred',
    '1617-s.avers': '1617-s-avers',
    '1815-s.avers': '1815-s-avers',
    '116-monterey-st': '116-monterey',
    '16085-e-seven': '16085-e-seven-mile',
    '18668-saint-louis': '18668-st-louis',
    '19750-marx-st': '19750-marx',
    '1890-marloes-ave': '1890-marloes'
}

# Apply the replacements
df['name_short'] = df['name_short'].replace(replacements)
# Save the modified dataframe as a new CSV file
df.to_csv('sorted_transactions_6.csv', index=False)



# The Exceptions:
# '4338-4340-east' into '4340-east-71'
# '19751-marx-st' into '19751-marx'
# '1521-1523-s.drake' into '1521-1523-s-drake'
# '305-moss-st' into '305-moss'
# '10604' into '10604-somerset'
# '16007-nelacrest-rd' into '16007-nelacrest'
# '16049-16081-e-seven' into '16049-16081-e-seven-mile'
# '19144-riopelle-st' into '19144-riopelle'
# '14825-wilfried' into '14825-wilfred'
# '1617-s.avers' into '1617-s-avers'
# '1815-s.avers' into '1815-s-avers'
# '116-monterey-st' into '116-monterey'
# '16085-e-seven' into '16085-e-seven-mile'
# '18668-saint-louis' into '18668-st-louis'
# '19750-marx-st' into '19750-marx'
# '1890-marloes-ave' into '1890-marloes'