import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your dataset
df = pd.read_csv("ecommerce_customer_data_large.csv")
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the time intervals for the dropdown with full names
time_intervals = [
    # {'label': 'Daily', 'value': 'D'},
    {'label': 'Weekly', 'value': 'W'},
    {'label': 'Monthly', 'value': 'M'},
    {'label': 'Yearly', 'value': 'Y'}
]

# Layout of the dashboard
app.layout = html.Div(style={'background-color': '#f8f9fa', 'padding': '20px'}, children=[
    html.H1("Purchase Behavior Dashboard", style={'color': '#007BFF', 'text-align': 'center', 'margin-bottom': '20px'}),

    # Dropdown for selecting time intervals
    html.Div([
        dcc.Dropdown(
            id='time-interval-dropdown',
            options=time_intervals,
            value='M',
            
          # default selection is Monthly
        ),
    ], style={'width': '20%', 'margin-bottom': '20px', 'text-align': 'center',
              'font-family': 'Arial, sans-serif', 'font-weight': '600', 'font-size': '1rem', 'margin-left': '37rem',
              'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px',
              'background-color': '#f8f9fa', 'color': '#495057'}),

    # Loading indicator for the entire app layout
    dcc.Loading(
        id="loading",
        type="default",
        children=[
            # Grid layout for charts
            html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'}, children=[
                # Line chart for frequency distribution of purchase dates
                dcc.Graph(id='purchase-date-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                           'border': '1px solid #ced4da', 'border-radius': '5px',
                                                           'background-color': '#ffffff'}),

                # Bar chart for average quantity of products purchased
                dcc.Graph(id='average-quantity-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                               'border': '1px solid #ced4da', 'border-radius': '5px',
                                                               'background-color': '#ffffff'}),
            ]),

            # Grid layout for charts
            html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px', 'margin-top': '20px'}, children=[
                # Bar chart for most popular product categories and their average prices
                dcc.Graph(id='product-category-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                               'border': '1px solid #ced4da', 'border-radius': '5px',
                                                               'background-color': '#ffffff'}),

                # Histogram for distribution of total purchase amounts
                dcc.Graph(id='total-purchase-distribution', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                                   'border': '1px solid #ced4da', 'border-radius': '5px',
                                                                   'background-color': '#ffffff'}),
            ]),
        ]),
])

# Callbacks to update graphs based on dropdown selection
@app.callback(
    [Output('purchase-date-chart', 'figure'),
     Output('average-quantity-chart', 'figure'),
     Output('product-category-chart', 'figure'),
     Output('total-purchase-distribution', 'figure')],
    [Input('time-interval-dropdown', 'value')]
)
def update_graphs(selected_interval):
    # Frequency distribution of purchase dates
    df_resampled = df.set_index('Purchase Date').resample(selected_interval).count().reset_index()
    fig_purchase_date = px.line(df_resampled, x='Purchase Date', y='Customer ID', template='plotly_dark',title=f'Frequency Distribution of Purchase Dates ({[item["label"] for item in time_intervals if item["value"]==selected_interval][0]})', color_discrete_sequence=px.colors.qualitative.Vivid)

    # Average quantity of products purchased
    fig_average_quantity = px.bar(df_resampled, x='Purchase Date', y='Quantity',template='plotly_dark', title=f'Average Quantity of Products Purchased ({[item["label"] for item in time_intervals if item["value"]==selected_interval][0]})', color_discrete_sequence=px.colors.qualitative.Safe)  

    # Most popular product categories and their average prices
    df_category_grouped = df.groupby(pd.Grouper(key='Purchase Date', freq=selected_interval))['Product Category'].value_counts().unstack().fillna(0)
    fig_product_category = px.bar(df_category_grouped, barmode='stack', title=f'Distribution of Product Prices by Category ({[item["label"] for item in time_intervals if item["value"]==selected_interval][0]})', template='plotly_dark')

    # Scatter plot for total purchase amounts
    df_total_purchase_scatter = df.set_index('Purchase Date').resample(selected_interval).sum().reset_index()
    fig_total_purchase_distribution = px.scatter(df_total_purchase_scatter, x='Purchase Date', y='Total Purchase Amount',template='plotly_dark', title=f'Scatter Plot of Total Purchase Amounts ({[item["label"] for item in time_intervals if item["value"]==selected_interval][0]})', color_discrete_sequence= px.colors.qualitative.Light24)

    return fig_purchase_date, fig_average_quantity, fig_product_category, fig_total_purchase_distribution

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

