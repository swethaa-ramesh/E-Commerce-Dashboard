import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import seaborn as sns

# Assuming df is your DataFrame with the payment data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)


app = dash.Dash(__name__)

# Dropdown for analysis selection
analysis_dropdown = dcc.Dropdown(
    id='Payment-dropdown',
    options=[
        {'label': 'Distribution of payment methods', 'value': 'payment_distribution'},
        {'label': 'Average purchase amount by payment method', 'value': 'average_purchase'},
        {'label': 'Correlation between payment method and product category or price', 'value': 'correlation_plot'}
    ],
    value='payment_distribution',  # Default selection
    multi=False
)

# Default figures
payment_distribution_fig = px.histogram(df, x='Payment Method', title='Distribution of Payment Methods Used by Customers')
average_purchase_fig = px.scatter(df, x='Payment Method', y='Total Purchase Amount', title='Average Purchase Amount by Payment Method')  # Changed to scatter plot
correlation_fig = px.box(df, x='Payment Method', y='Product Price', color='Product Category',
                         title='Distribution of Product Prices by Payment Method and Product Category')

app.layout = html.Div(children=[
    html.H1("Payment Analysis"),
    
    html.Div([
        html.Label('Select Analysis:'),
        analysis_dropdown,
    ]),

    html.Div([
        dcc.Graph(id='Payment-plot'),
    ]),
])


# Callback to update the selected plot based on the dropdown value
@app.callback(
    dash.dependencies.Output('Payment-plot', 'figure'),
    [dash.dependencies.Input('Payment-dropdown', 'value')]
)
def update_selected_plot(selected_analysis):
    if selected_analysis == 'payment_distribution':
        return payment_distribution_fig
    elif selected_analysis == 'average_purchase':
        return average_purchase_fig
    elif selected_analysis == 'correlation_plot':
        return correlation_fig


if __name__ == '__main__':
    app.run_server(debug=True)