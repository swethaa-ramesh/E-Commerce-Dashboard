import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Read your CSV file
df = pd.read_csv("ecommerce_customer_data_large.csv")

# Get unique payment methods for dropdown options
payment_methods = df['Payment Method'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Payment Analysis Layout with Dropdown
app.layout = html.Div(style={'background-color': '#f8f9fa', 'padding': '20px'}, children=[
    html.H1("Payment Analysis", style={'color': '#007BFF', 'text-align': 'center'}),

    # Dropdown for selecting specific payment methods (multi=True for multiple selections)
    html.Div([
        dcc.Dropdown(
        id='payment-method-dropdown',
        options=[{'label': method, 'value': method} for method in payment_methods],
        value=[payment_methods[0]],  # Default value (can be a list)
        multi=True,
        
    ),
    ],style={'width':'30%','margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto','box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
    

    # Grid layout for charts
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'}, children=[
        # Pie chart showing the percentage of the selected payment methods
        dcc.Graph(id='payment-pie-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                 'border': '1px solid #ced4da', 'border-radius': '5px'}),

        # Bar chart with payment methods on X-axis, average purchase amount on Y-axis
        dcc.Graph(id='average-purchase-bar-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                         'border': '1px solid #ced4da', 'border-radius': '5px'}),
    ]),

    # Scatter plot with payment methods on X-axis, product category/price on Y-axis
    dcc.Graph(id='correlation-scatter-plot', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                     'border': '1px solid #ced4da', 'border-radius': '5px',
                                                     'margin-top': '20px'}),
])

# Callback to update graphs based on dropdown selection
@app.callback(
    [Output('payment-pie-chart', 'figure'),
     Output('average-purchase-bar-chart', 'figure'),
     Output('correlation-scatter-plot', 'figure')],
    [Input('payment-method-dropdown', 'value')]
)
def update_graphs(selected_payment_methods):
    # Filter data based on selected payment methods
    filtered_df = df[df['Payment Method'].isin(selected_payment_methods)]

    # Pie chart showing the percentage of the selected payment methods
    pie_chart = px.pie(filtered_df, names='Payment Method', title=f'Distribution of Selected Payments',
                       color_discrete_sequence=px.colors.qualitative.Set1)
    pie_chart.update_layout(title_x=0.5)
    # Bar chart with payment methods on X-axis, average purchase amount on Y-axis
    bar_chart = px.histogram(filtered_df, x='Total Purchase Amount',
                               title='Distribution of Total Purchase Amount for Selected Payments',
                               color='Payment Method', color_discrete_sequence=px.colors.qualitative.Set2,
                               marginal='rug',  # Add marginal rug plots for better visibility
                               template="plotly_dark")
    bar_chart.update_layout(title_x=0.5,bargap=0.1)
    # Scatter plot with payment methods on X-axis, product category/price on Y-axis
    scatter_plot = px.scatter(filtered_df, x='Payment Method', y='Product Price', color='Product Category',
                              title='Correlation between Selected Payments and Product Category/Price',
                              color_discrete_sequence=px.colors.qualitative.Set3)
    scatter_plot.update_layout(title_x=0.5)

    return pie_chart, bar_chart, scatter_plot

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
