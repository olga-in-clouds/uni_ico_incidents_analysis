import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

print("\nICO Counting Method Analysis:")
print("===========================")

# Count unique incidents per quarter
quarterly_counts = df.groupby(['Year', 'Quarter'])['BI Reference'].nunique()

# Show quarterly breakdown
print("\nQuarterly Breakdown:")
print("-----------------")
for (year, quarter), count in quarterly_counts.items():
    print(f"{int(year)} {quarter}: {count:,} unique incidents")

# Sum by year (ICO method - sum of quarterly unique incidents)
yearly_sums = quarterly_counts.groupby('Year').sum()
print("\nYearly Totals (sum of quarterly unique incidents):")
print("--------------------------------------------")
for year, count in yearly_sums.items():
    print(f"{int(year)}: {count:,} incidents")

# Total using ICO method
total_ico_method = yearly_sums.sum()
print(f"\nTotal incidents (ICO method - sum of all quarterly unique incidents): {total_ico_method:,}")

# Compare with other counting methods
print("\nComparison with Other Counting Methods:")
print("------------------------------------")
print(f"Total rows in dataset: {len(df):,}")
print(f"Total unique BI References overall: {df['BI Reference'].nunique():,}")
print(f"Total incidents (ICO method): {total_ico_method:,}")

# Show why numbers differ
print("\nWhy Numbers Differ:")
print("----------------")
print("1. Row count includes all duplicate entries")
print("2. Unique BI References counts each incident only once ever")
print("3. ICO method counts each incident once per quarter it appears in") 