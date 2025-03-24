import pandas as pd

# Read the original CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Convert Quarter to a numeric value for sorting
df['Quarter_Num'] = df['Quarter'].str.extract('(\d+)').astype(int)

# Create a combined date field for sorting
df['Report_Order'] = df['Year'].astype(str) + df['Quarter_Num'].astype(str).str.zfill(2)

# Sort by Report_Order to ensure we keep the earliest occurrence
df_sorted = df.sort_values(['BI Reference', 'Report_Order'])

# Keep only the first occurrence of each BI Reference
df_unique = df_sorted.drop_duplicates(subset=['BI Reference'], keep='first')

# Remove the temporary columns we added
df_unique = df_unique.drop(['Quarter_Num', 'Report_Order'], axis=1)

# Save to a new file
output_file = 'data/data-security-incidents-unique-first-report.csv'
df_unique.to_csv(output_file, index=False)

# Print summary statistics
print("\nDuplicate Removal Summary:")
print("=========================")
print(f"Original number of rows: {len(df):,}")
print(f"Number of unique incidents: {len(df_unique):,}")
print(f"Number of duplicate entries removed: {len(df) - len(df_unique):,}")

# Show distribution by year in the new dataset
yearly_counts = df_unique.groupby('Year').size()
print("\nDistribution by year (unique incidents):")
for year, count in yearly_counts.items():
    print(f"{int(year)}: {count:,} incidents")

# Show distribution by quarter
quarterly_counts = df_unique.groupby(['Year', 'Quarter']).size()
print("\nQuarterly breakdown (unique incidents):")
for (year, quarter), count in quarterly_counts.items():
    print(f"{int(year)} {quarter}: {count:,} incidents")

print(f"\nNew file saved as: {output_file}") 