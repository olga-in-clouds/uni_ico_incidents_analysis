# %% [markdown]
# # Security Incidents Analysis 2019
# 
# Analysis of security incidents data from 2019, including:
# - Incident categories and types
# - Data subject types affected
# - Types of data compromised
# - Reporting times
# - Sector analysis
# - Scale of incidents

# %%
# Import required libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %%
# Load the dataset
file_path = '../data/data-security-incidents-trends-2019.csv'
df = pd.read_csv(file_path)

# Display basic information
print("Dataset Info:")
df.info()

print("\nFirst few rows:")
print(df.head())

# %% [markdown]
# ## 1. Incident Categories and Types Analysis

# %%
# Distribution of Incident Categories
fig = px.pie(df, 
             names='Incident Category',
             title='Distribution of Incident Categories',
             template='plotly_white')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

# Top Incident Types
incident_types = df['Incident Type'].value_counts().head(10)
fig = px.bar(x=incident_types.index, 
             y=incident_types.values,
             title='Top 10 Incident Types',
             labels={'x': 'Incident Type', 'y': 'Count'},
             template='plotly_white')
fig.update_xaxes(tickangle=45)
fig.show()

# %% [markdown]
# ## 2. Data Subject and Type Analysis

# %%
# Data Subject Types Distribution
subject_types = df['Data Subject Type'].value_counts()
fig = px.pie(values=subject_types.values,
             names=subject_types.index,
             title='Distribution of Data Subject Types',
             template='plotly_white')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

# Data Types Analysis
data_types = df['Data Type'].value_counts()
fig = px.bar(x=data_types.index,
             y=data_types.values,
             title='Types of Data Compromised',
             labels={'x': 'Data Type', 'y': 'Count'},
             template='plotly_white')
fig.update_xaxes(tickangle=45)
fig.show()

# %% [markdown]
# ## 3. Temporal Analysis

# %%
# Quarterly Trends
quarterly_incidents = df.groupby(['Quarter', 'Incident Category']).size().unstack(fill_value=0)
fig = px.bar(quarterly_incidents,
             title='Quarterly Incident Trends by Category',
             barmode='group',
             template='plotly_white')
fig.show()

# Reporting Time Analysis
reporting_times = df['Time Taken to Report'].value_counts()
fig = px.bar(x=reporting_times.index,
             y=reporting_times.values,
             title='Distribution of Reporting Times',
             labels={'x': 'Time to Report', 'y': 'Count'},
             template='plotly_white')
fig.update_xaxes(tickangle=45)
fig.show()

# %% [markdown]
# ## 4. Sector Analysis

# %%
# Incidents by Sector
sector_incidents = df['Sector'].value_counts()
fig = px.bar(x=sector_incidents.index,
             y=sector_incidents.values,
             title='Incidents by Sector',
             labels={'x': 'Sector', 'y': 'Number of Incidents'},
             template='plotly_white')
fig.update_xaxes(tickangle=45)
fig.show()

# Heatmap of Sectors vs Incident Types
sector_incident_matrix = pd.crosstab(df['Sector'], df['Incident Category'])
fig = px.imshow(sector_incident_matrix,
                labels=dict(x="Incident Category", y="Sector", color="Count"),
                title="Heatmap: Sectors vs Incident Categories",
                color_continuous_scale='RdYlBu_r')
fig.show()

# %% [markdown]
# ## 5. Scale of Incidents

# %%
# Distribution of Incident Scales
scale_distribution = df['No. Data Subjects Affected'].value_counts()
fig = px.bar(x=scale_distribution.index,
             y=scale_distribution.values,
             title='Scale of Incidents (Number of Data Subjects Affected)',
             labels={'x': 'Number of Subjects', 'y': 'Count'},
             template='plotly_white')
fig.update_xaxes(tickangle=45)
fig.show()

# Scale by Incident Category
fig = px.box(df,
             x='Incident Category',
             y='No. Data Subjects Affected',
             title='Scale of Incidents by Category',
             template='plotly_white')
fig.update_xaxes(tickangle=45)
fig.show()

# %% [markdown]
# ## 6. Decision Analysis

# %%
# Decisions Taken Distribution
decisions = df['Decision Taken'].value_counts()
fig = px.pie(values=decisions.values,
             names=decisions.index,
             title='Distribution of Decisions Taken',
             template='plotly_white')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

# Decision by Incident Category
decision_category_matrix = pd.crosstab(df['Decision Taken'], df['Incident Category'])
fig = px.imshow(decision_category_matrix,
                labels=dict(x="Incident Category", y="Decision Taken", color="Count"),
                title="Heatmap: Decisions vs Incident Categories",
                color_continuous_scale='RdYlBu_r')
fig.show()

# %% [markdown]
# ## 7. Summary Statistics

# %%
# Summary by Sector
sector_summary = df.groupby('Sector').agg({
    'BI Reference': 'count',
    'Incident Type': lambda x: x.nunique(),
    'Data Type': lambda x: x.nunique(),
    'Time Taken to Report': lambda x: x.mode().iloc[0] if not x.empty else None
}).rename(columns={
    'BI Reference': 'Total Incidents',
    'Incident Type': 'Unique Incident Types',
    'Data Type': 'Unique Data Types',
    'Time Taken to Report': 'Most Common Reporting Time'
})

print("\nSummary Statistics by Sector:")
print(sector_summary.sort_values('Total Incidents', ascending=False)) 