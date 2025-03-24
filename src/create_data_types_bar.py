import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Create a unique incident identifier combining BI Reference, Year, and Quarter
df['Incident_ID'] = df['BI Reference'] + '_' + df['Year'].astype(str) + '_' + df['Quarter']

# Count unique quarterly incidents for each Data Type
data_types = df.groupby('Data Type')['Incident_ID'].nunique().sort_values(ascending=True)

# Calculate relative frequencies
total_incidents = df['Incident_ID'].nunique()
relative_freq = (data_types / total_incidents * 100).round(2)

# Create figure
fig = go.Figure()

# Add bars with both count and percentage labels
fig.add_trace(
    go.Bar(
        x=data_types.values,
        y=data_types.index,
        orientation='h',
        text=[f"{x:,} ({relative_freq[i]:.1f}%)" for i, x in enumerate(data_types.values)],
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate="<b>%{y}</b><br>" +
                     "Count: %{x:,}<br>" +
                     "Percentage: %{text}<br>" +
                     "<extra></extra>"
    )
)

# Update layout
fig.update_layout(
    title={
        'text': 'Distribution of Data Types by Unique Quarterly Incidents<br>' +
                f'<sub>Total Unique Quarterly Incidents: {total_incidents:,}</sub>',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Number of Unique Quarterly Incidents",
    yaxis_title="Data Type",
    height=800,
    width=1200,
    showlegend=False,
    margin=dict(l=20, r=250, t=100, b=50),  # Increased right margin to accommodate labels
    plot_bgcolor='white',
    bargap=0.2
)

# Update axes
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=False)

# Save the figure
fig.write_html('figures/data_types_distribution.html')

# Print the data
print("\nDistribution of Data Types:")
print("=========================")
print(f"\nTotal unique quarterly incidents: {total_incidents:,}")
print("\nBreakdown by Data Type:")
for data_type, count in data_types.items():
    percentage = relative_freq[data_type]
    print(f"\n{data_type}:")
    print(f"  Count: {count:,}")
    print(f"  Percentage: {percentage:.1f}%")

print("\nNote: Percentages sum to more than 100% because some incidents involve multiple data types")
print("\nInteractive bar chart saved as 'figures/data_types_distribution.html'") 