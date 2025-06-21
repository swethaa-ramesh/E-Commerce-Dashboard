import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd 

# Read the provided dataset
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define unique values for dropdown options
analysis_options = ['Product Category Count', 'Payment Method Count', 'Gender Count']

# Define the layout of the app
app.layout = html.Div(style={'font-family': 'Arial, sans-serif'}, children=[
    html.H1(children='E-commerce Customer Behavior Analysis', style={'text-align': 'center', 'color': '#333'}),

    # Dropdown for selecting the type of analysis
    dcc.Dropdown(
        id='analysis-dropdown',
        options=[{'label': option, 'value': option} for option in analysis_options],
        value=analysis_options[0],
        multi=False,
        style={'width': '50%', 'margin': '20px auto', 'text-align': 'center'}
    ),

    # One row, three columns for graphs
    html.Div(className='row', children=[
        html.Div(className='four columns', children=[
            dcc.Graph(
                id='analysis-graph',
                style={'margin-top': '20px'}
            )
        ]),
        html.Div(className='four columns', children=[
            dcc.Graph(
                id='pie-chart',
                style={'margin-top': '20px'}
            )
        ]),
        html.Div(className='four columns', children=[
            dcc.Graph(
                id='box-plot',
                style={'margin-top': '20px'}
            )
        ]),
    ]),
])

# Define callback to update the graphs based on user input
@app.callback(
    [Output('analysis-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('box-plot', 'figure')],
    [Input('analysis-dropdown', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'Product Category Count':
        bar_fig = px.bar(df['Product Category'].value_counts(), x=df['Product Category'].value_counts().index, y=df['Product Category'].value_counts(), title='Product Category Count')
        pie_fig = px.pie(df, names='Product Category', title='Product Category Distribution')
        box_plot_fig = px.box(df, x='Product Category', y='Total Purchase Amount', title='Product Category vs. Total Purchase Amount')

    elif selected_analysis == 'Payment Method Count':
        bar_fig = px.bar(df['Payment Method'].value_counts(), x=df['Payment Method'].value_counts().index, y=df['Payment Method'].value_counts(), title='Payment Method Count')
        pie_fig = px.pie(df, names='Payment Method', title='Payment Method Distribution')
        box_plot_fig = px.box(df, x='Payment Method', y='Total Purchase Amount', title='Payment Method vs. Total Purchase Amount')

    elif selected_analysis == 'Gender Count':
        bar_fig = px.bar(df['Gender'].value_counts(), x=df['Gender'].value_counts().index, y=df['Gender'].value_counts(), title='Gender Count')
        pie_fig = px.pie(df, names='Gender', title='Gender Distribution')
        box_plot_fig = px.box(df, x='Gender', y='Total Purchase Amount', title='Gender vs. Total Purchase Amount')

    return bar_fig, pie_fig, box_plot_fig

if __name__ == '__main__':
    app.run_server(debug=True)
