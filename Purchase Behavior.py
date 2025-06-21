import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Assume df is your DataFrame containing the data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)
# Convert 'Purchase Date' to datetime
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
df['Purchase Month'] = df['Purchase Date'].dt.to_period('M').astype(str)  # Convert to string

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the web application
app.layout = html.Div([
    # Dropdown for selecting analysis type
    dcc.Dropdown(
        id='analysis-type',
        options=[
            {'label': 'Frequency distribution of purchase dates', 'value': 'frequency'},
            {'label': 'Average quantity of products purchased', 'value': 'quantity'},
            {'label': 'Most popular product categories and their average prices', 'value': 'popularity'},
            {'label': 'Distribution of total purchase amounts', 'value': 'distribution'}
        ],
        value='frequency',
        style={'width': '50%'}
    ),

    # Graph will be displayed here
    dcc.Graph(id='output-graph'),

])

# Callback to update the graph based on the selected analysis type
@app.callback(
    Output('output-graph', 'figure'),
    [Input('analysis-type', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'frequency':
        fig = px.histogram(df, x='Purchase Month', title='Frequency Distribution of Purchase Dates',color_discrete_sequence=[px.colors.qualitative.Light24[2]]).update_xaxes(categoryorder='total descending')
    elif selected_analysis == 'quantity':
        fig = px.histogram(df, x='Quantity', title='Distribution of Quantity Purchased',color_discrete_sequence=[px.colors.qualitative.D3_r])
        fig.update_layout(bargap=0.2)
    elif selected_analysis == 'popularity':
        fig = px.bar(df['Product Category'].value_counts(), x=df['Product Category'].value_counts().index, y=df['Product Category'].value_counts().values,color_discrete_sequence=[px.colors.qualitative.Bold] ,title='Most Popular Product Categories').update_xaxes(categoryorder='total descending')
    elif selected_analysis == 'distribution':
        fig = px.histogram(df, x='Total Purchase Amount', nbins=30, title='Distribution of Total Purchase Amounts',color_discrete_sequence=[px.colors.qualitative.Alphabet])
        fig.update_layout(bargap=0.2)

    return fig

# Run the web application
if __name__ == '__main__':
    app.run_server(debug=True)
