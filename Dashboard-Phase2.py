import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# Load the dataset
df = pd.read_csv("ecommerce_customer_data_large.csv")
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

time_intervals = ['D', 'W', 'M', 'Y']  # 'D' for Daily, 'W' for Weekly, 'M' for Monthly, 'Y' for Yearly
payment_methods = df['Payment Method'].unique()
return_percentage = (df['Returns'].count() / len(df)) * 100
returns_df = df[df['Returns'].notnull()]
# Dropdown options for product categories
product_category_options = [{'label': category, 'value': category} for category in df['Product Category'].unique()]

colors = {
    'background': '#f8f9fa',  # Light gray background
    'text': '#495057',  # Dark gray text
    'accent': '#007BFF'  # Blue accent color
}

color_map = {
    'Purchase Behavior': '#FFFD8C',  
    'Demographic Info': '#97FFF4',  
    'Churn Status': '#7091F5'      
}

# Dropdown options for age groups
age_group_options = [{'label': f'{i}-{i+9}', 'value': i} for i in range(18, 71, 10)]

app = dash.Dash(__name__)
# image = 'logo.png'
# image_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')
app.layout = html.Div(style={'font-family': 'Arial, sans-serif'},children=[
    #  html.Img(src='data:image/png;base64,{}'.format(image_base64), style={'width': '100px', 'margin': 'auto', 'display': 'block'}),
    html.H1("E-commerce Dashboard", style={'text-align': 'center'}),
    dcc.Tabs(children=[

         dcc.Tab(label='Download Dataset',children=[
             # Duplicate the structure for the second tab as needed
                html.Div([
                        html.H2("Ecommerce Customer Dataset preview",style={'text-align': 'center'}),
            # Checklist for selecting columns to drop
            html.H3('Select Columns to Drop:'),
            # Custom HTML and CSS for a flex container
            html.Div(
                id='column-checklist-container',
            children=[
                html.Div([
                    dcc.Checklist(
                        id='column-checklist-row1',
                        options=[{'label': col, 'value': col} for col in df.columns[:len(df.columns)//2]],
                        value=[],
                        style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-evenly','margin-bottom':'5px'},
                    ),
                ]),
                html.Div([
                    dcc.Checklist(
                        id='column-checklist-row2',
                        options=[{'label': col, 'value': col} for col in df.columns[len(df.columns)//2:]],
                        value=[],
                        style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-evenly'},
                    ),
                ]),
            ],
        ),
        html.Br(),
        html.H4("Click on the download button below to Download the dataset"),
        html.Button(
            "Download CSV",
            id="csv-button",
            n_clicks=0,
            style={
                'color': 'white',
                'borderStyle': 'solid',
                'borderWidth': '1px',
                'borderRadius': '10px',
                'backgroundColor': '#0e1012',
                'textTransform': 'uppercase',
                'fontFamily': 'sans-serif',
                'fontWeight': '900',
                'transition': 'all 0.2s ease',
                'marginTop': '10px',
            }
        ),
        # Display the data in an Ag-Grid table with styling
        dag.AgGrid(
            id='ag-grid',
            columnDefs=[{'headerName': col, 'field': col} for col in df.columns],
            rowData=df.to_dict('records'),
            className="ag-theme-alpine-dark",
            dashGridOptions={
                'rowHeight': 40,
                'domLayout': 'autoHeight',
                'animateRows': True,
                'pagination': True,
                'paginationPageSize': 20,
                'exportDataAsCsv': True,  # Enable CSV export option
            },
            style={'height': '500px', 'width': '100%', },
        ),
        dcc.Download(id="download-data"),
            ]),
        ]),#TAB-9 END

        #TAB-1
        dcc.Tab(label=' Demographic Analysis:',children=[
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

        ]),
         #TAB-9 Start Download
       
        
        #TAB-1
        dcc.Tab(label='Purchase Behavior',children=[
             html.H1("Purchase Behavior Dashboard", style={'color': '#007BFF', 'text-align': 'center', 'margin-bottom': '20px'}),
    
    # Dropdown for selecting time intervals
    html.Div([
        dcc.Dropdown(
            id='time-interval-dropdown',
            options=[{'label': interval, 'value': interval} for interval in time_intervals],
            value='M',  # default selection is Monthly   
        ),
    ], style={'width': '30%', 'margin-bottom': '20px', 'text-align': 'center',
              'font-family': 'Arial, sans-serif', 'font-weight': '600', 'font-size': '1rem','margin-left': '20rem',
              'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px',
              'background-color': '#f8f9fa', 'color': '#495057'}),

    # Grid layout for charts
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'}, children=[
        # Line chart for frequency distribution of purchase dates
        dcc.Graph(id='purchase-date-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                   'border': '1px solid #ced4da', 'border-radius': '5px',
                                                   'background-color': '#ffffff'}),
                                                  
        # Bar chart for average quantity of products purchased
        dcc.Graph(id='average-quantity-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                       'border': '1px solid #ced4da', 'border-radius': '5px',
                                                       'background-color': '#ffffff'}),
    ]),

    # Grid layout for charts
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px', 'margin-top': '20px'}, children=[
        # Bar chart for most popular product categories and their average prices
        dcc.Graph(id='product-category-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                       'border': '1px solid #ced4da', 'border-radius': '5px',
                                                       'background-color': '#ffffff'}),

        # Histogram for distribution of total purchase amounts
        dcc.Graph(id='total-purchase-distribution', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                           'border': '1px solid #ced4da', 'border-radius': '5px',
                                                           'background-color': '#ffffff'}),
    ]),
        ]),#TAB-2 End

        #TAB-3 Start
        dcc.Tab(label='Payment Analysis:',children=[
            html.H1("Payment Analysis", style={'color': 'cyan', 'text-align': 'center'}),

    # Dropdown for selecting specific payment methods (multi=True for multiple selections)
    html.Div([
        dcc.Dropdown(
        id='payment-method-dropdown',
        options=[{'label': method, 'value': method} for method in payment_methods],
        value=[payment_methods[0]],  # Default value (can be a list)
        multi=True,
        
    ),
    ],style={'width':'30%','margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto','box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
    

    # Grid layout for charts
    html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'}, children=[
        # Pie chart showing the percentage of the selected payment methods
        dcc.Graph(id='payment-pie-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                 'border': '1px solid #ced4da', 'border-radius': '5px'}),

        # Bar chart with payment methods on X-axis, average purchase amount on Y-axis
        dcc.Graph(id='average-purchase-bar-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                         'border': '1px solid #ced4da', 'border-radius': '5px'}),
    ]),

    # Scatter plot with payment methods on X-axis, product category/price on Y-axis
    dcc.Graph(id='correlation-scatter-plot', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                     'border': '1px solid #ced4da', 'border-radius': '5px',
                                                     'margin-top': '20px'}),
        ]),#TAB-3

        #TAB-4Start
        dcc.Tab(label=' Return Behavior:',children=[
            html.H1(children=' Return Behavior: Analysis', style={'color': '#007BFF', 'text-align': 'center'}),

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
            id='agerange-slider',
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
        ) ])
        ]),#TAB_4
        #TAB-5 S
        dcc.Tab(label='Churn Rate ',children=[
            html.H1("Churn Rate Among Customers Dashboard", style={'color': colors['accent'], 'text-align': 'center'}),

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
                figure=px.pie(df, names='Churn', title='Churn Rate',  template='plotly_dark', color_discrete_sequence=[colors['accent']]),
                style={'height': '500px','text-align': 'center'}  # Adjust the height as needed
            ),
        ]),

        # Right corner: Interaction options and Line chart displaying churn rate by product category
        html.Div([
            # Interaction options
            html.Label("Select a specific product category", style={'color': colors['text'], 'margin-bottom': '10px', 'font-size': '2rem'}),
            html.Div([
                 dcc.Dropdown(
                id='productcategory-dropdown',
                options=[{'label': category, 'value': category} for category in df['Product Category'].unique()],
                value=df['Product Category'].unique()[0],
                ),
            ],style={'width': '50%', 'margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto','margin-top': '10px',
                       'text-align': 'center', 'font-family': 'Arial, sans-serif', 'font-weight': '600', 'font-size': '1rem',
                       'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
           
            
            # Line chart displaying churn rate by product category
            dcc.Graph(id='churn-by-category-chart', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)',
                                                            'border': '1px solid #ced4da', 'border-radius': '5px', 'height': '500px'}),  # Adjust the height as needed
        ]),])
        ]),#TAB-5 end
        #TAB-6 Start
        dcc.Tab(label='Average number of transactions per customer',children=[
                html.H1("Average number of transactions per customer", style={'color': '#007BFF', 'text-align': 'center', 'margin-bottom': '20px'}),  # Set header color and center text
    html.Div([
         # Dropdown for selecting the analysis type
    dcc.Dropdown(
        id='analysis-type',
        options=[
            {'label': 'Average Transactions per Customer', 'value': 'avg_transactions'},
            {'label': 'Average Time Between Consecutive Purchases', 'value': 'avg_time_between_purchases'},
            {'label': 'Correlation between Total Purchase Amount and Churn', 'value': 'correlation'},
            {'label': 'Identify Potential Loyal Customers', 'value': 'loyal_customers'}
        ],
        value='avg_transactions',
        ),
           ],style={'width': '30%', 'margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto',
            'text-align': 'center',
            'font-family': 'Arial, sans-serif',
            'font-weight': '600',
            'font-size': '1rem', 'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
   
    html.Div([
         # Placeholder for the selected analysis result
        dcc.Graph(id='analysis-result', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px',})
    ])
        ]),#TAB-6 End

        #TAB_7 Start
        dcc.Tab(label='Time Series Analysis:',children=[
             html.H1("Time Series Analysis", style={'color': '#007BFF', 'text-align': 'center'}),  # Set header color and center text
    
    html.Div([
        # Dropdown for selecting time period
        dcc.Dropdown(
            id='time-period-dropdown',
            options=[
                {'label': 'Monthly', 'value': 'M'},
                {'label': 'Weekly', 'value': 'W'}
            ],
            value='M',  # Default value
              # Add drop shadow and outline
                ),
            ],style={'width': '20%', 'margin-bottom': '20px', 'margin-left': 'auto', 'margin-right': 'auto','text-align': 'center','box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px' }),
                
         html.Div([
        # Radio button for selecting product category
        dcc.RadioItems(
            id='product-category-radio',
            options=[
                {'label': category, 'value': category}
                for category in df['Product Category'].unique()
            ],
            value=df['Product Category'].unique()[0],  # Default value
            labelStyle={'display': 'block', 'margin-bottom': '10px'}  # Add margin
        ),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
              }),  # Center dropdown and radio items
    
    html.Div([
        # Graph for total sales over time
        dcc.Graph(id='total-sales-graph', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
    
        # Graph for seasonal patterns in selected product category sales
        dcc.Graph(id='product-category-sales-graph', style={'box-shadow': '0 8px 16px rgba rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'}),
    
        # Graph for trends in returns over time
        dcc.Graph(id='returns-over-time-graph', style={'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.1)', 'border': '1px solid #ced4da', 'border-radius': '5px'})
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'grid-gap': '20px', 'margin': '20px'}),  # Use grid layout
        ]),#TAB-7 End

        #TAB-8 start
        dcc.Tab(label='Segmentation',children=[
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
    ],style={
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
    html.Div(id='strategy-text', style={'font-size': '2rem', 'text-align': 'center'})

        ]),#TAB 8 End
     dcc.Tab(label='Customer Name Distribution',children=[
                html.H1("Customer Name Distribution", style={'color': '#007BFF', 'text-align': 'center'}),
    # First Row
    html.Div([
        # First Column - Dropdowns
        html.Div([
            html.Label("Select Customer:"),
            dcc.Dropdown(
                id='customer-dropdown1',
                options=[{'label': customer, 'value': customer} for customer in df['Customer Name'].unique()],
                value=df['Customer Name'].unique()[0],style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px','margin-bottom': '1rem'}
               
            ),
            html.Label("Select Product Category:"),
            dcc.Dropdown(
                id='product-category-dropdown1',
                options=[{'label': category, 'value': category} for category in df['Product Category'].unique()],
                value=df['Product Category'].unique()[0],style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            ),
        ], className="four columns", style={'margin-top': '4rem', 'margin-right': '1rem'}),

        # Second Column - Scatter Chart
        html.Div([
            dcc.Graph(
                id='scatter-plot1',
                style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            )
        ], className="four columns", style={'margin-bottom': '1rem','margin-top': '2rem'}),

        # Third Column - Pie Chart
        html.Div([
            dcc.Graph(
                id='pie-chart1',
                style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            )
        ], className="four columns", style={'margin-bottom': '1rem','margin-top': '2rem'}),
    ], className="row", style={'display': 'grid', 'grid-template-columns': '15% 1fr 25%', 'gap': '20px'}),

    # Second Row
    html.Div([
        # Bar Graph
        html.Div([
            dcc.Graph(
                id='bar-chart1',
                style={'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '8px'}
            )
        ], className="twelve columns"),
    ], className="row", style={'display': 'grid', 'grid-template-columns': '1fr'}),
        ],style={'backgroundColor': '#f4f4f4', 'padding': '20px', 'font-family': 'Arial, sans-serif'}),#TAB -9

        dcc.Tab(label='Customer ID Distribution',children=[
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
        ]),#TAB-10
    ])#TABS
])#HTML


#TAB-1
# Callback to update the bar chart, average purchase chart, and pie chart
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('avg-purchase-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('demographic-radio', 'value'),
     Input('group-dropdown', 'value'),
     Input('age-range-slider', 'value')]
)
def tab2_update_charts(selected_demographic, selected_groups, selected_age_range):
    if selected_demographic == 'Age':
        filtered_df = df[(df['Age'] >= selected_age_range[0]) & (df['Age'] <= selected_age_range[1])]
    else:
        filtered_df = df[df['Gender'].isin(selected_groups)]

    # Bar chart for distribution of customers by age or gender
    bar_chart = px.histogram(filtered_df, x=selected_demographic, title=f'Distribution of Customers by {selected_demographic}',
                                    labels={selected_demographic: selected_demographic, 'count': 'Count'},
                                    category_orders={'Gender': selected_groups} if selected_demographic == 'Gender' else None,
                                    color_discrete_sequence=px.colors.qualitative.D3_r, template="plotly_dark")
    bar_chart.update_layout( title_x=0.5,bargap=0.2)

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

