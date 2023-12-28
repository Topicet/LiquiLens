# Contains the layout of your Dash app. All your HTML and Dash components would go here.
from dash import dcc, html
from transactionDictionary import transactionDict
from dash import dash_table
from dash.dash_table import FormatTemplate

layout = html.Div([

    # Div for the header
    html.Div([

    dash_table.DataTable(
        id='positiveCashFlowTable',        
        columns=[
            {"name": "Positive Cash Flow",
            "id": "positiveCashFlow",
            'type': 'numeric',
            'format': FormatTemplate.money(2)}],           
        data=[],
        style_header={
            'backgroundColor': '#2C3531',
            'fontWeight': 'bold',
            'color': '#d1e8e2',
        },
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'fontSize': '1.2em',
            'padding-left': '10px',
            'padding-right': '10px',
            'font-family':'Tommy'
        },
        style_data={
            'height': '30px',
            'width': '280px',
            'whiteSpace': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    ),

    dash_table.DataTable(
        id='negativeCashFlowTable',
        columns=[{"name": "Negative Cash Flow", "id": "negativeCashFlow", 'type': 'numeric', 'format': FormatTemplate.money(2)}],
        data=[],
        style_header={
            'backgroundColor': '#2C3531',
            'fontWeight': 'bold',
            'color': '#d1e8e2',
        },
        style_cell={
            'textAlign': 'center',
            'height': 'auto',
            'whiteSpace': 'normal',
            'fontSize': '1.2em',
            'padding-left': '10px',
            'padding-right': '10px',
            'font-family':'Tommy'
        },
        style_data={
            'height': '30px',
            'width': '280px',
            'whiteSpace': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    ),

    dash_table.DataTable(
        id='netCashFlowTable',
        columns=[
            {"name": "Net Cash Flow", "id": "netCashFlow", 'type': 'numeric', 'format': FormatTemplate.money(2)}],
        data=[],
        style_header={
            'backgroundColor': '#2C3531',
            'fontWeight': 'bold',
            'color': '#d1e8e2',
        },
        style_cell={
            'textAlign': 'center',
            'height': 'auto',
            'whiteSpace': 'normal',
            'fontSize': '1.2em',
            'padding-left': '10px',
            'padding-right': '10px',
            'font-family':'Tommy'
        },
        style_data={
            'height': '30px',
            'width': '280px',
            'whiteSpace': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    ),

    dash_table.DataTable(
        id='incomeToExpenseRatioTable',
        columns=[
            {"name": "Income to Expense Ratio", "id": "incomeToExpenseRatio", 'type': 'numeric', 'format': FormatTemplate.percentage(2)}],
        data=[],
        style_header={
            'backgroundColor': '#2C3531',
            'fontWeight': 'bold',
            'color': '#d1e8e2',
        },
        style_cell={
            'textAlign': 'center',
            'height': 'auto',
            'whiteSpace': 'normal',
            'fontSize': '1.2em',
            'padding-left': '10px',
            'padding-right': '10px',
            'font-family':'Tommy'
        },
        style_data={
            'height': '30px',
            'width': '280px',
            'whiteSpace': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    ),
    ],  id='headerDiv'),


    html.Button('Update Data', id='update-data-button', n_clicks=0),
    dcc.Graph(id='bar-graph'), 
    html.Div(id='output-div'),

    #Used for holding the hidden data that will be shown in the unknown transactions dropdown.
    html.Div(id='intermediate_storage', style={'display': 'none'}),
    html.Div(id='updated_intermediate_storage', style={'display': 'none'}),





    dash_table.DataTable(
        id='categories-table',
        columns=[],
        data=[],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'center',
            'height': 'auto',
            'whiteSpace': 'normal',
            'fontSize': '1.2em',
        }
    ),


    html.Div([
        dcc.Dropdown(
            id='unknown_Transactions_dropdown',  # Dropdown to select unknown transactions
            options=[],  # Initially empty, will be populated dynamically
            placeholder='Select an unknown transaction',
        ),
        dcc.Dropdown(
            id='category_dropdown',  # Dropdown to select categories
            options=[{'label': category, 'value': category} for category in sorted(list(set(transactionDict.values())))],
            placeholder='Select a category',
        ),
        html.Button('Assign Category', id='assign_category_button', n_clicks=0),

        html.Div(id='assignment_output')  # This Div will display the result of the assignment
    ])
])  
