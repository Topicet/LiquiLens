"""
This module contains the callback functions for the Dash application. 
These functions define the app's interactivity by updating the app's 
components in response to user inputs. The functions are registered 
to the app in the `register_callbacks` function.
"""

# Standard library imports
import json

# Related third party imports
import dash
from dash import Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly import graph_objects as go

# Local application/library specific imports
from data_processing import *
from transactionDictionary import add_transaction

def register_callbacks(app: Dash):
    @app.callback(
        Output('bar-graph', 'figure'),  # Output for the bar graph
        Output('intermediate_storage', 'children'),  # Output for storing unknown transactions
        [Input('update-data-button', 'n_clicks')]  # Button to update data
    )
    def update_bar_graph(n_clicks):
        if n_clicks is not None:

            known_Transactions, unknown_Transactions = processData()

            # Extract categories and corresponding amounts from the dictionary
            categories = list(known_Transactions.keys())
            amounts = list(known_Transactions.values())

            # Create a bar graph
            bar_graph = go.Figure(
                data=[go.Bar(
                    x=categories, 
                    y=amounts,                    
                    text=amounts,
                    marker=dict(color='royalblue'),  
                    )],
                layout=go.Layout(
                    title="Expenditure Amounts by Category",
                    xaxis=dict(
                        title="Categories",
                        title_font=dict(size=24, family='Tommy')
                    ),
                    yaxis=dict(
                        title="Amount",
                        title_font=dict(size=24, family='Tommy'),
                        range=[-1000, 1000]
                    ),
                    autosize=False,
                    dragmode=False,                    
                )
            )
            return bar_graph, json.dumps(unknown_Transactions)
        
        else: return {}


    @app.callback(
        Output('positiveCashFlowTable', 'data'),
        Input('update-data-button', 'n_clicks')
    )
    def updatePositiveCashFlowTable(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        data = createPositiveCashFlowDictionary()

        return [data]

    @app.callback(
        Output('negativeCashFlowTable', 'data'),
        Input('update-data-button', 'n_clicks')
    )
    def updateNegativeCashFlowTable(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        data = createNegativeCashFlowDictionary()

        return [data]

    @app.callback(
        Output('netCashFlowTable', 'data'),
        Input('update-data-button', 'n_clicks')
    )
    def updateNetCashFlowTable(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        data = createNetCashFlowDictionary()

        return [data]

    @app.callback(
        Output('incomeToExpenseRatioTable', 'data'),
        Input('update-data-button', 'n_clicks')
    )
    def updateIncomeToExpenseRatioTable(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        data = createIncomeToExpenseRatioDictionary()

        return [data]
    
    @app.callback(
        [Output('categories-table', 'columns'),
        Output('categories-table', 'data')],
        [Input('update-data-button', 'n_clicks')]
    )
    def updateCategoriesTable(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        categories_columns, categories_data = createCategoryDataTable()
        
        return categories_columns, categories_data

    @app.callback(
    Output('unknown_Transactions_dropdown', 'options'),
    Input('intermediate_storage', 'children'),
    Input('updated_intermediate_storage', 'children'),
)
    def update_unknown_Transactions_dropdown(json_data, new_json_data):

        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == 'intermediate_storage':
            transactions = json.loads(json_data)

        elif trigger_id == 'updated_intermediate_storage':
            transactions = json.loads(new_json_data)

        options = [{'label': key, 'value': key} for key in transactions.keys()]
        return options


    @app.callback(
        Output('assignment_output', 'children'),
        Output('updated_intermediate_storage', 'children'),  # Output for storing unknown transactions
        Input('assign_category_button', 'n_clicks'),
        Input('intermediate_storage', 'children'),
        State('category_dropdown', 'value'),
        State('unknown_Transactions_dropdown', 'value'),
    )
    def assign_category(n_clicks, json_data, selected_category, selected_unknown_transaction):
        if n_clicks and selected_category and selected_unknown_transaction:
            add_transaction(selected_unknown_transaction, selected_category)

            # Load the JSON data into a Python object
            data = json.loads(json_data)

            # Check if the selected transaction is in the dictionary
            if selected_unknown_transaction in data:
                # Remove the selected transaction
                del data[selected_unknown_transaction]

            # Dump the updated data back into a JSON string
            json_data = json.dumps(data)

        return None, json_data