#TAB-2
@app.callback(
    [Output('purchase-date-chart', 'figure'),
     Output('average-quantity-chart', 'figure'),
     Output('product-category-chart', 'figure'),
     Output('total-purchase-distribution', 'figure')],
    [Input('time-interval-dropdown', 'value')]
)
    

def update_graphs(selected_interval):
    
    # Resample data based on the selected time interval
    df_resampled = df.set_index('Purchase Date').resample(selected_interval).count().reset_index()

    # Frequency distribution of purchase dates
    fig_purchase_date = px.line(df_resampled, x='Purchase Date', y='Customer ID', title='Frequency Distribution of Purchase Dates', color_discrete_sequence=px.colors.qualitative.Vivid,template="plotly_dark")

    # Average quantity of products purchased
    fig_average_quantity = px.bar(df_resampled, x='Purchase Date', y='Quantity', title='Average Quantity of Products Purchased', color_discrete_sequence=px.colors.qualitative.Safe,template="plotly_dark")
    # Most popular product categories and their average prices
    fig_product_category = px.histogram(df, x='Product Price', color='Product Category', nbins=30,title='Distribution of Product Prices by Category',color_discrete_sequence=px.colors.qualitative.Antique,template='plotly_dark')
    fig_product_category.update_layout( title_x=0.5,bargap=0.2)
    # Distribution of total purchase amounts
    fig_total_purchase_distribution = px.histogram(df, x='Total Purchase Amount', title='Distribution of Total Purchase Amounts', color_discrete_sequence= px.colors.qualitative.Light24,template="plotly_dark")
    return fig_purchase_date, fig_average_quantity, fig_product_category, fig_total_purchase_distribution

