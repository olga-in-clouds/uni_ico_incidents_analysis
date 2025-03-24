import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Count incidents by quarter (ICO style)
quarterly_counts = df.groupby(['Year', 'Quarter'])['BI Reference'].nunique()
total_incidents = quarterly_counts.sum()

print("\nICO-style Analysis:")
print("===================")
print(f"\nTotal incidents (sum of quarterly unique incidents): {total_incidents}")
print("\nBreakdown by quarter:")
print(quarterly_counts)

# Create a yearly summary
yearly_counts = df.groupby('Year')['BI Reference'].nunique()
print("\nYearly summary:")
print(yearly_counts)

# Save detailed quarterly analysis
quarterly_df = quarterly_counts.reset_index()
quarterly_df.columns = ['Year', 'Quarter', 'Number of Incidents']
quarterly_df.to_csv('data/quarterly_incident_counts.csv', index=False)

print("\nDetailed quarterly analysis saved to 'data/quarterly_incident_counts.csv'")

# Print verification stats
print("\nVerification Statistics:")
print("========================")
print(f"Total rows in dataset: {len(df)}")
print(f"Unique BI References overall: {df['BI Reference'].nunique()}")
print("Note: The difference between total incidents and unique BI References")
print("is because some incidents span multiple quarters and are counted multiple times")
print("in the ICO's reporting method.") 