import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from dash.dash_table.Format import Group
import dash_table

# Assume df is your DataFrame containing the data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)

# Create a customer-level dataset with relevant metrics for segmentation
customer_data = df.groupby('Customer Name').agg({
    'Total Purchase Amount': ['sum', 'mean'],
    'Returns': 'sum',
    'Churn': 'max'
}).reset_index()
customer_data.columns = ['Customer Name', 'Total Purchases', 'Average Purchase Amount', 'Total Returns', 'Churn Status']

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_data[['Total Purchases', 'Average Purchase Amount', 'Total Returns', 'Churn Status']])

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
scaled_data_imputed = imputer.fit_transform(scaled_data)

# Dash web application
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    # Dropdown for selecting the number of clusters
    dcc.Dropdown(
        id='cluster-dropdown',
        options=[
            {'label': f'{n} Clusters', 'value': n} for n in range(2, 11)
        ],
        value=4,  # Default: 4 clusters
        style={'width': '50%'}
    ),

    # Scatter plot for customer segmentation
    dcc.Graph(
        id='customer-segmentation',
    ),

    # Table for cluster summary
    dash_table.DataTable(
        id='cluster-summary',
    ),
])

# Callback to update the graphs based on the selected number of clusters
@app.callback(
    [Output('customer-segmentation', 'figure'),
     Output('cluster-summary', 'columns'),
     Output('cluster-summary', 'data')],
    [Input('cluster-dropdown', 'value')]
)
def update_graph(num_clusters):
    # Apply KMeans clustering with the selected number of clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    customer_data['Cluster'] = kmeans.fit_predict(scaled_data_imputed)

    # Cluster summary
    cluster_summary = customer_data.groupby('Cluster').agg({
        'Total Purchases': 'mean',
        'Average Purchase Amount': 'mean',
        'Total Returns': 'mean',
        'Churn Status': 'mean'
    }).reset_index()

    # Scatter plot
    fig = px.scatter(
        customer_data,
        x='Total Purchases',
        y='Average Purchase Amount',
        color='Cluster',
        title=f'Customer Segmentation ({num_clusters} Clusters)',
    )

    return fig, [{'name': col, 'id': col} for col in cluster_summary.columns], cluster_summary.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
