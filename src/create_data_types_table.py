import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('data/data-security-incidents-trends-q1-2019-to-q4-2024.csv')

# Create a unique incident identifier combining BI Reference, Year, and Quarter
df['Incident_ID'] = df['BI Reference'] + '_' + df['Year'].astype(str) + '_' + df['Quarter']

# Count unique quarterly incidents for each Data Type
data_types = df.groupby('Data Type')['Incident_ID'].nunique().sort_values(ascending=False)

# Calculate relative frequencies
total_incidents = df['Incident_ID'].nunique()
relative_freq = (data_types / total_incidents * 100).round(2)

# Create a DataFrame with both frequencies
table_data = pd.DataFrame({
    'Frequency': data_types,
    'Relative Frequency (%)': relative_freq
})

# Create table figure
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['Data Type', 'Frequency', 'Relative Frequency (%)'],
        font=dict(size=12, color='white'),
        fill_color='darkblue',
        align='left'
    ),
    cells=dict(
        values=[table_data.index, 
                table_data['Frequency'], 
                table_data['Relative Frequency (%)'].apply(lambda x: f"{x:.2f}%")],
        font=dict(size=11),
        align='left',
        height=30
    )
)])

# Update layout
fig.update_layout(
    title={
        'text': 'Frequency Distribution of Data Types<br><sub>Based on unique combinations of BI Reference, Year, and Quarter</sub>',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    width=1000,
    height=800
)

# Save the figure
fig.write_html('figures/data_types_frequency_table.html')

# Print the table data
print("\nFrequency Distribution of Data Types:")
print("===================================")
print("\nTotal unique quarterly incidents:", total_incidents)
print("\nFrequency Distribution Table:")
print("---------------------------")
for data_type in table_data.index:
    freq = table_data.loc[data_type, 'Frequency']
    rel_freq = table_data.loc[data_type, 'Relative Frequency (%)']
    print(f"{data_type}:")
    print(f"  Frequency: {freq:,}")
    print(f"  Relative Frequency: {rel_freq:.2f}%")

print("\nNote: Relative frequencies sum to more than 100% because some incidents involve multiple data types")
print("\nInteractive table saved as 'figures/data_types_frequency_table.html'") 