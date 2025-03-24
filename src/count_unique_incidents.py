import pandas as pd

# Read the merged CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Count occurrences of each BI Reference
incident_counts = df['BI Reference'].value_counts()

print(f"\nTotal number of rows in dataset: {len(df)}")
print(f"Number of unique BI References: {len(incident_counts)}")

print("\nIncidents with multiple entries:")
multiple_entries = incident_counts[incident_counts > 1]
print(f"Number of incidents with multiple entries: {len(multiple_entries)}")
print("\nTop 10 incidents with most entries:")
print(multiple_entries.head(10))

# Analyze what differs in multiple entries for the same BI Reference
print("\nExample of an incident with multiple entries:")
example_bi = multiple_entries.index[0]
print(f"\nDetails for BI Reference: {example_bi}")
print(df[df['BI Reference'] == example_bi])

# Save summary to a file
summary_df = pd.DataFrame({
    'BI Reference': incident_counts.index,
    'Number of Entries': incident_counts.values
})
summary_df.to_csv('data/incident_frequency.csv', index=False)
print("\nDetailed incident frequency has been saved to 'data/incident_frequency.csv'") 