#TAB-3
# Callback to update graphs based on dropdown selection
@app.callback(
    [Output('payment-pie-chart', 'figure'),
     Output('average-purchase-bar-chart', 'figure'),
     Output('correlation-scatter-plot', 'figure')],
    [Input('payment-method-dropdown', 'value')]
)
def tab3_update_graphs(selected_payment_methods):
    # Filter data based on selected payment methods
    filtered_df = df[df['Payment Method'].isin(selected_payment_methods)]

    # Pie chart showing the percentage of the selected payment methods
    pie_chart = px.pie(filtered_df, names='Payment Method', title=f'Distribution of Selected Payments',
                       color_discrete_sequence=px.colors.qualitative.Set1,template="plotly_dark")
    pie_chart.update_layout(title_x=0.5)
    # Bar chart with payment methods on X-axis, average purchase amount on Y-axis
    bar_chart = px.histogram(filtered_df, x='Total Purchase Amount',
                               title='Distribution of Total Purchase Amount for Selected Payments',
                               color='Payment Method', color_discrete_sequence=px.colors.qualitative.Set2,
                               marginal='rug',  # Add marginal rug plots for better visibility
                               template="plotly_dark")
    bar_chart.update_layout(title_x=0.5,bargap=0.1)
    # Scatter plot with payment methods on X-axis, product category/price on Y-axis
    scatter_plot = px.scatter(filtered_df, x='Payment Method', y='Product Price', color='Product Category',
                              title='Correlation between Selected Payments and Product Category/Price',
                              color_discrete_sequence=px.colors.qualitative.Set3,template="plotly_dark")
    scatter_plot.update_layout(title_x=0.5)
    return pie_chart, bar_chart, scatter_plot

