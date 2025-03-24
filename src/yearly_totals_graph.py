import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Create unique incident identifier
df['Incident_ID'] = df['BI Reference'] + '_' + df['Year'].astype(str) + '_' + df['Quarter']

# Calculate yearly totals
yearly_data = []
for year in sorted(df['Year'].unique()):
    year_data = df[df['Year'] == year]
    total_incidents = year_data['Incident_ID'].nunique()
    yearly_data.append([year, total_incidents])

# Calculate total for percentages
total_all_years = sum(total for _, total in yearly_data)

# Create bar graph
fig = go.Figure(data=[
    go.Bar(
        x=[year for year, _ in yearly_data],
        y=[total for _, total in yearly_data],
        text=[f"{round((total/total_all_years * 100), 1)}%" for _, total in yearly_data],
        textposition='outside',
        marker_color='rgb(49, 130, 189)'
    )
])

# Update layout
fig.update_layout(
    title={
        'text': 'Figure 1: Yearly Distribution of Unique Incidents',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=14)
    },
    xaxis_title="Year",
    yaxis_title="Number of Unique Incidents",
    width=800,
    height=500,
    showlegend=False,
    plot_bgcolor='white',
    yaxis=dict(
        gridcolor='lightgrey',
        gridwidth=1
    )
)

# Save the figure
fig.write_html('figures/yearly_totals_graph.html')

# Print the data
print("\nYearly Distribution of Unique Incidents:")
print("=====================================")
print(f"Total incidents across all years: {total_all_years:,}")
print("\nBreakdown by year:")
for year, total in yearly_data:
    percentage = round((total/total_all_years * 100), 1)
    print(f"{year}: {total:,} incidents ({percentage}%)")

print("\nInteractive graph saved as 'figures/yearly_totals_graph.html'") 