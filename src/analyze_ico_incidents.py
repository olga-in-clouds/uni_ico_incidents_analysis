import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Basic dataset information
print("\nDataset Overview:")
print(f"Total rows in dataset: {len(df)}")
print(f"Date range: {df['Year'].min()} Q{df['Quarter'].str.extract('(\d+)').min()[0]} to {df['Year'].max()} Q{df['Quarter'].str.extract('(\d+)').max()[0]}")

# Count unique incidents
unique_incidents = df['BI Reference'].nunique()
print(f"\nTotal unique incidents (BI References): {unique_incidents}")

# Analyze incidents by year and quarter
incidents_by_period = df.groupby(['Year', 'Quarter'])['BI Reference'].nunique()
print("\nUnique incidents by period:")
print(incidents_by_period)

# Analyze why we might have multiple rows per incident
print("\nAnalysis of multiple entries:")
multiple_entries = df[df.duplicated(['BI Reference'], keep=False)]
multiple_entries_count = len(df[df['BI Reference'].isin(multiple_entries['BI Reference'].unique())])
print(f"Number of rows that are part of multiple entries: {multiple_entries_count}")

# Analyze what varies in multiple entries
print("\nColumns that commonly vary within the same BI Reference:")
variations = {}
for bi_ref in multiple_entries['BI Reference'].unique()[:10]:  # Look at first 10 examples
    incident_rows = df[df['BI Reference'] == bi_ref]
    for column in df.columns:
        if incident_rows[column].nunique() > 1:
            variations[column] = variations.get(column, 0) + 1

print("\nNumber of times each column varies in multiple entries:")
for column, count in sorted(variations.items(), key=lambda x: x[1], reverse=True):
    print(f"{column}: {count} times")

# Save summary statistics
summary_stats = pd.DataFrame({
    'Metric': ['Total Rows', 'Unique Incidents', 'Incidents with Multiple Entries'],
    'Value': [len(df), unique_incidents, len(multiple_entries['BI Reference'].unique())]
})
summary_stats.to_csv('data/incident_analysis_summary.csv', index=False)

print("\nSummary statistics have been saved to 'data/incident_analysis_summary.csv'") 