#TAB-4
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

#TAB-5
# Callbacks for dynamic updates based on user input
@app.callback(
    [Output('churn-by-category-chart', 'figure'),
     Output('total-customers', 'children'),
     Output('churn-rate', 'children')],
    [Input('productcategory-dropdown', 'value')]
)
def update_churn_by_category(selected_category):
    filtered_df = df[df['Product Category'] == selected_category]
    churn_by_category_fig = px.line(
        filtered_df,
        x='Churn',
        y='Total Purchase Amount',  # Change this to a relevant column for the y-axis
        title=f'Churn Rate for {selected_category}',
        color='Churn',
        labels={'Total Purchase Amount': 'Y-axis Label'} ,template="plotly_dark" # Change Y-axis label
    )
    churn_by_category_fig.update_layout(title_x=0.5)
    total_customers = len(filtered_df)
    churn_rate = round(filtered_df['Churn'].mean() * 100, 2)
    return churn_by_category_fig, total_customers, churn_rate

#TAB-6
@app.callback(
    Output('analysis-result', 'figure'),
    [Input('analysis-type', 'value')]
)
def update_graph(selected_analysis):
    if selected_analysis == 'avg_transactions':
        # Calculate average transactions per customer
        avg_transactions = df.groupby('Customer ID')['Purchase Date'].count().mean()

        # Create a simple bar chart
        fig = px.bar(x=['Average Transactions per Customer'], y=[avg_transactions], title='Average Transactions per Customer',template="plotly_dark" ,color_discrete_sequence=[px.colors.qualitative.Plotly[0]])
        fig.update_layout(title_x=0.5)

    elif selected_analysis == 'avg_time_between_purchases':
        # Calculate average time between consecutive purchases
        # (You'll need to adjust this based on your specific date columns)
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
        df['Time Between Purchases'] = df.groupby('Customer ID')['Purchase Date'].diff().mean()

        # Create a histogram
        fig = px.histogram(df, x='Time Between Purchases', nbins=50, title='Average Time Between Consecutive Purchases',template="plotly_dark", color_discrete_sequence=[px.colors.qualitative.Plotly[1]])
        fig.update_layout(title_x=0.5)
    elif selected_analysis == 'correlation':
        # Calculate correlation between total purchase amount and churn
        # (You'll need to adjust this based on your specific columns)
        fig = px.scatter(df, x='Total Purchase Amount', y='Churn', title='Correlation between Total Purchase Amount and Churn',template="plotly_dark", color_discrete_sequence=[px.colors.qualitative.Plotly[2]])
        fig.update_layout(title_x=0.5)

    elif selected_analysis == 'loyal_customers':
        # Identify potential loyal customers
        threshold_frequency = 3  # Define your threshold for purchase frequency
        threshold_amount = 1000  # Define your threshold for total purchase amount

        loyal_customers = df.groupby('Customer ID').agg({'Total Purchase Amount': 'sum', 'Purchase Date': 'count'})
        loyal_customers = loyal_customers[(loyal_customers['Total Purchase Amount'] > threshold_amount) & (loyal_customers['Purchase Date'] > threshold_frequency)]

        # Create a scatter plot or table
        fig = px.scatter(loyal_customers, x='Total Purchase Amount', y='Purchase Date', title='Identify Potential Loyal Customers', color_discrete_sequence=[px.colors.qualitative.Plotly[3]])
        fig.update_layout(title_x=0.5)

    return fig

