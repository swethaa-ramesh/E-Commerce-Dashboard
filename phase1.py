import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as stats
from mpl_toolkits.mplot3d import Axes3D
df = pd.read_csv('ecommerce_customer_data_large.csv')
print(df.shape)
print(df.info())
print(df.describe().round(2))
missing_values = df.isnull().sum()
print("Missing Values(before cleaning) are :")
print(missing_values)
# Remove duplicates
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
# Replace missing 'Returns' values with a suitable default value, e.g., 0 for no return
default = 0
df['Returns'].fillna(default, inplace=True)
print("Missing Values (after cleaning) are :")
print(df.isnull().sum())
df['Total Purchase Amount'] = df['Product Price'] * df['Quantity']
# Drop unnecessary columns
df.drop(['Customer Name'], axis=1, inplace=True)
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
df.set_index('Purchase Date', inplace=True)
# print top 5 records
print(df.head())

# Line plot
# Resample data to get monthly total purchase amount
monthly_purchase = df.resample('M')['Total Purchase Amount'].sum()
plt.figure(figsize=(10, 6))
plt.plot(monthly_purchase.index, monthly_purchase.values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
plt.xlabel('Month',fontname='serif', color='darkred')
plt.ylabel('Total Purchase Amount',fontname='serif', color='darkred')
plt.title('Monthly Total Purchase Amount',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Stack bar plot
gender_category_counts = df.groupby(['Gender', 'Product Category']).size().unstack()
gender_category_counts.plot(kind='bar', stacked=True)
plt.xlabel('Gender',fontname='serif', color='darkred', fontsize=14)
plt.ylabel('Number of Purchases',fontname='serif', color='darkred', fontsize=14)
plt.title('Product Category Purchase Count by Gender',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xticks(rotation=0)
plt.show()

# Group bar plot
grouped_data = df.groupby(['Product Category', 'Gender'])['Total Purchase Amount'].sum().unstack()
grouped_data.plot(kind='bar', width=0.8, colormap='Set2')
plt.title('Total Purchase Amount by Product Category and Gender', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xlabel('Product Category' , fontsize=14,fontname='serif', color='darkred')
plt.ylabel('Total Purchase Amount', fontsize=14,fontname='serif', color='darkred')
plt.xticks(rotation=45)
plt.legend(title='Gender', loc='upper right')
plt.show()

# Count plot
plt.figure(figsize=(10, 6))
sns.countplot(x='Product Category', data=df, palette='viridis')
plt.title('Distribution of Product Categories Purchased', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xlabel('Product Category',fontname='serif', color='darkred', fontsize=14)
plt.ylabel('Count',fontname='serif', color='darkred', fontsize=14)
plt.xticks(rotation=45)
plt.show()

# Pie chart
payment_method_counts = df['Payment Method'].value_counts().reset_index()
plt.figure(figsize=(8, 8))
plt.pie(payment_method_counts, labels=payment_method_counts.index, autopct='%1.2f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Payment Method Distribution',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

# Dist plot
plt.figure(figsize=(8, 6))
sns.histplot(df['Customer Age'], kde=True, color='skyblue')
plt.title('Distribution of Customer Ages',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xlabel('Customer Age',fontname='serif', color='darkred', fontsize=14)
plt.ylabel('Density',fontname='serif', color='darkred', fontsize=14)
plt.show()

# pair plot
sns.set(style="whitegrid")
sns.pairplot(df, vars=['Product Price','Quantity','Total Purchase Amount'], hue='Churn')
plt.suptitle('Pair Plot for Selected Columns', y=1.02)
plt.show()

#  Heatmap
sns.set(style="whitegrid")
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", cbar=True)
plt.title('Heatmap with Color Bar',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Histogram with kde
plt.figure(figsize=(8, 6))
sns.histplot(df['Total Purchase Amount'], kde=True, color='skyblue')
plt.title('Histogram Plot with KDE',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

# QQ-Plot
sm.qqplot(df['Product Price'], line='s')
plt.title('QQ-Plot',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

# kde plot
plt.figure(figsize=(8, 6))
sns.kdeplot(df['Quantity'], fill=True, alpha=0.6, palette="viridis", linewidth=3)
plt.title('KDE Plot with Filled Area',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xlabel("Quality", fontname='serif', color='darkred')
plt.ylabel('Density', fontname='serif', color='darkred')
plt.show()


# lm or reg plot
x = 'Customer Age'
y = 'Total Purchase Amount'
sns.set(style="whitegrid")  # Set the plot style
sns.lmplot(x=x, y=y, data=df, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
plt.title(f'lmplot: {y} vs. {x}', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Multivariate Box Plot
sns.boxplot(x='Product Category', y='Customer Age', hue='Gender', data=df)
plt.title('Multivariate Box Plot: Customer Age by Product Category (Color-coded by Gender)',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

# Area plot
monthly_purchase = df.resample('M')['Total Purchase Amount'].sum()
monthly_purchase.plot(kind='area', stacked=False, alpha=0.5, figsize=(10, 6))
plt.xlabel('Month', fontname='serif', color='darkred')
plt.ylabel('Total Purchase Amount', fontname='serif', color='darkred')
plt.title('Monthly Purchase Trends',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Violin plot
sns.violinplot(x='Product Category', y='Customer Age', hue='Gender', data=df, split=True, inner='quart')
plt.title('Violin Plot: Customer Age by Product Category (Split by Gender)',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Joint Plot with KDE and Scatter Representation:
sns.jointplot(x='Customer Age', y='Total Purchase Amount', data=df, kind='kde', color='g')
plt.suptitle('Joint Plot: Customer Age vs. Total Purchase Amount',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Rug plot
sns.rugplot(df['Product Price'])
plt.xlabel('Product Price', fontname='serif', color='darkred')
plt.title('Rug Plot: Product Price Distribution',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['Customer Age'], df['Product Price'], df['Total Purchase Amount'], c='b', marker='o')
ax.set_xlabel('Customer Age', fontname='serif', color='darkred')
ax.set_ylabel('Product Price', fontname='serif', color='darkred')
ax.set_zlabel('Total Purchase Amount', fontname='serif', color='darkred')
plt.title('3D Plot: Customer Age, Product Price, and Total Purchase Amount',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Contour plot
plt.figure(figsize=(8, 6))
sns.kdeplot(data=df, x='Customer Age', y='Product Price', cmap='viridis', shade=True, cbar=True)
plt.xlabel('Customer Age')
plt.ylabel('Product Price')
plt.title('KDE Plot: Customer Age vs. Product Price')
plt.show()

#Cluster map
sns.clustermap(df.corr(), cmap='coolwarm', annot=True, figsize=(10, 8))
plt.title('Cluster Map: Correlation Heatmap',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

# Hexbin plot
sns.jointplot(x='Customer Age', y='Total Purchase Amount', data=df, kind='hex', color='b')
plt.suptitle('Hexbin Plot: Customer Age vs. Total Purchase Amount',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

#Strip plot
sns.stripplot(x='Gender', y='Total Purchase Amount', data=df, jitter=True, palette='Set2')
plt.title('Strip Plot: Total Purchase Amount by Gender',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()

# Swarm plot
sns.swarmplot(x='Product Category', y='Customer Age', data=df, hue='Gender', palette='Set2', dodge=True)
plt.xlabel('Product Category', fontname='serif', color='darkred')
plt.ylabel('Customer Age', fontname='serif', color='darkred')
plt.title('Swarm Plot: Customer Age by Product Category (Color-coded by Gender)',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.legend(title='Gender', loc='upper right')
plt.xticks(rotation=45)
plt.show()


# Subplots
# Plot 1: Average Purchase Amount by Product Category (Bar Plot)
plt.figure(figsize=(10, 6))
average_purchase_by_category = df.groupby('Product Category')['Total Purchase Amount'].mean()
average_purchase_by_category.plot(kind='bar', color='skyblue')
plt.xlabel('Product Category', fontsize=14, fontname='serif', color='darkred')
plt.ylabel('Average Purchase Amount', fontsize=14, fontname='serif', color='darkred')
plt.title('Average Purchase Amount by Product Category', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xticks(rotation=45)
plt.show()

# Plot 2: Purchase Frequency by Gender (Count Plot)
plt.figure(figsize=(8, 6))
sns.countplot(x='Gender', data=df, palette='pastel')
plt.title('Purchase Frequency by Gender', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xlabel('Gender', fontsize=14, fontname='serif', color='darkred')
plt.ylabel('Purchase Frequency', fontsize=14, fontname='serif', color='darkred')
plt.show()

# Plot 3: Payment Method Preference by Age Group (Stacked Bar Plot)
age_bins = [0, 18, 35, 50, 100]
age_labels = ['<18', '18-35', '36-50', '50+']
df['Age Group'] = pd.cut(df['Customer Age'], bins=age_bins, labels=age_labels)
payment_method_by_age_group = df.groupby(['Age Group', 'Payment Method']).size().unstack()
payment_method_by_age_group.plot(kind='bar', stacked=True, colormap='Set2', figsize=(10, 6))
plt.xlabel('Age Group', fontsize=14, fontname='serif', color='darkred')
plt.ylabel('Number of Purchases', fontsize=14, fontname='serif', color='darkred')
plt.title('Payment Method Preference by Age Group', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.xticks(rotation=0)
plt.show()

# Plot 4: Customer Churn by Product Category (Pie Chart)
churn_by_category = df.groupby('Product Category')['Churn'].sum()
plt.figure(figsize=(8, 8))
plt.pie(churn_by_category, labels=churn_by_category.index, autopct='%1.2f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Customer Churn by Product Category', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
plt.show()
