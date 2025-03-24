import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Filter for 2024 data
df_2024 = df[df['Year'] == 2024].copy()

print("\n2024 Analysis:")
print("==============")
print(f"Total rows in 2024: {len(df_2024)}")
print(f"Unique BI References in 2024: {df_2024['BI Reference'].nunique()}")

# Find duplicated BI References in 2024
duplicates_2024 = df_2024[df_2024.duplicated(['BI Reference'], keep=False)].sort_values('BI Reference')
print(f"\nNumber of rows that are duplicates: {len(duplicates_2024)}")
print(f"Number of BI References with multiple entries: {duplicates_2024['BI Reference'].nunique()}")

# Analyze what differs in duplicate entries
if len(duplicates_2024) > 0:
    print("\nExample of duplicate entries:")
    example_bi = duplicates_2024['BI Reference'].iloc[0]
    example_entries = df_2024[df_2024['BI Reference'] == example_bi]
    
    print(f"\nShowing all entries for BI Reference: {example_bi}")
    print(example_entries)
    
    print("\nColumns that vary within this BI Reference:")
    for column in df_2024.columns:
        if example_entries[column].nunique() > 1:
            print(f"{column}: {sorted(example_entries[column].unique())}")

# Quarterly breakdown
quarterly_counts = df_2024.groupby('Quarter')['BI Reference'].nunique()
print("\nUnique incidents per quarter in 2024:")
print(quarterly_counts)

# Save 2024 analysis
duplicates_2024.to_csv('data/2024_duplicates.csv', index=False)
print("\nDetailed 2024 duplicate entries saved to 'data/2024_duplicates.csv'") 