#TAB -7
@app.callback(
    Output('total-sales-graph', 'figure'),
    Output('product-category-sales-graph', 'figure'),
    Output('returns-over-time-graph', 'figure'),
    Input('time-period-dropdown', 'value'),
    Input('product-category-radio', 'value')
)
def update_graphs(selected_time_period, selected_category):
    # Filter data based on selected product category
    filtered_df = df[df['Product Category'] == selected_category]

    # a. Monthly or weekly trends in total sales
    total_sales_fig = px.line(filtered_df, x='Purchase Date', y='Total Purchase Amount', 
                              labels={'Total Purchase Amount': 'Total Sales'},template="plotly_dark",
                              title=f'Trends in Total Sales ({selected_time_period})',
                              color_discrete_sequence=[px.colors.qualitative.Plotly[0]])
    total_sales_fig.update_layout(title_x=0.5)
    # b. Seasonal patterns in selected product category sales
    product_category_sales_fig = px.line(filtered_df, x='Purchase Date', y='Total Purchase Amount', template="plotly_dark",labels={'Total Purchase Amount': 'Total Sales'},
    title=f'Seasonal Patterns in {selected_category} Sales',color_discrete_sequence=[px.colors.qualitative.Plotly[1]])
    product_category_sales_fig.update_layout(title_x=0.5)
    # c. Trends in returns over time
    returns_over_time_fig = px.line(filtered_df, x='Purchase Date', y='Returns',template="plotly_dark",labels={'Returns': 'Count of Returns'},title=f'Trends in Returns Over Time ({selected_category})',color_discrete_sequence=[px.colors.qualitative.Plotly[2]])

    returns_over_time_fig.update_layout(title_x=0.5)

    return total_sales_fig, product_category_sales_fig, returns_over_time_fig

