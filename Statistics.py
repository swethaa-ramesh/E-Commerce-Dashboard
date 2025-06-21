import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
# Assuming df is your DataFrame
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'])

# Pairplot to visualize relationships between numerical variables
sns.pairplot(df, hue='Churn', diag_kind='kde', markers=['o', 's'], palette='husl')
plt.show()

