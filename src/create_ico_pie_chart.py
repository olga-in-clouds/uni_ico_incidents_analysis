import pandas as pd
import plotly.express as px

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Count unique incidents per quarter and sum by year (ICO method)
quarterly_counts = df.groupby(['Year', 'Quarter'])['BI Reference'].nunique()
yearly_totals = quarterly_counts.groupby('Year').sum().reset_index()
yearly_totals.columns = ['Year', 'Incidents']

# Create pie chart
fig = px.pie(yearly_totals, 
             values='Incidents',
             names='Year',
             title='Security Incidents by Year (ICO Counting Method)',
             template='plotly_white')

# Update layout
fig.update_traces(textposition='inside', 
                 textinfo='percent+label+value',
                 hovertemplate="Year: %{label}<br>Incidents: %{value:,}<br>Percentage: %{percent}")

fig.update_layout(
    title={
        'text': 'Security Incidents by Year (ICO Counting Method)<br><sub>Based on unique incidents per quarter</sub>',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Save the figure
fig.write_html('figures/incidents_by_year_pie.html')

# Print the data used in the chart
print("\nData Used in Visualization:")
print("=========================")
print("\nYearly Totals (sum of quarterly unique incidents):")
for _, row in yearly_totals.iterrows():
    percentage = (row['Incidents'] / yearly_totals['Incidents'].sum()) * 100
    print(f"{int(row['Year'])}: {int(row['Incidents']):,} incidents ({percentage:.1f}%)")

print(f"\nTotal incidents across all years: {yearly_totals['Incidents'].sum():,}")
print("\nInteractive pie chart saved as 'figures/incidents_by_year_pie.html'") 