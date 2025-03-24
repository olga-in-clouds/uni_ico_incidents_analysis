import pandas as pd

# Read the merged CSV file
df = pd.read_csv('data/merged_output.csv')

print("\nTotal number of rows:", len(df))

# Display counts of unique values for each column
print("\nNumber of unique values in each column:")
for column in df.columns:
    print(f"{column}: {df[column].nunique()} unique values")

# Get counts of duplicate rows
duplicates = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicates}")

# Count unique combinations of all columns
unique_incidents = len(df.drop_duplicates())
print(f"\nNumber of unique incidents (considering all columns): {unique_incidents}")

# Group by relevant columns and count occurrences
# Note: You might want to adjust these columns based on what defines a unique incident
grouped = df.groupby(df.columns.tolist()).size().reset_index(name='count')
grouped = grouped.sort_values('count', ascending=False)

print("\nTop 10 most frequent incident patterns:")
print(grouped.head(10))

# Save the unique incidents to a new file
df_unique = df.drop_duplicates()
df_unique.to_csv('data/unique_incidents.csv', index=False)

print("\nUnique incidents have been saved to 'data/unique_incidents.csv'") 