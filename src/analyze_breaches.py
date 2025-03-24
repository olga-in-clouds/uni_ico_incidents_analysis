import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Set plot styles
plt.style.use('seaborn')
sns.set_palette('deep')

# Load the dataset
df = pd.read_csv('cybersecurity_dataset.csv')

# 1. Basic Information
print("\n=== Dataset Info ===")
print(df.info())

print("\n=== First Few Rows ===")
print(df.head())

# 2. Statistical Summary
print("\n=== Summary Statistics ===")
print(df.describe())

print("\n=== Breach Types Distribution ===")
print(df['Type_of_Breach'].value_counts())

print("\n=== Severity Distribution ===")
print(df['Severity_of_Breach'].value_counts())

# 3. Visualizations
# Cost distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Cost_of_Breach', bins=30)
plt.title('Distribution of Breach Costs')
plt.xlabel('Cost ($)')
plt.show()

# Costs by breach type
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Type_of_Breach', y='Cost_of_Breach')
plt.title('Cost Distribution by Breach Type')
plt.xticks(rotation=45)
plt.show()

# Severity analysis
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.countplot(data=df, x='Severity_of_Breach', order=['Low', 'Medium', 'High', 'Critical'])
plt.title('Distribution of Breach Severity')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.boxplot(data=df, x='Severity_of_Breach', y='Data_Loss', order=['Low', 'Medium', 'High', 'Critical'])
plt.title('Data Loss by Severity Level')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Correlation Analysis
numerical_cols = ['Number_of_Breaches', 'Cost_of_Breach', 'Time_to_Detection', 'Data_Loss']
correlation_matrix = df[numerical_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Numerical Variables')
plt.show()

# 5. Statistical Analysis
X = sm.add_constant(df['Time_to_Detection'])
y = df['Cost_of_Breach']
model = sm.OLS(y, X).fit()

print("\n=== Regression Analysis: Impact of Detection Time on Cost ===")
print(model.summary())

plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='Time_to_Detection', y='Cost_of_Breach')
plt.title('Relationship between Detection Time and Cost')
plt.show()

# 6. Risk Analysis
risk_by_type = df.groupby('Type_of_Breach').agg({
    'Cost_of_Breach': ['mean', 'std', 'count'],
    'Data_Loss': 'mean',
    'Time_to_Detection': 'mean'
}).round(2)

print("\n=== Risk Analysis by Breach Type ===")
print(risk_by_type) 