#TAB-8
@app.callback(
    Output('segment-scatter', 'figure'),
    Output('revenue-chart', 'figure'),
    Output('strategy-text', 'children'),
    Input('segment-dropdown', 'value')
)
def update_plots(selected_segment):
    # Update 'Segment' column based on selected segment
    df['Segment'] = selected_segment

    # Update scatter plot based on 'Segment' column
    scatter_fig = px.scatter(df, x='Customer Age', y='Total Purchase Amount', color='Segment',size='Quantity', hover_data=['Customer Name'], title='Customer Segmentation',color_discrete_map=color_map, template="plotly_dark")  
    scatter_fig.update_layout( title_x=0.5)
    # Update revenue chart based on 'Segment' column
    revenue_fig = px.histogram(df, x='Total Purchase Amount', color='Segment', nbins=30,title='Distribution of Total Purchase Amount by Segment',
    template='plotly_dark',color_discrete_map=color_map)
    revenue_fig.update_layout( title_x=0.5,bargap=0.2)

    # Display strategies based on selected segment
    strategies = get_strategies(selected_segment)

    return scatter_fig, revenue_fig, strategies

def get_strategies(segment):
    # Function to get strategies based on the selected segment
    # You can customize this based on your business logic
    if segment == 'Purchase Behavior':
        return "Implement personalized product recommendations."
    elif segment == 'Demographic Info':
        return "Launch targeted marketing campaigns based on demographic characteristics."
    elif segment == 'Churn Status':
        return "Implement customer retention programs for at-risk customers."
    else:
        return "No specific strategy available."

