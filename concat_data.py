def concatenate_csv_files(file_path1, file_path2, output_file_path):
    import pandas as pd

    csv1 = pd.read_csv(file_path1)
    csv2 = pd.read_csv(file_path2)
    
    matching_columns = [col for col in csv1.columns if col in csv2.columns]
    
    csv1_matched = csv1[matching_columns]
    csv2_matched = csv2[matching_columns]
    
    # Concatenate the data
    concatenated_df = pd.concat([csv1_matched, csv2_matched], ignore_index=True)
    
    # Save the concatenated data to a new CSV file
    concatenated_df.to_csv(output_file_path, index=False)

    return f"Data from {file_path1} and {file_path2} has been concatenated into {output_file_path}, based on matching column names."

print(concatenate_csv_files("April_5.csv","uniswap_8.csv","final.csv"))