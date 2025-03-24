import pandas as pd
import plotly.express as px

# Create the data
data = {'Color': ['Brown', 'Yellow', 'Red', 'Orange', 'Blue', 'Green'],
        'Frequency': [12, 10, 9, 6, 3, 5]}

# Create DataFrame
df = pd.DataFrame(data, columns=['Color', 'Frequency'])

# Create interactive bar plot with Plotly
fig = px.bar(df, 
             x='Color', 
             y='Frequency',
             title='Color Frequency Distribution',
             color='Color',  # This will color each bar according to its category
             template='plotly_white')  # Clean, modern template

# Update layout for better appearance
fig.update_layout(
    xaxis_title="Color",
    yaxis_title="Frequency",
    showlegend=False  # Hide legend since colors are self-explanatory
)

# Show the plot
fig.show() 