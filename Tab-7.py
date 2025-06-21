import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import random

# Load dataset
df = pd.read_csv("ecommerce_customer_data_large.csv")

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(style={'backgroundColor': '#f4f4f4', 'padding': '20px', 'font-family': 'Arial, sans-serif'},children=[
    html.H1("E-commerce Dashboard", style={'color': '#007BFF', 'text-align': 'center'}),  # Set header color and center text
    
    html.Div([
        # Dropdown for selecting time period
        dcc.Dropdown(
            id='time-period-dropdown',
            options=[
                {'label': 'Monthly', 'value': 'M'},
                {'label': 'Weekly', 'value': 'W'}
            ],
            value='M',  # Default value
              # Add drop shadow and outline
                ),
            ],style={'width': '20%', 'margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto','text-align': 'center','box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px' }),
                
         html.Div([
        # Radio button for selecting product category
        dcc.RadioItems(
            id='product-category-radio',
            options=[
                {'label': category, 'value': category}
                for category in df['Product Category'].unique()
            ],
            value=df['Product Category'].unique()[0],  # Default value
            labelStyle={'display': 'block', 'margin-bottom': '10px'}  # Add margin
        ),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
              }),  # Center dropdown and radio items
    
    html.Div([
        # Graph for total sales over time
        dcc.Graph(id='total-sales-graph', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
    
        # Graph for seasonal patterns in selected product category sales
        dcc.Graph(id='product-category-sales-graph', style={'box-shadow': '0 8px 16px rgba rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
    
        # Graph for trends in returns over time
        dcc.Graph(id='returns-over-time-graph', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'})
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'grid-gap': '20px', 'margin': '20px'}),  # Use grid layout
    
])  # Set background color and padding for the entire page

# Define callbacks for updating graphs
@app.callback(
    Output('total-sales-graph', 'figure'),
    Output('product-category-sales-graph', 'figure'),
    Output('returns-over-time-graph', 'figure'),
    Input('time-period-dropdown', 'value'),
    Input('product-category-radio', 'value')
)
def update_graphs(selected_time_period, selected_category):
    # Filter data based on selected product category
    filtered_df = df[df['Product Category'] == selected_category]

    # a. Monthly or weekly trends in total sales
    total_sales_fig = px.line(filtered_df, x='Purchase Date', y='Total Purchase Amount', 
                              labels={'Total Purchase Amount': 'Total Sales'},
                              title=f'Trends in Total Sales ({selected_time_period})',
                              color_discrete_sequence=[px.colors.qualitative.Plotly[0]])
    total_sales_fig.update_layout(title_x=0.5)
    # b. Seasonal patterns in selected product category sales
    product_category_sales_fig = px.line(filtered_df, x='Purchase Date', y='Total Purchase Amount', 
                                         labels={'Total Purchase Amount': 'Total Sales'},
                                         title=f'Seasonal Patterns in {selected_category} Sales',
                                         color_discrete_sequence=[px.colors.qualitative.Plotly[1]])
    product_category_sales_fig.update_layout(title_x=0.5)
    # c. Trends in returns over time
    returns_over_time_fig = px.line(filtered_df, x='Purchase Date', y='Returns', 
                                     labels={'Returns': 'Count of Returns'},
                                     title=f'Trends in Returns Over Time ({selected_category})',
                                     color_discrete_sequence=[px.colors.qualitative.Plotly[2]])
    returns_over_time_fig.update_layout(title_x=0.5)

    return total_sales_fig, product_category_sales_fig, returns_over_time_fig

# Add additional CSS styling
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
