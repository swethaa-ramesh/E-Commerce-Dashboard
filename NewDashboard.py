import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from dash.dash_table.Format import Group
from dash import dash_table

df = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)
df2 = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)
df3 = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)
df4 = pd.read_csv("ecommerce_customer_data_large.csv", parse_dates=['Purchase Date'], low_memory=False)
# Set 'Purchase Date' as the index
df.set_index('Purchase Date', inplace=True)
df4.set_index('Purchase Date', inplace=True)
analysis_options = ['Product Category Count', 'Payment Method Count', 'Gender Count'] 

# Convert Returns column to a more descriptive format for visualization
df['Returns'] = df['Returns'].map({0: 'No Return', 1: 'Returned'})

# Calculate transactions_per_customer and total_purchase_per_customer outside the callback
transactions_per_customer = df.groupby('Customer Name').size()
total_purchase_per_customer = df.groupby('Customer Name')['Total Purchase Amount'].sum()
# Convert 'Purchase Date' to datetime
df2['Purchase Date'] = pd.to_datetime(df2['Purchase Date'])
df2['Purchase Month'] = df2['Purchase Date'].dt.to_period('M').astype(str)  # Convert to string

# Create the 'Age Group' column
age_bins = [20, 30, 40, 50, 60, 70, 80]
df['Age Group'] = pd.cut(df['Customer Age'], bins=age_bins, labels=['20-29', '30-39', '40-49', '50-59', '60-69', '70-79'])

#Segementation
# Create a customer-level dataset with relevant metrics for segmentation
customer_data = df3.groupby('Customer Name').agg({
    'Total Purchase Amount': ['sum', 'mean'],
    'Returns': 'sum',
    'Churn': 'max'
}).reset_index()
customer_data.columns = ['Customer Name', 'Total Purchases', 'Average Purchase Amount', 'Total Returns', 'Churn Status']

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_data[['Total Purchases', 'Average Purchase Amount', 'Total Returns', 'Churn Status']])

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
scaled_data_imputed = imputer.fit_transform(scaled_data)

# Set up Dash app
app = dash.Dash(__name__)

# Dropdown for analysis selection
analysis_dropdown = dcc.Dropdown(
    id='Payment-dropdown',
    options=[
        {'label': 'Distribution of payment methods', 'value': 'payment_distribution'},
        {'label': 'Average purchase amount by payment method', 'value': 'average_purchase'},
        {'label': 'Correlation between payment method and product category or price', 'value': 'correlation_plot'}
    ],
    value='payment_distribution',  # Default selection
    multi=False
)

# Default figures
payment_distribution_fig = px.histogram(df, x='Payment Method', title='Distribution of Payment Methods Used by Customers')
average_purchase_fig = px.scatter(df, x='Payment Method', y='Total Purchase Amount', title='Average Purchase Amount by Payment Method')  # Changed to scatter plot
correlation_fig = px.box(df, x='Payment Method', y='Product Price', color='Product Category',
                         title='Distribution of Product Prices by Payment Method and Product Category')



