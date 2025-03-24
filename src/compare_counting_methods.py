import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Count by rows
rows_by_year = df.groupby('Year').size()

# Count by unique incidents
unique_by_year = df.groupby('Year')['BI Reference'].nunique()

# Create comparison
print("\nComparison of Counting Methods:")
print("=============================")
print("\nBy Total Rows (including duplicates):")
print("--------------------------------")
for year, count in rows_by_year.items():
    percentage = (count / len(df)) * 100
    print(f"{int(year)}: {count:,} rows ({percentage:.1f}%)")

print("\nBy Unique Incidents (BI References):")
print("--------------------------------")
for year, count in unique_by_year.items():
    percentage = (count / df['BI Reference'].nunique()) * 100
    print(f"{int(year)}: {count:,} unique incidents ({percentage:.1f}%)")

# Show the difference
print("\nDifference (Rows - Unique Incidents):")
print("--------------------------------")
for year in rows_by_year.index:
    diff = rows_by_year[year] - unique_by_year[year]
    print(f"{int(year)}: {diff:,} duplicate rows")

# Summary
print("\nSummary:")
print("--------")
print(f"Total rows in dataset: {len(df):,}")
print(f"Total unique incidents: {df['BI Reference'].nunique():,}")
print(f"Total duplicate rows: {len(df) - df['BI Reference'].nunique():,}") 