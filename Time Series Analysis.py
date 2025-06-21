import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Assume df is your DataFrame containing the data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)

# Set 'Purchase Date' as the index
df.set_index('Purchase Date', inplace=True)

# Set up Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    # Tabs for different analyses
   
        
            # Dropdown to select time frequency
            html.Label('Select Time Frequency:'),
            dcc.Dropdown(
                id='time-frequency-dropdown',
                options=[
                    {'label': 'Monthly', 'value': 'M'},
                    {'label': 'Weekly', 'value': 'W'}
                ],
                value='M',  # Default: Monthly
                style={'width': '50%'}
            ),
            # Graph for sales trend
            dcc.Graph(id='sales-trend'),
      
        
            # Graph for seasonal patterns in product category sales
            dcc.Graph(id='seasonal-patterns'),
       
    
])

# Callback to update the graphs based on the selected time frequency
@app.callback(
    [Output('sales-trend', 'figure'),
     Output('seasonal-patterns', 'figure')],
    [Input('time-frequency-dropdown', 'value')]
)
def update_graphs(selected_frequency):
    # Monthly or weekly trends in total sales
    if selected_frequency == 'M':
        sales_trend = px.line(df.resample('M').sum(), x=df.resample('M').sum().index, y='Total Purchase Amount', labels={'x': 'Month', 'y': 'Total Sales'},
                              title='Monthly Sales Trend')
    else:
        sales_trend = px.line(df.resample('W').sum(), x=df.resample('W').sum().index, y='Total Purchase Amount', labels={'x': 'Week', 'y': 'Total Sales'},
                              title='Weekly Sales Trend')

    # Seasonal patterns in product category sales
    monthly_product_sales = df.groupby([df.index.month, 'Product Category']).size().unstack()
    seasonal_patterns = px.line(monthly_product_sales, x=monthly_product_sales.index, y=monthly_product_sales.columns,
                                labels={'x': 'Month', 'y': 'Number of Sales'}, title='Monthly Sales Count by Product Category')

    return sales_trend, seasonal_patterns

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
