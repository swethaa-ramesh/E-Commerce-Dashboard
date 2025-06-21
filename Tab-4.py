import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Assume df is your DataFrame
df = pd.read_csv("ecommerce_customer_data_large.csv")
return_percentage = (df['Returns'].count() / len(df)) * 100
returns_df = df[df['Returns'].notnull()]

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown options for product categories
product_category_options = [{'label': category, 'value': category} for category in df['Product Category'].unique()]

# Dropdown options for age groups
age_group_options = [{'label': f'{i}-{i+9}', 'value': i} for i in range(18, 71, 10)]

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='E-commerce Data Analysis', style={'color': '#007BFF', 'text-align': 'center'}),

    # First Row: Dropdowns and Slider
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr ', 'grid-gap': '20px', 'margin-top': '20px', 'margin-bottom': '20px', 'text-align': 'center',
    'background-color': '#f8f9fa', 'color': '#495057','width':'60%','margin-left': '19.5rem'}, children=[
        # Dropdown for product categories
        dcc.Dropdown(
            id='product-category-dropdown',
            options=product_category_options,
            value=product_category_options[0]['value'],
            multi=False,
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px','font-family': 'Arial, sans-serif', 'font-weight': '600', 'font-size': '1rem',}
        ),

        # Dropdown for age groups
        dcc.Dropdown(
            id='age-group-dropdown',
            options=age_group_options,
            value=age_group_options[0]['value'],
            multi=False,
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}
        ),
    ]),

    # Second Row: Slider
    html.Div(style={'margin-top': '20px'}, children=[
        dcc.RangeSlider(
            id='age-range-slider',
            min=18,
            max=70,
            step=1,
            marks={i: f'{i}' for i in range(18, 71)},
            value=[18, 70]
        ),
    ]),

    # Third Row: Graphs
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px', 'margin-top': '20px'}, children=[
        # a. Percentage of transactions that resulted in returns
        dcc.Graph(
            id='percentage-of-returns',
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}
        ),

        # b. Most commonly returned product categories
        dcc.Graph(
            id='commonly-returned-categories',
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}
        ),
    ]),

    # Fourth Row: Graphs
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px', 'margin-top': '20px'}, children=[
        # c. Correlation between returns and product categories
        dcc.Graph(
            id='correlation-with-product-categories',
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}
        ),

        # d. Analysis of returns by age group
        dcc.Graph(
            id='returns-by-age-group',
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}
        ),
    ]),

    # Fifth Row: Graph
    html.Div(style={'margin-top': '20px'}, children=[
        # e. Analysis of returns by gender
        dcc.Graph(
            id='returns-by-gender',
            style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}
        ),
    ])
])

# Callback to update visualizations based on the selected product category, age group, and age range
@app.callback(
    Output('percentage-of-returns', 'figure'),
    Output('commonly-returned-categories', 'figure'),
    Output('correlation-with-product-categories', 'figure'),
    Output('returns-by-age-group', 'figure'),
    Output('returns-by-gender', 'figure'),
    Input('product-category-dropdown', 'value'),
    Input('age-group-dropdown', 'value'),
    Input('age-range-slider', 'value')
)
def update_visualizations(selected_category, selected_age_group, selected_age_range):
    filtered_df = df[(df['Product Category'] == selected_category) &
                     (df['Age'].between(selected_age_range[0], selected_age_range[1]))]

    # Update the pie chart
    return_percentage = (filtered_df['Returns'].count() / len(filtered_df)) * 100
    pie_chart = px.pie(names=['No Returns', 'Returns'], values=[100 - return_percentage, return_percentage],title='Percentage of Transactions with Returns', hole=0.1,labels={'No Returns': 'No Returns', 'Returns': 'Returns'},color_discrete_sequence=px.colors.qualitative.Set2,template='plotly_dark')
    pie_chart .update_layout(title_x=0.5)

    # Update the bar chart for most commonly returned product categories
    bar_chart_common_returns = px.bar(x=filtered_df['Product Category'].value_counts().index,y=filtered_df['Product Category'].value_counts().values,template="plotly_dark",labels={'x': 'Product Category', 'y': 'Count of Returns'},title='Most Commonly Returned Product Categories').update_xaxes(categoryorder='total ascending')
    pie_chart .update_layout(title_x=0.5)

    # Update the bar chart for correlation between returns and product categories
    bar_chart_correlation = px.histogram(filtered_df, x='Product Category', color='Returns', barmode='group', title='Distribution of Product Category with Returns',color_discrete_sequence=px.colors.qualitative.Dark24_r,template="plotly_dark")
    bar_chart_correlation.update_layout(title_x=0.5)

    # Update the bar chart for returns by age group
    bar_chart_age_group =px.histogram(filtered_df, x='Age', color='Returns', barmode='group',title='Distribution of Age with Returns',color_discrete_sequence=px.colors.qualitative.Light24,template="plotly_dark")
    bar_chart_age_group.update_layout(title_x=0.5)

    # Update the bar chart for returns by gender
    bar_chart_gender = px.histogram(filtered_df, x='Gender', color='Returns', barmode='group',title='Distribution of Gender with Returns',color_discrete_sequence=px.colors.qualitative.Set2,template="plotly_dark")
    bar_chart_gender.update_layout(title_x=0.5,bargap=0.2)

    return pie_chart, bar_chart_common_returns, bar_chart_correlation, bar_chart_age_group, bar_chart_gender

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
