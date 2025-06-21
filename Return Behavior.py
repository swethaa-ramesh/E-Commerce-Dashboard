import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Assume df is your DataFrame containing the data
df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)

# Convert Returns column to a more descriptive format for visualization
df['Returns'] = df['Returns'].map({0: 'No Return', 1: 'Returned'})

# Create the 'Age Group' column
age_bins = [20, 30, 40, 50, 60, 70, 80]
df['Age Group'] = pd.cut(df['Customer Age'], bins=age_bins, labels=['20-29', '30-39', '40-49', '50-59', '60-69', '70-79'])

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the web application
app.layout = html.Div([
    # Slider for age filtering
    dcc.RangeSlider(
        id='age-slider',
        marks={i: str(i) for i in range(20, 81, 10)},
        min=20,
        max=80,
        step=10,
        value=[20, 80],
    ),

    # Dropdown for product categories
    dcc.Dropdown(
        id='productcategory-dropdown',
        options=[{'label': category, 'value': category} for category in df['Product Category'].unique()],
        multi=True,
        value=df['Product Category'].unique(),  # Default: all categories selected
        style={'width': '50%'}
    ),

    # Graphs will be displayed here
    dcc.Graph(id='returns-distribution'),
    dcc.Graph(id='returned-product-categories'),
    dcc.Graph(id='returns-by-price-and-payment'),
    dcc.Graph(id='returns-by-age'),
    dcc.Graph(id='returns-by-gender'),
])

# Callback to update the graphs based on the age slider and product category dropdown
@app.callback(
    [Output('returns-distribution', 'figure'),
     Output('returned-product-categories', 'figure'),
     Output('returns-by-price-and-payment', 'figure'),
     Output('returns-by-age', 'figure'),
     Output('returns-by-gender', 'figure')],
    [Input('age-slider', 'value'),
     Input('productcategory-dropdown', 'value')]
)
def update_graph(age_range, selected_categories):
    filtered_df = df[(df['Customer Age'] >= age_range[0]) & (df['Customer Age'] <= age_range[1])]
    
    # Visualization 1: Percentage of transactions that resulted in returns
    fig1 = px.histogram(filtered_df, x='Returns', title='Distribution of Transactions Resulting in Returns',color_discrete_sequence=[px.colors.qualitative.Set1])

    # Define 'returned_products' here
    returned_products = filtered_df[filtered_df['Returns'] == 'Returned']

    # Visualization 2: Most commonly returned product categories (changed to Box Plot)
    fig2 = go.Figure()

    for category in selected_categories:
        category_df = returned_products[returned_products['Product Category'] == category]
        fig2.add_trace(go.Box(x=category_df['Product Category'], y=category_df['Product Price'], name=category))

    fig2.update_layout(title='Most Commonly Returned Product Categories (Box Plot)')

    # Visualization 3: Returns by product category, prices, and payment methods
    fig3 = go.Figure()

    # For Product Categories
    for category in selected_categories:
        category_df = filtered_df[filtered_df['Product Category'] == category]
        counts = category_df['Returns'].value_counts()
        fig3.add_trace(go.Bar(x=counts.index, y=counts.values, name=category))

    fig3.update_layout(barmode='group', title='Returns by Product Category')

    # For Product Prices
    fig3.add_trace(go.Box(x=filtered_df['Returns'], y=filtered_df['Product Price'], name='Product Price'))

    # For Payment Methods
    payment_counts = filtered_df.groupby(['Payment Method', 'Returns']).size().unstack(fill_value=0)
    fig3.add_trace(go.Bar(x=payment_counts.index, y=payment_counts['Returned'], name='Returned'))
    fig3.add_trace(go.Bar(x=payment_counts.index, y=payment_counts['No Return'], name='No Return'))

    fig3.update_layout(title='Returns by Product Category, Prices, and Payment Method', barmode='group')

    # Visualization 4: Returns by age group and gender
    fig4 = px.histogram(filtered_df, x='Age Group', color='Returns', barnorm='percent',
                        title='Returns by Age Group', category_orders={'Age Group': ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79']})
    
    # For Gender
    fig5 = px.histogram(filtered_df, x='Gender', color='Returns', barnorm='percent', title='Returns by Gender')

    return fig1, fig2, fig3, fig4 , fig5

# Run the web application
if __name__ == '__main__':
    app.run_server(debug=True)