app.layout = html.Div([

    dcc.Tabs(children=[
        #TAB-1
        dcc.Tab(label='Churn',children=[
             html.H1(children='Churn Behavior Analysis', style={'text-align': 'center', 'color': '#333'}),

            # Dropdown for selecting the type of analysis
            html.Div([
                 dcc.Dropdown(
                id='analysis-dropdown',
                options=[{'label': option, 'value': option} for option in analysis_options],
                value=analysis_options[0],
                multi=False,
            ),
            ],style={'width': '30%', 'margin': '20px auto', 'text-align': 'center'}),
           

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

        ]),#TAB-1 End

        #TAB-2
        dcc.Tab(label='Loyalty and Retention',children=[
                 dcc.Dropdown(
        id='Loyalty-dropdown',
        options=[
            {'label': 'Transactions per Customer', 'value': 'transactions_per_customer'},
            {'label': 'Time Between Consecutive Purchases', 'value': 'time_between_purchases'},
            {'label': 'Total Purchase Amount by Churn Status', 'value': 'total_purchase_by_churn'},
            {'label': 'Potential Loyal Customers', 'value': 'potential_loyal_customers'}
        ],
        value='transactions_per_customer',
        style={'width': '50%'}
         ),

        # Graph will be displayed here
        dcc.Graph(id='Loyalty-graph'),
        ]),#TAB-2 End
        
         #TAB-3
        dcc.Tab(label='Payment',children=[
             html.H1("Payment Analysis"),
    
            html.Div([
                html.Label('Select Analysis:'),
                analysis_dropdown,
            ]),

            html.Div([
                dcc.Graph(id='Payment-plot'),
            ]),
                    
        ]),#TAB-3 End
        
        #TAB-4
        dcc.Tab(label='Purchase Behavior',children=[
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
        ]),#TAB-4 End
        
         #TAB-5
    dcc.Tab(label='Return Behavior',children=[
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
    ]),#TAB-5 End
        
         #TAB-6
        dcc.Tab(label='Segmentation',children=[
            dcc.Dropdown(
        id='cluster-dropdown',
        options=[
            {'label': f'{n} Clusters', 'value': n} for n in range(2, 11)
        ],
        value=4,  # Default: 4 clusters
        style={'width': '50%'}
        ),

        # Scatter plot for customer segmentation
        dcc.Graph(
            id='customer-segmentation',
        ),

        # Table for cluster summary
        dash_table.DataTable(
            id='cluster-summary',
        ),
        ]),#TAB-6 End
        
         #TAB-7
        dcc.Tab(label='Time Series Analysis',children=[
              # Dropdown to select time frequency
            html.Label('Select Time Frequency:'),
            dcc.Dropdown(
                id='time-frequency-dropdown',
                options=[
                    {'label': 'Monthly', 'value': 'M'},
                    {'label': 'Weekly', 'value': 'W'}
                ],
                value='M',  # Default: Monthly
                style={'width': '50%'}
            ),
            # Graph for sales trend
            dcc.Graph(id='sales-trend'),
      
            # Graph for seasonal patterns in product category sales
            dcc.Graph(id='seasonal-patterns'),
        ]),#TAB-7 End
        

    ])
])

# Define callback to update the graphs based on user input
#TAB-1
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

#TAB-2

