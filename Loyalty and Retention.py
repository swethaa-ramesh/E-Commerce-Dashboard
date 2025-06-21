import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Assume df is your DataFrame containing the data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)

# Convert Returns column to a more descriptive format for visualization
df['Returns'] = df['Returns'].map({0: 'No Return', 1: 'Returned'})

# Calculate transactions_per_customer and total_purchase_per_customer outside the callback
transactions_per_customer = df.groupby('Customer Name').size()
total_purchase_per_customer = df.groupby('Customer Name')['Total Purchase Amount'].sum()

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the web application
app.layout = html.Div([
    # Dropdown to select the analysis
    dcc.Dropdown(
        id='analysis-dropdown',
        options=[
            {'label': 'Transactions per Customer', 'value': 'transactions_per_customer'},
            {'label': 'Time Between Consecutive Purchases', 'value': 'time_between_purchases'},
            {'label': 'Total Purchase Amount by Churn Status', 'value': 'total_purchase_by_churn'},
            {'label': 'Potential Loyal Customers', 'value': 'potential_loyal_customers'}
        ],
        value='transactions_per_customer',
        style={'width': '50%'}
    ),

    # Graph will be displayed here
    dcc.Graph(id='analysis-graph'),
])

# Callback to update the graph based on the selected analysis
@app.callback(
    Output('analysis-graph', 'figure'),
    [Input('analysis-dropdown', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'transactions_per_customer':
        # 1. Average number of transactions per customer
        fig = px.histogram(transactions_per_customer, x=transactions_per_customer, title='Distribution of Number of Transactions Per Customer', labels={'x': 'Number of Transactions'})
    elif selected_analysis == 'time_between_purchases':
        # 2. Average time between consecutive purchases for a customer
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
        df_sorted = df.sort_values(['Customer Name', 'Purchase Date'])
        df_sorted['Time Between Purchases'] = df_sorted.groupby('Customer Name')['Purchase Date'].diff()
        average_time_between_purchases = df_sorted.groupby('Customer Name')['Time Between Purchases'].mean().dt.days
        fig = px.histogram(average_time_between_purchases, x=average_time_between_purchases, title='Average Time Between Consecutive Purchases (in days)', labels={'x': 'Days'})
    elif selected_analysis == 'total_purchase_by_churn':
        # 3. Correlation between total purchase amount and churn
        fig = px.histogram(df, x='Total Purchase Amount', color='Churn', nbins=20, title='Total Purchase Amount by Churn Status', labels={'x': 'Total Purchase Amount', 'color': 'Churn'})
        fig.update_layout(bargap=0.2)
    elif selected_analysis == 'potential_loyal_customers':
        # 4. Identify potential loyal customers based on frequency and amount of purchases
        loyal_threshold_transactions = transactions_per_customer.quantile(0.75)
        loyal_threshold_purchase = total_purchase_per_customer.quantile(0.75)
        potential_loyal_customers = df.groupby('Customer Name').filter(lambda x: len(x) > loyal_threshold_transactions and x['Total Purchase Amount'].sum() > loyal_threshold_purchase)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=potential_loyal_customers['Customer Name'].unique(), y=[1] * len(potential_loyal_customers['Customer Name'].unique()), mode='markers', marker=dict(size=10), text=potential_loyal_customers['Customer Name'].unique()))
        fig.update_layout(title='Potential Loyal Customers', showlegend=False)

    return fig



# Run the web application
if __name__ == '__main__':
    app.run_server(debug=True)
