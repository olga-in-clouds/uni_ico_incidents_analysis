import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Filter for 2024 data
df_2024 = df[df['Year'] == 2024]

# Create unique incident identifier
df_2024['Incident_ID'] = df_2024['BI Reference'] + '_' + df_2024['Year'].astype(str) + '_' + df_2024['Quarter']

print("\nTotal Incidents Reported in 2024 by Quarter:")
print("==========================================")

# Count by quarter
for quarter in sorted(df_2024['Quarter'].unique()):
    quarter_data = df_2024[df_2024['Quarter'] == quarter]
    total = quarter_data['Incident_ID'].nunique()
    print(f"{quarter}: {total:,} unique incidents")

# Overall total for 2024
total_2024 = df_2024['Incident_ID'].nunique()
print(f"\nTotal unique incidents in 2024: {total_2024:,}")