# Callback to update the graph based on the selected analysis
@app.callback(
    Output('Loyalty-graph', 'figure'),
    [Input('Loyalty-dropdown', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'transactions_per_customer':
        # 1. Average number of transactions per customer
        fig = px.histogram(transactions_per_customer, x=transactions_per_customer, title='Distribution of Number of Transactions Per Customer', labels={'x': 'Number of Transactions'})
    elif selected_analysis == 'time_between_purchases':
        # 2. Average time between consecutive purchases for a customer
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
        df_sorted = df.sort_values(['Customer Name', 'Purchase Date'])
        df_sorted['Time Between Purchases'] = df_sorted.groupby('Customer Name')['Purchase Date'].diff()
        average_time_between_purchases = df_sorted.groupby('Customer Name')['Time Between Purchases'].mean().dt.days
        fig = px.histogram(average_time_between_purchases, x=average_time_between_purchases, title='Average Time Between Consecutive Purchases (in days)', labels={'x': 'Days'})
    elif selected_analysis == 'total_purchase_by_churn':
        # 3. Correlation between total purchase amount and churn
        fig = px.histogram(df, x='Total Purchase Amount', color='Churn', nbins=20, title='Total Purchase Amount by Churn Status', labels={'x': 'Total Purchase Amount', 'color': 'Churn'})
        fig.update_layout(bargap=0.2)
    elif selected_analysis == 'potential_loyal_customers':
        # 4. Identify potential loyal customers based on frequency and amount of purchases
        loyal_threshold_transactions = transactions_per_customer.quantile(0.75)
        loyal_threshold_purchase = total_purchase_per_customer.quantile(0.75)
        potential_loyal_customers = df.groupby('Customer Name').filter(lambda x: len(x) > loyal_threshold_transactions and x['Total Purchase Amount'].sum() > loyal_threshold_purchase)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=potential_loyal_customers['Customer Name'].unique(), y=[1] * len(potential_loyal_customers['Customer Name'].unique()), mode='markers', marker=dict(size=10), text=potential_loyal_customers['Customer Name'].unique()))
        fig.update_layout(title='Potential Loyal Customers', showlegend=False)

    return fig

#TAB-3
# Callback to update the selected plot based on the dropdown value
@app.callback(
    dash.dependencies.Output('Payment-plot', 'figure'),
    [dash.dependencies.Input('Payment-dropdown', 'value')]
)
def update_selected_plot(selected_analysis):
    if selected_analysis == 'payment_distribution':
        return payment_distribution_fig
    elif selected_analysis == 'average_purchase':
        return average_purchase_fig
    elif selected_analysis == 'correlation_plot':
        return correlation_fig
    
#TAB-4
# Callback to update the graph based on the selected analysis type
@app.callback(
    Output('output-graph', 'figure'),
    [Input('analysis-type', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'frequency':
        fig = px.histogram(df2, x='Purchase Month', title='Frequency Distribution of Purchase Dates',color_discrete_sequence=[px.colors.qualitative.Light24[2]]).update_xaxes(categoryorder='total descending')
    elif selected_analysis == 'quantity':
        fig = px.histogram(df2, x='Quantity', title='Distribution of Quantity Purchased',color_discrete_sequence=[px.colors.qualitative.D3_r])
        fig.update_layout(bargap=0.2)
    elif selected_analysis == 'popularity':
        fig = px.bar(df2['Product Category'].value_counts(), x=df2['Product Category'].value_counts().index, y=df2['Product Category'].value_counts().values,color_discrete_sequence=[px.colors.qualitative.Bold] ,title='Most Popular Product Categories').update_xaxes(categoryorder='total descending')
    elif selected_analysis == 'distribution':
        fig = px.histogram(df2, x='Total Purchase Amount', nbins=30, title='Distribution of Total Purchase Amounts',color_discrete_sequence=[px.colors.qualitative.Alphabet])
        fig.update_layout(bargap=0.2)
    return fig
#TAB-5
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

#TAB-6
@app.callback(
    [Output('customer-segmentation', 'figure'),
     Output('cluster-summary', 'columns'),
     Output('cluster-summary', 'data')],
    [Input('cluster-dropdown', 'value')]
)
def update_graph(num_clusters):
    # Apply KMeans clustering with the selected number of clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    customer_data['Cluster'] = kmeans.fit_predict(scaled_data_imputed)

    # Cluster summary
    cluster_summary = customer_data.groupby('Cluster').agg({
        'Total Purchases': 'mean',
        'Average Purchase Amount': 'mean',
        'Total Returns': 'mean',
        'Churn Status': 'mean'
    }).reset_index()

    # Scatter plot
    fig = px.scatter(
        customer_data,
        x='Total Purchases',
        y='Average Purchase Amount',
        color='Cluster',
        title=f'Customer Segmentation ({num_clusters} Clusters)',
    )

    return fig, [{'name': col, 'id': col} for col in cluster_summary.columns], cluster_summary.to_dict('records')

#TAB-7
# Callback to update the graphs based on the selected time frequency
@app.callback(
    [Output('sales-trend', 'figure'),
     Output('seasonal-patterns', 'figure')],
    [Input('time-frequency-dropdown', 'value')]
)
def update_graphs(selected_frequency):
    # Monthly or weekly trends in total sales
    if selected_frequency == 'M':
        sales_trend = px.line(df4.resample('M').sum(), x=df4.resample('M').sum().index, y='Total Purchase Amount', labels={'x': 'Month', 'y': 'Total Sales'},
                              title='Monthly Sales Trend')
    else:
        sales_trend = px.line(df4.resample('W').sum(), x=df4.resample('W').sum().index, y='Total Purchase Amount', labels={'x': 'Week', 'y': 'Total Sales'},
                              title='Weekly Sales Trend')

    # Seasonal patterns in product category sales
    monthly_product_sales = df4.groupby([df4.index.month, 'Product Category']).size().unstack()
    seasonal_patterns = px.line(monthly_product_sales, x=monthly_product_sales.index, y=monthly_product_sales.columns,
                                labels={'x': 'Month', 'y': 'Number of Sales'}, title='Monthly Sales Count by Product Category')

    return sales_trend, seasonal_patterns


if __name__ == '__main__':
    app.run_server(debug=True)
