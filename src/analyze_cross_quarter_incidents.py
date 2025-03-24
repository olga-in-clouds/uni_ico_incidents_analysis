import pandas as pd

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Find incidents that appear in multiple quarters
cross_quarter = df.groupby('BI Reference').agg({
    'Quarter': 'nunique',
    'Year': 'nunique'
}).reset_index()

multi_quarter_refs = cross_quarter[cross_quarter['Quarter'] > 1]['BI Reference']

print("\nCross-Quarter Analysis:")
print("======================")
print(f"Number of incidents appearing in multiple quarters: {len(multi_quarter_refs)}")

# Analyze an example in detail
if len(multi_quarter_refs) > 0:
    example_bi = multi_quarter_refs.iloc[0]
    example_data = df[df['BI Reference'] == example_bi].sort_values(['Year', 'Quarter'])
    
    print(f"\nDetailed example - BI Reference: {example_bi}")
    print("\nTimeline of this incident:")
    print(example_data[['Year', 'Quarter', 'Data Type', 'Decision Taken', 'Time Taken to Report', 'Sector']])
    
    # Analyze what changes between quarters
    print("\nChanges between quarters:")
    for column in df.columns:
        if example_data[column].nunique() > 1:
            print(f"\n{column} changes:")
            for _, row in example_data.iterrows():
                print(f"{row['Year']} {row['Quarter']}: {row[column]}")

# Analyze patterns in cross-quarter incidents
print("\nAnalysis of cross-quarter patterns:")
print(f"Average quarters per incident: {cross_quarter['Quarter'].mean():.2f}")
print("\nDistribution of quarters per incident:")
print(cross_quarter['Quarter'].value_counts().sort_index())

# Look at time gaps
def analyze_time_gaps(incident_data):
    quarters = incident_data.apply(lambda x: f"{x['Year']}-{x['Quarter']}")
    return quarters.nunique()

time_patterns = df[df['BI Reference'].isin(multi_quarter_refs)].groupby('BI Reference').apply(analyze_time_gaps)
print("\nNumber of distinct quarters per cross-quarter incident:")
print(time_patterns.value_counts().sort_index())

# Save analysis of cross-quarter incidents
cross_quarter_details = df[df['BI Reference'].isin(multi_quarter_refs)].sort_values(['BI Reference', 'Year', 'Quarter'])
cross_quarter_details.to_csv('data/cross_quarter_incidents.csv', index=False)
print("\nDetailed cross-quarter incident data saved to 'data/cross_quarter_incidents.csv'") 