#TAB-9 Download
@app.callback(
    Output("download-data", "data"),
    [Input("csv-button", "n_clicks")],
    [State("column-checklist-row1", "value"),
     State("column-checklist-row2", "value")]
)
def download_data(n_clicks, selectedChecklist1, selectedChecklist2):
    if n_clicks > 0:
        # Copy the DataFrame to avoid modifying the original DataFrame
        dfCopy = df.copy()

        # Combine selected columns from both rows
        selected_columns = selectedChecklist1 + selectedChecklist2

        # Drop selected columns
        dfCopy = dfCopy.drop(columns=selected_columns)

        # Create a CSV string for the modified dataset
        csv_string = dfCopy.to_csv(index=False, encoding='utf-8')

        # Return a dictionary specifying data and filename for download
        return dcc.send_data_frame(dfCopy.to_csv, filename="E-commercedataset.csv", index=False)

    # Return PreventUpdate to prevent updating the download when the button is not clicked
    raise PreventUpdate

#TAB-10
# Define callback to update graphs based on dropdown selections
@app.callback(
    [Output('scatter-plot1', 'figure'),
     Output('pie-chart1', 'figure'),
     Output('bar-chart1', 'figure')],
    [Input('customer-dropdown1', 'value'),
     Input('product-category-dropdown1', 'value')]
)
def update_graphs(selected_customer, selected_category):
    # Filter DataFrame based on selected values
    filtered_df = df[(df['Customer Name'] == selected_customer) & (df['Product Category'] == selected_category)]

    # Scatter Plot
    scatter_plot = px.scatter(filtered_df, x='Customer Age', y='Total Purchase Amount', color='Gender', size='Quantity',title='Customer Age vs. Total Purchase Amount',color_discrete_sequence=[px.colors.qualitative.Dark24])
    scatter_plot.update_layout(
        plot_bgcolor='#f8f9fa',  # Background color
        paper_bgcolor='#f8f9fa',  # Plot area color
        font_color='#495057',  # Text color
        title_x=0.5
    )

    # Pie Chart
    pie_chart = px.pie(filtered_df, names='Payment Method', title='Payment Method Distribution')
    pie_chart.update_layout(
        plot_bgcolor='#f8f9fa',  # Background color
        paper_bgcolor='#f8f9fa',  # Plot area color
        font_color='#495057',  # Text color
        title_x=0.5
    )

    # Bar Chart
    bar_chart = px.bar(filtered_df, x='Purchase Date', y='Total Purchase Amount', title='Total Purchase Amount Over Time',color_discrete_sequence=[px.colors.qualitative.Prism])
    bar_chart.update_layout(
        plot_bgcolor='#f8f9fa',  # Background color
        paper_bgcolor='#f8f9fa',  # Plot area color
        font_color='#495057',  # Text color
        title_x=0.5
    )
    

    return scatter_plot, pie_chart, bar_chart

#TAB-11
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
