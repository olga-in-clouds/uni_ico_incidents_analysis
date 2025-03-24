import pandas as pd

a = pd.read_csv("file1.csv")
b = pd.read_csv("file2.csv")
merged_df = pd.merge(a, b, on='A')

merged_df.to_csv("output.csv", index=False)