import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv("ecommerce_customer_data_large.csv")

# Set color scheme
colors = {
    'background': '#f8f9fa',  # Light gray background
    'text': '#495057',  # Dark gray text
    'accent': '#007BFF'  # Blue accent color
}

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    html.H1("Churn Rate Dashboard", style={'color': colors['accent'], 'text-align': 'center'}),

    # Grid layout
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px', 'margin-top': '20px'}, children=[
        # Left corner: Pie chart displaying churn rate
        html.Div([
            html.Div(style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '20px','margin-bottom': '20px'}, children=[
                html.Div([
                    html.Label("Total Number of Customers", style={'color': colors['text'], 'font-size': '1.5rem'}),
                    html.Div(len(df), id='total-customers', style={'font-size': '2rem', 'color': colors['text'], 'font-weight': 'bold','box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '2px solid #ced4da', 'border-radius': '5px'}),
                ], style={'margin-right': '9rem', 'text-align': 'center', 'font-family': 'Arial, sans-serif',}),
                
                html.Div([
                    html.Label("Churn Rate", style={'color': colors['text'], 'font-size': '1.5rem'}),
                    html.Div(f"{round(df['Churn'].mean() * 100, 2)}%", id='churn-rate', style={'font-size': '2rem', 'color': colors['text'], 'font-weight': 'bold','box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '2px solid #ced4da', 'border-radius': '5px'}),
                ],style={'text-align': 'center', 'font-family': 'Arial, sans-serif'}),
            ]),
            
            dcc.Graph(
                id='churn-pie-chart',
                figure=px.pie(df, names='Churn', title='Churn Rate',  template='plotly_dark',color_discrete_sequence=[colors['accent']]),
                style={'height': '500px','text-align': 'center'}  # Adjust the height as needed
            ),
        ]),

        # Right corner: Interaction options and Line chart displaying churn rate by product category
        html.Div([
            # Interaction options
            html.Label("Select a specific product category", style={'color': colors['text'], 'margin-bottom': '10px', 'font-size': '2rem'}),
            html.Div([
                 dcc.Dropdown(
                id='product-category-dropdown',
                options=[{'label': category, 'value': category} for category in df['Product Category'].unique()],
                value=df['Product Category'].unique()[0],
                ),
            ],style={'width': '50%', 'margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto','margin-top': '10px',
                       'text-align': 'center', 'font-family': 'Arial, sans-serif', 'font-weight': '600', 'font-size': '1rem',
                       'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
           
            
            # Line chart displaying churn rate by product category
            dcc.Graph(id='analysis-graph', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                            'border': '1px solid #ced4da', 'border-radius': '5px', 'height': '500px'}),  # Adjust the height as needed
        ]),
    ]),
])

# Callbacks for dynamic updates based on user input
@app.callback(
    [Output('analysis-graph', 'figure'),
     Output('total-customers', 'children'),
     Output('churn-rate', 'children')],
    [Input('product-category-dropdown', 'value')]
)
def update_churn_by_category(selected_category):
    filtered_df = df[df['Product Category'] == selected_category]
    churn_by_category_fig = px.line(
        filtered_df,
        x='Churn',
        y='Total Purchase Amount',  # Change this to a relevant column for the y-axis
        title=f'Churn Rate for {selected_category}',
        color='Churn',
        labels={'Total Purchase Amount': 'Y-axis Label'}  # Change Y-axis label
    )
    churn_by_category_fig.update_layout(title_x=0.5)

    
    total_customers = len(filtered_df)
    churn_rate = round(filtered_df['Churn'].mean() * 100, 2)
    return churn_by_category_fig, total_customers, churn_rate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
