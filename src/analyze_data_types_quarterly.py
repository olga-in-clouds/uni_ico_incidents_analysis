import pandas as pd
import plotly.express as px

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Create a unique incident identifier combining BI Reference, Year, and Quarter
df['Incident_ID'] = df['BI Reference'] + '_' + df['Year'].astype(str) + '_' + df['Quarter']

# Count unique quarterly incidents for each Data Type
data_types = df.groupby('Data Type')['Incident_ID'].nunique().sort_values(ascending=True)

# Create bar chart
fig = px.bar(x=data_types.index,
             y=data_types.values,
             title='Distribution of Data Types by Unique Quarterly Incidents',
             labels={'x': 'Data Type', 'y': 'Number of Unique Quarterly Incidents'},
             template='plotly_white')

# Update layout
fig.update_layout(
    title={
        'text': 'Distribution of Data Types by Unique Quarterly Incidents<br><sub>Based on unique combinations of BI Reference, Year, and Quarter</sub>',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_tickangle=45,
    height=800  # Make the plot taller to accommodate labels
)

# Save the figure
fig.write_html('figures/data_types_quarterly_distribution.html')

# Print the data used in the chart
print("\nData Types by Unique Quarterly Incidents:")
print("=====================================")
total_unique_quarterly = df['Incident_ID'].nunique()
for data_type, count in data_types.items():
    percentage = (count / total_unique_quarterly) * 100
    print(f"{data_type}: {count:,} incidents ({percentage:.1f}%)")

print(f"\nTotal unique quarterly incidents: {total_unique_quarterly:,}")
print("\nBreakdown by year:")
yearly_counts = df.groupby('Year')['Incident_ID'].nunique()
for year, count in yearly_counts.items():
    print(f"{int(year)}: {count:,} incidents")

print("\nNote: Percentages sum to more than 100% because some incidents involve multiple data types")
print("\nInteractive bar chart saved as 'figures/data_types_quarterly_distribution.html'") 