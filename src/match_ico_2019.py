import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Filter for 2019 data
df_2019 = df[df['Year'] == 2019]

print("\n2019 Analysis (All Quarters vs Q2-Q4):")
print("====================================")

# Count all quarters
all_quarters = df_2019.groupby('Quarter')['BI Reference'].nunique()
print("\nAll quarters of 2019:")
print("-------------------")
total_all = 0
for quarter, count in all_quarters.items():
    print(f"{quarter}: {count:,} incidents")
    total_all += count
print(f"Total (all quarters): {total_all:,}")

# Count only Q2-Q4 (ICO method)
q2_q4 = df_2019[df_2019['Quarter'].isin(['Qtr 2', 'Qtr 3', 'Qtr 4'])]
q2_q4_counts = q2_q4.groupby('Quarter')['BI Reference'].nunique()
print("\nQ2-Q4 only (ICO method):")
print("----------------------")
total_q2_q4 = 0
for quarter, count in q2_q4_counts.items():
    print(f"{quarter}: {count:,} incidents")
    total_q2_q4 += count
print(f"Total (Q2-Q4): {total_q2_q4:,}")

print("\nComparison:")
print("-----------")
print(f"Our total (all quarters): {total_all:,}")
print(f"Our total (Q2-Q4 only): {total_q2_q4:,}")
print("ICO website total: 12,259")
print(f"Difference from ICO (using Q2-Q4): {12259 - total_q2_q4:,}")

# Show distribution of data types and sectors for Q1
print("\nQ1 2019 Analysis (data not included in ICO numbers):")
print("------------------------------------------------")
q1_data = df_2019[df_2019['Quarter'] == 'Qtr 1']
print(f"Number of incidents in Q1: {q1_data['BI Reference'].nunique():,}")
print("\nSectors affected in Q1:")
print(q1_data['Sector'].value_counts().head()) 