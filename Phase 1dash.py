import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import plotly.express as px
import scipy.stats as stats
from mpl_toolkits.mplot3d import Axes3D
from prettytable import PrettyTable
from scipy.stats import boxcox
from scipy.stats import anderson
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

df = pd.read_csv('ecommerce_customer_data_large.csv')
# print(df.shape)
# print(df.info())
# print(df.describe().round(2))
missing_values = df.isnull().sum()
# print("Missing Values(before cleaning) are :")
# print(missing_values)
# Remove duplicates
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
# Replace missing 'Returns' values with a suitable default value, e.g., 0 for no return
default = 0
df['Returns'].fillna(default, inplace=True)
# print("Missing Values (after cleaning) are :")
# print(df.isnull().sum())
df['Total Purchase Amount'] = df['Product Price'] * df['Quantity']
# Drop unnecessary columns
df.drop(['Customer Name'], axis=1, inplace=True)
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
df.set_index('Purchase Date', inplace=True)
# print top 5 records
# print(df.head())
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
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix,  cmap="coolwarm", fmt=".2f", linewidths=.5)
for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix.columns)):
        coeff_value = correlation_matrix.iloc[i, j]
        plt.text(j + 0.5, i + 0.5, f"{coeff_value:.2f}", ha='center', va='center', color='black')
plt.title("Pearson Correlation Coefficient Heatmap")
plt.show()

# Create a scatter plot matrix using seaborn
scatter_plot_matrix = sns.pairplot(df[numerical_features])
plt.suptitle("Scatter Plot Matrix")
plt.show()

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

app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("E-commerce Data Visualization"),
    
    # Dropdown menu for selecting the graph
    dcc.Dropdown(
        id='graph-selector', # 
        options=[
            {'label': 'Line plot', 'value': 'line-plot'},
            {'label': 'stackbar plot', 'value': 'stack-bar-plot'},
            {'label': 'Group bar plot', 'value': 'Group-bar-plot'},
            {'label': 'Count plot', 'value': 'Count-plot'},
            {'label': 'Pie chart', 'value': 'pie-chart'},
            {'label': 'Dist plot', 'value': 'Dist-plot'},
            {'label': 'Pair plot', 'value': 'Pair-plot'},
            {'label': 'Heatmap', 'value': 'Heatmap'},
            {'label': 'Histogram with kde', 'value': 'Histogram-with-kde'},
            {'label': 'QQ Plot', 'value': 'QQ-Plot'},
            {'label': 'kde plot', 'value': 'kde-plot'},
            {'label': 'Implot', 'value': 'Implot'},
            {'label': 'Multivariate Box Plot', 'value': 'Multivariate-Box-Plot'},
            {'label': 'Area-Graph', 'value': 'Area-Graph'},
            {'label': 'Violin Plot', 'value': 'Violin-Plot'},
            {'label': 'Joint Plot', 'value': 'Joint-Plot'},
            {'label': 'Rug Plot', 'value': 'Rug-Plot'},
            {'label': '3D Plot', 'value': '3D-Plot'},
            {'label': 'Contour Plot', 'value': 'Contour-Plot'},
            {'label': 'Hexbin plot', 'value': 'Hexbin-plot'},
            {'label': 'Cluster Map', 'value': 'Cluster-map'},
            {'label': 'Strip Plot', 'value': 'Strip-Plot'},
            {'label': 'Swarm Plot', 'value': 'Swarm-Plot'},
        ],
        value='line-plot',  
        style={'width': '50%'}
    ),
    
    # Container for displaying the selected graph
    dcc.Graph(id='selected-graph'),
])

