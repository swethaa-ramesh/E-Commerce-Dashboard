from prettytable import PrettyTable
import pandas as pd

# Assuming you've already read the CSV file and filled NaN values
df = pd.read_csv("ecommerce_customer_data_large.csv")
df['Returns'].fillna(df['Returns'].mean(), inplace=True)

# Select numerical features
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns

# Display numerical features in a PrettyTable with two-point precision for mean, median, and standard deviation
table_stats = PrettyTable(["Feature", "Mean", "Median", "Correlation", "Std Dev","Variance"])
for feature in numerical_features:
    table_stats.add_row([
        feature,
        f"{df[feature].mean():.2f}",
        f"{df[feature].median():.2f}",
        f"{df['Churn'].corr(df[feature]):.2f}",  # Replace 'Churn' with your target column
        f"{df[feature].std():.2f}",
        f"{df[feature].var():.2f}"
    ])

table_correlation = PrettyTable(["Feature1", "Feature2", "Correlation"])
for i in range(len(numerical_features)):
    for j in range(i + 1, len(numerical_features)):
        feature1 = numerical_features[i]
        feature2 = numerical_features[j]
        correlation = df[feature1].corr(df[feature2])
        table_correlation.add_row([feature1, feature2, f"{correlation:.2f}"])

print("Correlation Table:")
print(table_correlation)

print("Statistics Table:")
print(table_stats)


