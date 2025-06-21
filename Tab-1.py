import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("ecommerce_customer_data_large.csv")
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
time_intervals = ['D', 'W', 'M', 'Y']  # 'D' for Daily, 'W' for Weekly, 'M' for Monthly, 'Y' for Yearly
payment_methods = df['Payment Method'].unique()

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("E-commerce Dashboard", style={'text-align': 'center'}),
    
    # First Row: RadioItems and Dropdown
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'}, children=[
        # RadioItems for selecting between age and gender
        dcc.RadioItems(
            id='demographic-radio',
            options=[
                {'label': 'Age', 'value': 'Age'},
                {'label': 'Gender', 'value': 'Gender'}
            ],
            value='Age',
            labelStyle={'display': 'block'}
        ),
        
        # Dropdown for selecting specific genders
        dcc.Dropdown(
            id='group-dropdown',
            options=[
                {'label': gender, 'value': gender} for gender in df['Gender'].unique()
            ],
            multi=True,  # Allow selecting multiple genders
            style={'width': '50%'}
        ),
    ]),
    
    # Second Row: RangeSlider
    html.Div([
        # RangeSlider for selecting specific age ranges
        dcc.RangeSlider(
            id='age-range-slider',
            min=df['Age'].min(),
            max=df['Age'].max(),
            marks={i: str(i) for i in range(df['Age'].min(), df['Age'].max()+1, 10)},
            value=[df['Age'].min(), df['Age'].max()],
        ),
    ], style={'margin-top': '20px'}),
    
    # Third Row: Loading and Graphs
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            # Grid layout for charts
            html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr', 'grid-gap': '20px', 'margin-top': '20px'}, children=[
                # Bar chart for distribution of customers by age or gender
                dcc.Graph(id='bar-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                 'border': '1px solid #ced4da', 'border-radius': '5px'}),
                
                # Bar chart for average purchase amount by age or gender
                dcc.Graph(id='avg-purchase-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                          'border': '1px solid #ced4da', 'border-radius': '5px'}),
                
                # Pie chart for most popular product categories by age or gender
                dcc.Graph(id='pie-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                 'border': '1px solid #ced4da', 'border-radius': '5px'}),
            ]),
        ]
    )
])

# Callback to update the bar chart, average purchase chart, and pie chart
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('avg-purchase-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('demographic-radio', 'value'),
     Input('group-dropdown', 'value'),
     Input('age-range-slider', 'value')]
)
def update_charts(selected_demographic, selected_groups, selected_age_range):
    if selected_demographic == 'Age':
        filtered_df = df[(df['Age'] >= selected_age_range[0]) & (df['Age'] <= selected_age_range[1])]
    else:
        filtered_df = df[df['Gender'].isin(selected_groups)]

    # Bar chart for distribution of customers by age or gender
   # Bar chart for distribution of customers by age or gender
    bar_chart = px.histogram(filtered_df, x=selected_demographic, title=f'Distribution of Customers by {selected_demographic}',
                                    labels={selected_demographic: selected_demographic, 'count': 'Count'},
                                    category_orders={'Gender': selected_groups} if selected_demographic == 'Gender' else None,
                                    color_discrete_sequence=px.colors.qualitative.D3_r, template="plotly_dark")
    bar_chart.update_layout(title_x=0.5,bargap=0.2)



    # Bar chart for average purchase amount by age or gender
    avg_purchase_chart = px.bar(filtered_df.groupby(selected_demographic)['Total Purchase Amount'].mean().reset_index(),
                                x=selected_demographic, y='Total Purchase Amount',
                                title=f'Average Purchase Amount by {selected_demographic}',
                                labels={selected_demographic: selected_demographic, 'Total Purchase Amount': 'Average Purchase Amount'},
                                category_orders={'Gender': selected_groups} if selected_demographic == 'Gender' else None,
                                color_discrete_sequence=px.colors.qualitative.G10,template="plotly_dark")
    avg_purchase_chart.update_layout( title_x=0.5)

    # Pie chart for most popular product categories by age or gender
    pie_chart = px.pie(filtered_df, names='Product Category', title=f'Most Popular Product Categories by {selected_demographic}',
                       labels={'Product Category': 'Product Category', 'count': 'Count'},
                       category_orders={'Gender': selected_groups} if selected_demographic == 'Gender' else None,
                       color_discrete_sequence=px.colors.qualitative.Pastel,template="plotly_dark")
    pie_chart.update_layout( title_x=0.5)

    return bar_chart, avg_purchase_chart, pie_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
