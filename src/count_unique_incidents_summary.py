import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Basic counts
total_rows = len(df)
unique_bi_refs = df['BI Reference'].nunique()

print("\nUnique Incidents Summary:")
print("========================")
print(f"Total rows in dataset: {total_rows:,}")
print(f"Unique BI References: {unique_bi_refs:,}")

# Count by year
yearly_counts = df.groupby('Year')['BI Reference'].nunique()
print("\nUnique incidents by year:")
for year, count in yearly_counts.items():
    print(f"{int(year)}: {count:,} incidents")

# Count by quarter (total across all years)
quarterly_counts = df.groupby(['Year', 'Quarter'])['BI Reference'].nunique()
print("\nQuarterly breakdown:")
for (year, quarter), count in quarterly_counts.items():
    print(f"{int(year)} {quarter}: {count:,} incidents")

# Calculate total of quarterly counts
total_quarterly = quarterly_counts.sum()
print(f"\nSum of quarterly incidents: {total_quarterly:,}")
print("(This matches ICO's counting method)")

# Analyze incidents spanning multiple quarters
incidents_per_quarter = df.groupby('BI Reference').agg({
    'Quarter': 'nunique',
    'Year': 'nunique'
})

print("\nIncident duration analysis:")
print(f"Single quarter incidents: {len(incidents_per_quarter[incidents_per_quarter['Quarter'] == 1]):,}")
print(f"Multi-quarter incidents: {len(incidents_per_quarter[incidents_per_quarter['Quarter'] > 1]):,}") 