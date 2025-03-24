import pandas as pd

# Read the CSV files
df1 = pd.read_csv('data/data-security-incidents-trends-2019.csv')
df2 = pd.read_csv('data/data-security-incidents-trends-2020.csv')
df3 = pd.read_csv('data/data-security-incidents-trends-2021.csv')
df4 = pd.read_csv('data/data-security-incidents-trends-2022.csv')
df5 = pd.read_csv('data/data-security-incidents-trends-2023.csv')
df6 = pd.read_csv('data/data-security-incidents-trends-2024.csv')

# Concatenate the dataframes
merged_df = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)

# Sort by column A to ensure nice ordering
#merged_df = merged_df.sort_values('A')

# Save the merged dataframe
merged_df.to_csv('data/merged_output.csv', index=False)

print("Files merged successfully!")
print("\nFirst few rows of the merged file:")
print(merged_df.head()) 