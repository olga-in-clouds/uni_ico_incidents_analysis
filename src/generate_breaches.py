import pandas as pd
import numpy as np
# Define the number of records
num_records = 100
# Generate data for each type of variable
data = {
    'Number_of_Breaches': np.random.randint(1, 11, num_records),
    'Cost_of_Breach': np.random.uniform(10.0, 1000.0, num_records),
    'Type_of_Breach': np.random.choice(['Phishing', 'Malware', 'Ransomware', 'DDoS', 'SQLInjection'], num_records),
    'Severity_of_Breach': np.random.choice(['Low', 'Medium', 'High', 'Critical'], num_records),
    'Time_to_Detection': np.random.uniform(0.0, 100.0, num_records), # time to detection in
    'Data_Loss': np.random.uniform(0.1, 1000.0, num_records) # loss in GB
}
# Create a DataFrame
df = pd.DataFrame(data)
# Save to a CSV file
df.to_csv('cybersecurity_dataset.csv', index=False)
print(df.head())