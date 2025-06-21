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
    # Customer Dropdown
    html.Div([
        html.Label("Select Customer ID:"),
        dcc.Dropdown(
            id='customer-dropdown2',
            options=[{'label': customer, 'value': customer} for customer in df['Customer ID'].unique()],
            value=df['Customer ID'].unique()[0],
            style={'width': '50%','margin-left':'18rem'}
        ),
    ], style={'margin': '20px','text-align':'center'}),

    # Dashboards
    html.Div([
        # Scatter Plot
        dcc.Graph(
            id='scatter-plot2',
            style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'},
        ),

        # Bar Chart
        dcc.Graph(
            id='bar-chart2',
            style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'},
        ),

        # Line Chart
        dcc.Graph(
            id='line-chart2',
            style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'},
        ),

        # Pie Chart
        dcc.Graph(
            id='pie-chart2',
            style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'},
        ),
    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '20px', 'margin': '20px'}),
])

# Define callback to update graphs based on dropdown selections
@app.callback(
    [Output('scatter-plot2', 'figure'),
     Output('bar-chart2', 'figure'),
     Output('line-chart2', 'figure'),
     Output('pie-chart2', 'figure')],
    [Input('customer-dropdown2', 'value')]
)
def update_dashboard(selected_customer):
    # Filter DataFrame based on selected customer
    filtered_df = df[df['Customer ID'] == selected_customer]

    # Scatter Plot
    scatter_plot = px.scatter(filtered_df, x='Customer Age', y='Total Purchase Amount', color='Gender',
                              size='Quantity', title=f"Customer {selected_customer} - Age vs. Total Purchase Amount")

    # Bar Chart
    bar_chart = px.bar(filtered_df, x='Product Category', y='Total Purchase Amount', color='Product Category',
                       title=f"Customer {selected_customer} - Purchase Amount by Product Category")

    # Line Chart
    line_chart = px.line(filtered_df, x='Purchase Date', y='Total Purchase Amount', color='Product Category',
                         title=f"Customer {selected_customer} - Purchase Amount Over Time")

    # Pie Chart
    pie_chart = px.pie(filtered_df, names='Payment Method',
                       title=f"Customer {selected_customer} - Payment Method Distribution")

    # Update layout for all charts
    for chart in [scatter_plot, bar_chart, line_chart, pie_chart]:
        chart.update_layout(
            plot_bgcolor='#f8f9fa',  # Background color
            paper_bgcolor='#f8f9fa',  # Plot area color
            font_color='#495057',  # Text color
        )

    return scatter_plot, bar_chart, line_chart, pie_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
