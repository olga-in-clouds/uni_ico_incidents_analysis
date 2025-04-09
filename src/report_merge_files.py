import pandas as pd

# Read the CSV files
df1 = pd.read_csv('data/data-security-incidents-trends-2023.csv')
df2 = pd.read_csv('data/data-security-incidents-trends-2024.csv')

# Concatenate the dataframes
merged_df = pd.concat([df1, df2], ignore_index=True)


# Save the merged dataframe
merged_df.to_csv('data/data-security-incidents-trends-2023-2024.csv', index=False)

print("Files merged successfully!")
print("\nFirst few rows of the merged file:")
print(merged_df.head()) 