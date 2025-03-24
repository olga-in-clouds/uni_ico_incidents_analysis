import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Filter for Q1 2019
q1_2019 = df[(df['Year'] == 2019) & (df['Quarter'] == 'Qtr 1')]

# Count total rows and unique incidents
total_rows = len(q1_2019)
unique_incidents = q1_2019['BI Reference'].nunique()

print("\nQ1 2019 Analysis:")
print("================")
print(f"Total rows: {total_rows:,}")
print(f"Unique incidents: {unique_incidents:,}") 