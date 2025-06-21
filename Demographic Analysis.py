import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Assume df is your DataFrame containing the data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)

# Drop duplicates based on 'Customer Name' for demographic analysis
unique_customers = df.drop_duplicates(subset='Customer Name')

# Check and convert 'Customer Age' column to numeric
try:
    unique_customers['Customer Age'] = pd.to_numeric(unique_customers['Customer Age'])
except pd.errors.InvalidOperation as e:
    print(f"Error converting 'Customer Age' to numeric: {e}")
    print("Unique values in 'Customer Age' column:")
    print(unique_customers['Customer Age'].unique())

# Create 'Age Group' column
age_bins = [20, 30, 40, 50, 60, 70, 80]
unique_customers['Age Group'] = pd.cut(unique_customers['Customer Age'], bins=age_bins)

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the web application
app.layout = html.Div([
    # Dropdown for age group
    dcc.Dropdown(
        id='age-group-dropdown',
        options=[
            {'label': '20-29', 'value': '20-29'},
            {'label': '30-39', 'value': '30-39'},
            {'label': '40-49', 'value': '40-49'},
            {'label': '50-59', 'value': '50-59'},
            {'label': '60-69', 'value': '60-69'},
            {'label': '70-79', 'value': '70-79'},
        ],
        value='20-29',  # Default age group
        style={'width': '50%'}
    ),

    # Dropdown for gender
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'},
        ],
        value='Male',  # Default gender
        style={'width': '50%'}
    ),

    # Distribution of customers by age and gender
    dcc.Graph(
        id='customer-age-gender-distribution',
    ),

    # Average purchase amount by age group
    dcc.Graph(
        id='avg-purchase-by-age',
    ),

    # Average purchase amount by gender
    dcc.Graph(
        id='avg-purchase-by-gender',
    ),

    # Most popular product categories by age group
    dcc.Graph(
        id='popular-products-by-age',
    ),

    # Most popular product categories by gender
    dcc.Graph(
        id='popular-products-by-gender',
    ),
])

# Callback to update the graphs based on user input
@app.callback(
    [Output('customer-age-gender-distribution', 'figure'),
     Output('avg-purchase-by-age', 'figure'),
     Output('avg-purchase-by-gender', 'figure'),
     Output('popular-products-by-age', 'figure'),
     Output('popular-products-by-gender', 'figure')],
    [Input('age-group-dropdown', 'value'),
     Input('gender-dropdown', 'value')]
)
def update_graph(age_group, gender):
    # Filter data based on user input
    filtered_data = unique_customers[(unique_customers['Age Group'] == age_group) & (unique_customers['Gender'] == gender)]

    # Distribution of customers by age and gender
    fig1 = px.histogram(
        filtered_data,
        x='Customer Age',
        color='Gender',
        barmode='overlay',
        title=f'Distribution of Customers ({gender}) in Age Group {age_group}'
    )

    # Average purchase amount by age group
    fig2 = px.bar(
        filtered_data,
        x='Age Group',
        y='Total Purchase Amount',
        title=f'Average Purchase Amount in Age Group {age_group}',
        labels={'Age Group': 'Age Group', 'Total Purchase Amount': 'Average Purchase Amount'}
    )

    # Average purchase amount by gender
    fig3 = px.bar(
        filtered_data,
        x='Gender',
        y='Total Purchase Amount',
        title=f'Average Purchase Amount for {gender}',
        labels={'Gender': 'Gender', 'Total Purchase Amount': 'Average Purchase Amount'}
    )

    # Most popular product categories by age group
    popular_products_age = filtered_data.groupby(['Age Group', 'Product Category']).size().unstack()
    fig4 = popular_products_age.plot(kind='bar', stacked=True, figsize=(12, 7))
    fig4.set_title(f'Most Popular Product Categories in Age Group {age_group}')
    fig4.set_ylabel('Number of Purchases')

    # Most popular product categories by gender
    popular_products_gender = filtered_data.groupby(['Gender', 'Product Category']).size().unstack()
    fig5 = popular_products_gender.plot(kind='bar', stacked=True, figsize=(10, 6))
    fig5.set_title(f'Most Popular Product Categories for {gender}')
    fig5.set_ylabel('Number of Purchases')

    return fig1, fig2, fig3, fig4, fig5

# Run the web application
if __name__ == '__main__':
    app.run_server(debug=True)
