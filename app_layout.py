# Contains the layout of your Dash app. All your HTML and Dash components would go here.
from dash import dcc, html
from transactionDictionary import transaction_dict
from dash import dash_table
import pandas as pd


predefined_categories = sorted(list(set(transaction_dict.values())))

layout = html.Div([
    html.Button('Update Data', id='update-data-button', n_clicks=0, style={'margin-bottom': '20px', 'background-color': 'royalblue', 'color': 'white'}),
    dcc.Graph(id='bar-graph'),  # This is where the graph will be displayed
    html.Div(id='output-div'),

    html.Div(id='intermediate_storage', style={'display': 'none'}),
    html.Div(id='updated_intermediate_storage', style={'display': 'none'}),

    
    dash_table.DataTable(
        id='category-spending-table',
        columns=pd.DataFrame,  # Empty columns initially
        data= pd.DataFrame,  # Empty data initially
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    ),


    html.Div([
        dcc.Dropdown(
            id='unknown_transactions_dropdown',  # Dropdown to select unknown transactions
            options=[],  # Initially empty, will be populated dynamically
            placeholder='Select an unknown transaction',
        ),
        dcc.Dropdown(
            id='category_dropdown',  # Dropdown to select categories
            options=[{'label': category, 'value': category} for category in predefined_categories],
            placeholder='Select a category',
        ),
        html.Button('Assign Category', id='assign_category_button', n_clicks=0),

        html.Div(id='assignment_output')  # This Div will display the result of the assignment
    ])
])
