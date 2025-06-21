import pandas as pd


df = pd.read_csv("ecommerce_customer_data_large.csv")
print(df.info())
print(df.columns)
print(df['Customer Name'].unique())
