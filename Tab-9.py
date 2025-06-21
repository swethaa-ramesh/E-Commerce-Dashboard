import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Assuming you have already loaded your DataFrame 'df'
df = pd.read_csv("ecommerce_customer_data_large.csv")

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Customer Name Distribution", style={'color': '#007BFF', 'text-align': 'center'}),
    # First Row
    html.Div([
        # First Column - Dropdowns
      html.Div([
    html.Label("Select Customer:"),
    dcc.Dropdown(
        id='customer-dropdown1',
        options=[{'label': customer, 'value': customer} for customer in df['Customer Name'].unique()],
        value=[df['Customer Name'].unique()[0]],  # Set default value as a list with a single element
        multi=True,  # Allow multiple selections
        style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px','margin-bottom': '1rem'}
    ),
    html.Label("Select Product Category:"),
    dcc.Dropdown(
        id='product-category-dropdown1',
        options=[{'label': category, 'value': category} for category in df['Product Category'].unique()],
        value=[df['Product Category'].unique()[0]],  # Set default value as a list with a single element
        multi=True,  # Allow multiple selections
        style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
    ),
], className="four columns", style={'margin-top': '4rem', 'margin-right': '1rem'}),


        # Second Column - Scatter Chart
        html.Div([
            dcc.Graph(
                id='scatter-plot1',
                style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            )
        ], className="four columns", style={'margin-bottom': '1rem','margin-top': '2rem'}),

        # Third Column - Pie Chart
        html.Div([
            dcc.Graph(
                id='pie-chart1',
                style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            )
        ], className="four columns", style={'margin-bottom': '1rem','margin-top': '2rem'}),
    ], className="row", style={'display': 'grid', 'grid-template-columns': '15% 1fr 25%', 'gap': '20px'}),

    # Second Row
    html.Div([
        # Bar Graph
        html.Div([
            dcc.Graph(
                id='bar-chart1',
                style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            )
        ], className="twelve columns"),
    ], className="row", style={'display': 'grid', 'grid-template-columns': '1fr'}),
],style={'backgroundColor': '#f4f4f4', 'padding': '20px', 'font-family': 'Arial, sans-serif'})

# Define callback to update graphs based on dropdown selections
# Define callback to update graphs based on dropdown selections
@app.callback(
    [Output('scatter-plot1', 'figure'),
     Output('pie-chart1', 'figure'),
     Output('bar-chart1', 'figure')],
    [Input('customer-dropdown1', 'value'),
     Input('product-category-dropdown1', 'value')]
)
def update_graphs(selected_customers, selected_categories):
    # Handle multiple selections in the callback function
    filtered_df = df[
        (df['Customer Name'].isin(selected_customers)) &
        (df['Product Category'].isin(selected_categories))
    ]

    # Scatter Plot
    scatter_plot = px.scatter(filtered_df, x='Customer Age', y='Total Purchase Amount',  size='Quantity',title='Customer Age vs. Total Purchase Amount',color_discrete_sequence=[px.colors.qualitative.Dark24])
    scatter_plot.update_layout(
        plot_bgcolor='#f8f9fa',  # Background color
        paper_bgcolor='#f8f9fa',  # Plot area color
        font_color='#495057',  # Text color
        title_x=0.5
    )

    # Pie Chart
    pie_chart = px.pie(filtered_df, names='Payment Method', title='Payment Method Distribution')
    pie_chart.update_layout(
        plot_bgcolor='#f8f9fa',  # Background color
        paper_bgcolor='#f8f9fa',  # Plot area color
        font_color='#495057',  # Text color
        title_x=0.5
    )

    # Bar Chart
    bar_chart = px.bar(filtered_df, x='Purchase Date', y='Total Purchase Amount', title='Total Purchase Amount Over Time',color_discrete_sequence=[px.colors.qualitative.Prism])
    bar_chart.update_layout(
        plot_bgcolor='#f8f9fa',  # Background color
        paper_bgcolor='#f8f9fa',  # Plot area color
        font_color='#495057',  # Text color
        title_x=0.5
    )
    

    return scatter_plot, pie_chart, bar_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
