import pandas as pd

# Read the original CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Filter for 2024 data
df_2024 = df[df['Year'] == 2024]

print("\n2024 Incidents Analysis (Original File):")
print("=====================================")
print(f"Total rows for 2024: {len(df_2024):,}")
print(f"Unique BI References in 2024: {df_2024['BI Reference'].nunique():,}")

# Quarterly breakdown
quarterly_counts = df_2024.groupby('Quarter')['BI Reference'].nunique()
print("\nUnique incidents per quarter:")
for quarter, count in quarterly_counts.items():
    print(f"{quarter}: {count:,} incidents")
    
# Count total rows per quarter
quarterly_rows = df_2024.groupby('Quarter').size()
print("\nTotal rows per quarter (including duplicates):")
for quarter, count in quarterly_rows.items():
    print(f"{quarter}: {count:,} rows")

# Analyze duplicates
duplicates = df_2024[df_2024.duplicated(['BI Reference'], keep=False)]
print(f"\nNumber of BI References with multiple entries: {duplicates['BI Reference'].nunique():,}")
print(f"Number of rows that are duplicates: {len(duplicates):,}")

# Distribution of duplicate counts
duplicate_counts = df_2024.groupby('BI Reference').size()
print("\nDistribution of entries per incident:")
for count, frequency in duplicate_counts.value_counts().items():
    print(f"Incidents with {count} entries: {frequency:,}") 