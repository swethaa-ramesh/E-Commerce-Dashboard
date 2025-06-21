import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import base64

# Assuming 'df' is your DataFrame
df = pd.read_csv("ecommerce_customer_data_large.csv")

# Create a new column 'Segment' based on user segments
df['Segment'] = 'Purchase Behavior'

# Define color map for segments
color_map = {
    'Purchase Behavior': '#FFFD8C',  
    'Demographic Info': '#97FFF4',  
    'Churn Status': '#7091F5'      
}

# Initialize the Dash app
app = dash.Dash(__name__)

image = 'logo.png'
image_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')

# Define layout
app.layout = html.Div(style={'backgroundColor': '#f4f4f4', 'padding': '20px', 'font-family': 'Arial, sans-serif'}, children=[
    html.Img(src='data:image/png;base64,{}'.format(image_base64), style={'width': '100px', 'margin': 'auto', 'display': 'block'}),
    html.H1("Customer Segmentation Dashboard", style={'color': '#333', 'margin-bottom': '20px', 'text-align': 'center'}),

    # Dropdown for selecting segments
    html.Div([
        dcc.Dropdown(
            id='segment-dropdown',
            options=[
                {'label': 'Purchase Behavior', 'value': 'Purchase Behavior'},
                {'label': 'Demographic Info', 'value': 'Demographic Info'},
                {'label': 'Churn Status', 'value': 'Churn Status'}
            ],
            value='Purchase Behavior',
            multi=False,
        ),
    ], style={
       'width': '30%',
       'margin': 'auto',
       'text-align': 'center',
       'font-family': 'Arial, sans-serif',
       'font-weight': '600',
       'font-size': '1rem',
        'background-color': '#ffffff',
        'border-radius': '10px',
        'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.3)',       
    }),
    html.Div([
        # Scatter plot or bubble chart
        dcc.Graph(
            id='segment-scatter',
            style={'width': '48%', 'display': 'inline-block', 'background-color': '#ffffff', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),

        # Bar chart or pie chart
        dcc.Graph(
            id='revenue-chart',
            style={'width': '48%', 'display': 'inline-block', 'background-color': '#ffffff', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),
    ], style={'margin-top': '20px', 'text-align': 'center'}),

    # Text box for displaying strategies
    html.Div([
        dcc.Textarea(
            id='strategy-textarea',
            value='',
            style={'width': '80%', 'height': 100, 'margin': 'auto', 'display': 'block', 'resize': 'none','font-size':'20px','font-family': 'Arial, sans-serif',},
            readOnly=True
        )
    ], style={'margin-top': '20px', 'text-align': 'center'})
])



# Update the callback function
@app.callback(
    Output('segment-scatter', 'figure'),
    Output('revenue-chart', 'figure'),
    Output('strategy-textarea', 'value'),
    Input('segment-dropdown', 'value')
)
def update_plots(selected_segment):
    # Update 'Segment' column based on selected segment
    df['Segment'] = selected_segment

    # Update scatter plot based on 'Segment' column
    scatter_fig = px.scatter(df, x='Customer Age', y='Total Purchase Amount', color='Segment', size='Quantity', hover_data=['Customer Name'], title='Customer Segmentation', color_discrete_map=color_map, template="plotly_dark")  
    scatter_fig.update_layout(title_x=0.5)

    # Update revenue chart based on 'Segment' column
    revenue_fig = px.histogram(df, x='Total Purchase Amount', color='Segment', nbins=30, title='Distribution of Total Purchase Amount by Segment', template='plotly_dark', color_discrete_map=color_map)
    revenue_fig.update_layout(title_x=0.5, bargap=0.2)

    # Display detailed information in the text area
    detailed_info = get_detailed_info(selected_segment)

    return scatter_fig, revenue_fig, detailed_info

def get_detailed_info(segment):
    # Function to get detailed information based on the selected segment
    # You can customize this based on your business logic
    if segment == 'Purchase Behavior':
        return "In the Above Graph Shows the Relationshion of Purchase Behavior of the customer Purchase items in the store .The Right side graph shows the Total Amount purchase Based on the customer's age.The Other Graph Shows the Count of Total amount Of customer has purchsed from the store "
    elif segment == 'Demographic Info':
        return  "In the Above Graph Shows the Democracy Info of the customer Purchase items in the store .The Right side graph shows the Total Amount purchase Based on the customer's age.The Other Graph Shows the Count of Total amount Of customer has purchsed from the store "
    elif segment == 'Churn Status':
        return  "In the Above Graph Shows the Churn Status  of the  .The Right side graph shows the Total Amount purchase Based on the customer's age.The Other Graph Shows the Count of Total amount Of customer has purchsed from the store "
    else:
        return "No specific information available for this segment."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