# Define callback to update the graph based on the selected option
@app.callback(
    Output('selected-graph', 'figure'),
    [Input('graph-selector', 'value')]
)
def update_graph(selected_graph):
    if selected_graph == 'line-plot':
        monthly_purchase = df.resample('M')['Total Purchase Amount'].sum().reset_index()
        fig = px.line(monthly_purchase, x='Purchase Date', y='Total Purchase Amount', markers=True, line_shape='linear',
                    labels={'Purchase Date': 'Month', 'Total Purchase Amount': 'Total Purchase Amount'},
                    title='Monthly Total Purchase Amount')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    
    elif selected_graph == 'stack-bar-plot':
        # Stack bar plot
        gender_category_counts = df.groupby(['Gender', 'Product Category']).size().unstack().reset_index()
        fig = px.bar(gender_category_counts, x='Gender', y=[col for col in gender_category_counts.columns if col != 'Gender'],
                    barmode='stack', labels={'value': 'Number of Purchases', 'variable': 'Product Category'},
                    title='Product Category Purchase Count by Gender')
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        
        return fig
    elif selected_graph == 'Group-bar-plot':
        grouped_data = df.groupby(['Product Category', 'Gender'])['Total Purchase Amount'].sum().unstack().reset_index()
        fig = px.bar(grouped_data, x='Product Category', y=[col for col in grouped_data.columns if col != 'Product Category'],
                    barmode='group', labels={'value': 'Total Purchase Amount', 'variable': 'Gender'},
                    title='Total Purchase Amount by Product Category and Gender')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
                                                
        return fig
    elif selected_graph == 'Count-plot':
        # Count plot
        fig = px.histogram(df, x='Product Category', labels={'Product Category': 'Product Category', 'count': 'Count'},
                        title='Distribution of Product Categories Purchased')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'pie-chart':
        # Update the pie chart
        payment_method_counts = df['Payment Method'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(payment_method_counts, labels=payment_method_counts.index, autopct='%1.2f%%', startangle=90, colors=sns.color_palette('pastel'))
        plt.title('Payment Method Distribution',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.show()
        return px.line()
    elif selected_graph == 'Dist-plot':
        plt.figure(figsize=(8, 6))
        sns.histplot(df['Customer Age'], kde=True, color='skyblue')
        plt.title('Distribution of Customer Ages',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.xlabel('Customer Age',fontname='serif', color='darkred', fontsize=14)
        plt.ylabel('Density',fontname='serif', color='darkred', fontsize=14)
        plt.show()
        return px.line()
    elif selected_graph == 'Pair-plot':
        # Pair plot
        sns.set(style="whitegrid")
        sns.pairplot(df, vars=['Product Price','Quantity','Total Purchase Amount'], hue='Churn')
        plt.suptitle('Pair Plot for Selected Columns', y=1.02)
        plt.show()
        return px.line()
    elif selected_graph =='Heatmap':
        #Heatmap
       numeric_df = df.select_dtypes(include=['float64', 'int64'])
       correlation_matrix = numeric_df.corr()
       plt.figure(figsize=(10, 8))
       sns.heatmap(correlation_matrix, cmap='coolwarm')
       for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix.columns)):
                text = f"{correlation_matrix.iloc[i, j]:.2f}"
                plt.text(j + 0.5, i + 0.5, text, ha='center', va='center', color='black', fontsize=12)
       
       plt.title('Heat Map: Correlation Matrix', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
       plt.show()
       return px.line()
    elif selected_graph =='Histogram-with-kde':
        #Histogram with kde
        plt.figure(figsize=(8, 6))
        sns.histplot(df['Total Purchase Amount'], kde=True, color='skyblue')
        plt.title('Histogram Plot with KDE',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.xlabel( 'Total Purchase Amount',fontname='serif', color='darkred')
        plt.ylabel( 'Count',fontname='serif', color='darkred')
        plt.show()
        return px.line()
    elif selected_graph =='QQ-Plot':
        # QQ-Plot
        sm.qqplot(df['Product Price'], line='s')
        plt.title('QQ-Plot',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.xlabel('Theoritical quantity',fontname='serif', color='darkred')
        plt.ylabel('Sample quantity', fontname='serif', color='darkred')
        plt.show()
        return px.line()
    elif selected_graph == 'kde-plot':
        # kde plot
        plt.figure(figsize=(8, 6))
        sns.kdeplot(df['Quantity'], fill=True, alpha=0.6, palette="viridis", linewidth=3)
        plt.title('KDE Plot with Filled Area',fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.xlabel("Quality", fontname='serif', color='darkred')
        plt.ylabel('Density', fontname='serif', color='darkred')
        plt.show()
    elif selected_graph == 'Implot' :
        #Implot
        fig = px.scatter(df, x='Customer Age', y='Total Purchase Amount', trendline='ols',
                 title='lmplot: Total Purchase Amount vs. Customer Age')
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Multivariate-Box-Plot':
        fig = px.box(df, x='Product Category', y='Customer Age', color='Gender',
             title='Multivariate Box Plot: Customer Age by Product Category (Color-coded by Gender)')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Area-Graph':
        monthly_purchase = df.resample('M')['Total Purchase Amount'].sum().reset_index()
        fig = px.area(monthly_purchase, x='Purchase Date', y='Total Purchase Amount',
              labels={'Purchase Date': 'Month', 'Total Purchase Amount': 'Total Purchase Amount'},
              title='Area Graph - Monthly Purchase Trends')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Violin-Plot':
        fig = px.violin(df, x='Product Category', y='Customer Age', color='Gender',
                title='Violin Plot: Customer Age by Product Category (Color-coded by Gender)')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Joint-Plot':
        #Joint Plot with KDE and Scatter Representation:
        sns.set(style="whitegrid")
        sns.jointplot(x='Customer Age', y='Total Purchase Amount', data=df, color='g')
        sns.kdeplot(df['Customer Age'], color='b', ax=plt.gca())
        sns.kdeplot(df['Total Purchase Amount'], color='r', vertical=True, ax=plt.gca())
        plt.suptitle('Joint Plot with KDE: Customer Age vs. Total Purchase Amount', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.show()
        return px.line()
    elif selected_graph == 'Rug-Plot':
        fig = px.scatter(df, x='Product Price', marginal_y='rug',
                 title='Rug Plot: Product Price Distribution')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == '3D-Plot':
        fig = px.scatter_3d(df, x='Customer Age', y='Product Price', z='Total Purchase Amount',title='3D Plot: Customer Age, Product Price, and Total Purchase Amount')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Contour-Plot':
        fig = px.density_contour(df, x='Customer Age', y='Product Price',
                         title='Contour Plot: Customer Age vs. Product Price',)
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Cluster-map':
        #Cluster map
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_df.corr()
        sns.clustermap(numeric_df.corr(), cmap='coolwarm', annot=True, figsize=(10, 8))
        for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix.columns)):
                text = f"{correlation_matrix.iloc[i, j]:.2f}"
        plt.title('Cluster Map: Correlation Heatmap', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.show()
        return px.line()
    elif selected_graph == 'Hexbin-plot':
        # Hexbin plot
        plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
        plt.hexbin(df['Age'], df['Customer ID'], gridsize=50, cmap='viridis')
        plt.colorbar()
        plt.title('Hexbin Plot of Age vs Customer ID', fontdict={'fontname': 'serif', 'color': 'blue', 'size': 16})
        plt.xlabel('Age', fontdict={'fontname': 'serif', 'color': 'darkred'})
        plt.ylabel('Total Purchase Amount', fontdict={'fontname': 'serif', 'color': 'darkred'})
        plt.show()
        return px.line()
    elif selected_graph == 'Strip-Plot' :
        fig = px.strip(df, x='Gender', y='Total Purchase Amount', color='Gender',
               title='Strip Plot: Total Purchase Amount by Gender')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
    elif selected_graph == 'Swarm-Plot' :
        fig = px.scatter(df, x='Product Category', y='Customer Age', color='Gender', 
                 title='Swarm Plot: Customer Age by Product Category (Color-coded by Gender)',
                 render_mode='webgl', 
                 category_orders={'Product Category': ['Category A', 'Category B', 'Category C']}) 
        fig.update_xaxes(tickangle=45)
        fig.update_layout(font=dict(family='serif', color='blue', size=20))
        fig.update_layout(
            xaxis=dict(tickfont=dict(family='serif', color='darkred')),
            yaxis=dict(tickfont=dict(family='serif', color='darkred')),title_x=0.5
        )
        return fig
  
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)