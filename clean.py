import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.stats import boxcox
from scipy.stats import anderson
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("ecommerce_customer_data_large.csv")
print(df.info())
print(df.isnull().sum())
print(df.isnull().any())

#1
# Filling missing values in 'Returns' with the mean
df['Returns'].fillna(df['Returns'].mean(), inplace=True)
cleaned_df_head = df.head()
cleaned_df_stats = df.describe()
print("Cleaned Dataset - First Few Observations:")
print(cleaned_df_head)
print(df.isnull().sum())
print("\nCleaned Dataset - Statistics:")
print(cleaned_df_stats)

#2 Out-liners
from scipy import stats
z_threshold = 3
z_scores = stats.zscore(df.select_dtypes(include=['int64', 'float64']))
outliers = (abs(z_scores) > z_threshold).all(axis=1)
cleaned_outliers = df[~outliers]
cleaned_outliers_stats = cleaned_outliers.describe()

# Print the cleaned DataFrame without outliers
print("Cleaned Dataset without Outliers:")
print(cleaned_outliers)

# Print the statistics of the cleaned dataset without outliers
print("\nCleaned Dataset without Outliers - Statistics:")
print(cleaned_outliers_stats)

#PCA
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[numerical_features])

# Perform PCA
pca = PCA()
pca_result = pca.fit_transform(scaled_data)

# Explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_

# Display explained variance ratio for each principal component
print("Explained Variance Ratio:")
print(explained_variance_ratio)

# Cumulative explained variance
cumulative_variance_ratio = explained_variance_ratio.cumsum()

# Display cumulative explained variance
print("\nCumulative Explained Variance:")
print(cumulative_variance_ratio)

# Number of principal components to retain based on desired explained variance
desired_explained_variance = 0.95  # Adjust as needed
num_components = (cumulative_variance_ratio < desired_explained_variance).sum() + 1

# Retain the desired number of principal components
pca_result_reduced = pca_result[:, :num_components]

# Display the number of retained principal components
print(f"\nNumber of Retained Principal Components: {num_components}")

# Condition number of the covariance matrix
condition_number = np.linalg.cond(pca.get_covariance())
print(f"\nCondition Number of Covariance Matrix: {condition_number}")

# Singular values of the retained principal components
singular_values = pca.singular_values_[:num_components]
print("\nSingular Values of Retained Principal Components:")
print(singular_values)

#Normality
# Significance levels for the Anderson-Darling test
alpha_levels = [0.01, 0.05, 0.1]

# Loop through numerical features and perform the Anderson-Darling test
for feature in numerical_features:
    result = anderson(df[feature])
    print(f"Anderson-Darling test for {feature}: Statistic={result.statistic}, Critical Values={result.critical_values}, Significance Levels={alpha_levels}")
    print(f"Conclusion: {'Normal' if result.statistic < result.critical_values[2] else 'Not Normal'}\n")

#BOXCOX
transformed_df = pd.DataFrame()

# Loop through numerical features and perform the Box-Cox transformation
for feature in numerical_features:
    transformed_data, lambda_value = boxcox(df[feature] + 1)  # Adding 1 to handle zero values
    transformed_df[feature] = transformed_data

# Display the first few observations of the transformed dataset
print("Transformed Dataset:")
print(transformed_df.head())

#HeatMap
# Calculate the Pearson correlation matrix
correlation_matrix = df[numerical_features].corr()

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Create a heatmap using seaborn
sns.heatmap(correlation_matrix,  cmap="coolwarm", fmt=".2f", linewidths=.5)
for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix.columns)):
        coeff_value = correlation_matrix.iloc[i, j]
        plt.text(j + 0.5, i + 0.5, f"{coeff_value:.2f}", ha='center', va='center', color='black')
# Display the heatmap
plt.title("Pearson Correlation Coefficient Heatmap")
plt.show()

# Create a scatter plot matrix using seaborn
scatter_plot_matrix = sns.pairplot(df[numerical_features])

# Display the scatter plot matrix
plt.suptitle("Scatter Plot Matrix")
plt.show()