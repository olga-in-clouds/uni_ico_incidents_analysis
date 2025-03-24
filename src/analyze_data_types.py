import pandas as pd
import plotly.express as px

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Count unique incidents (BI References) for each Data Type
data_types = df.groupby('Data Type')['BI Reference'].nunique().sort_values(ascending=True)

# Create bar chart
fig = px.bar(x=data_types.index,
             y=data_types.values,
             title='Distribution of Data Types by Unique Incidents',
             labels={'x': 'Data Type', 'y': 'Number of Unique Incidents'},
             template='plotly_white')

# Update layout
fig.update_layout(
    title={
        'text': 'Distribution of Data Types by Unique Incidents<br><sub>Based on unique BI References</sub>',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_tickangle=45,
    height=800  # Make the plot taller to accommodate labels
)

# Save the figure
fig.write_html('figures/data_types_distribution.html')

# Print the data used in the chart
print("\nData Types by Unique Incidents:")
print("=============================")
for data_type, count in data_types.items():
    percentage = (count / df['BI Reference'].nunique()) * 100
    print(f"{data_type}: {count:,} incidents ({percentage:.1f}%)")

print(f"\nTotal unique incidents: {df['BI Reference'].nunique():,}")
print("\nNote: Percentages sum to more than 100% because some incidents involve multiple data types")
print("\nInteractive bar chart saved as 'figures/data_types_distribution.html'") 