import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_csv("ecommerce_customer_data_large.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("E-commerce Dashboard", style={'color': '#007BFF', 'text-align': 'center', 'margin-bottom': '20px'}),  # Set header color and center text
    html.Div([
         # Dropdown for selecting the analysis type
    dcc.Dropdown(
        id='analysis-type',
        options=[
            {'label': 'Average Transactions per Customer', 'value': 'avg_transactions'},
            {'label': 'Average Time Between Consecutive Purchases', 'value': 'avg_time_between_purchases'},
            {'label': 'Correlation between Total Purchase Amount and Churn', 'value': 'correlation'},
            {'label': 'Identify Potential Loyal Customers', 'value': 'loyal_customers'}
        ],
        value='avg_transactions',
        ),
           ],style={'width': '30%', 'margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto',
            'text-align': 'center',
            'font-family': 'Arial, sans-serif',
            'font-weight': '600',
            'font-size': '1rem', 'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
   
    html.Div([
         # Placeholder for the selected analysis result
        dcc.Graph(id='analysis-result', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px',})
    ]),
],style={'backgroundColor': '#f4f4f4', 'padding': '20px', 'font-family': 'Arial, sans-serif','height':'90vh'})

# Define callback to update the graph based on user input
@app.callback(
    Output('analysis-result', 'figure'),
    [Input('analysis-type', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'avg_transactions':
        # Calculate average transactions per customer
        avg_transactions = df.groupby('Customer ID')['Purchase Date'].count().mean()

        # Create a simple bar chart
        fig = px.bar(x=['Average Transactions per Customer'], y=[avg_transactions], title='Average Transactions per Customer', color_discrete_sequence=[px.colors.qualitative.Plotly[0]])
        fig.update_layout(title_x=0.5)

    elif selected_analysis == 'avg_time_between_purchases':
        # Calculate average time between consecutive purchases
        # (You'll need to adjust this based on your specific date columns)
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
        df['Time Between Purchases'] = df.groupby('Customer ID')['Purchase Date'].diff().mean()

        # Create a histogram
        fig = px.histogram(df, x='Time Between Purchases', nbins=50, title='Average Time Between Consecutive Purchases', color_discrete_sequence=[px.colors.qualitative.Plotly[1]])
        fig.update_layout(title_x=0.5)
    elif selected_analysis == 'correlation':
        # Calculate correlation between total purchase amount and churn
        # (You'll need to adjust this based on your specific columns)
        fig = px.scatter(df, x='Total Purchase Amount', y='Churn', title='Correlation between Total Purchase Amount and Churn', color_discrete_sequence=[px.colors.qualitative.Plotly[2]])
        fig.update_layout(title_x=0.5)

    elif selected_analysis == 'loyal_customers':
        # Identify potential loyal customers
        threshold_frequency = 3  # Define your threshold for purchase frequency
        threshold_amount = 1000  # Define your threshold for total purchase amount

        loyal_customers = df.groupby('Customer ID').agg({'Total Purchase Amount': 'sum', 'Purchase Date': 'count'})
        loyal_customers = loyal_customers[(loyal_customers['Total Purchase Amount'] > threshold_amount) & (loyal_customers['Purchase Date'] > threshold_frequency)]

        # Create a scatter plot or table
        fig = px.scatter(loyal_customers, x='Total Purchase Amount', y='Purchase Date', title='Identify Potential Loyal Customers', color_discrete_sequence=[px.colors.qualitative.Plotly[3]])
        fig.update_layout(title_x=0.5)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
