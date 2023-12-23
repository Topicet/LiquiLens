#Houses the logic for the interactive components of your Dash app. For example, if you have a dropdown to select a date range, the callback to update your graphs would go here.

from dash.dependencies import Input, Output, State
import json
from plotly import graph_objects as go
from data_processing import *
from dash import Dash
import dash
from transactionDictionary import add_transaction
from dash.exceptions import PreventUpdate
from transactionDictionary import transaction_dict
import pandas as pd

predefined_categories = sorted(list(set(transaction_dict.values())))

def register_callbacks(app: Dash):
    @app.callback(
        Output('bar-graph', 'figure'),  # Output for the bar graph
        Output('intermediate_storage', 'children'),  # Output for storing unknown transactions
        [Input('update-data-button', 'n_clicks')]  # Button to update data
    )
    def update_bar_graph(n_clicks):
        if n_clicks is not None:
            category_amount_dict, unknown_transactions = process_data()

            # Extract categories and corresponding amounts from the dictionary
            categories = list(category_amount_dict.keys())
            amounts = list(category_amount_dict.values())

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
                            title_font=dict(size=24, family='Courier New, monospace')
                        ),
                        yaxis=dict(
                            title="Amount",
                            title_font=dict(size=24, family='Courier New, monospace'),
                            range=[-500, 500]
                        ),
                        autosize=False,
                        dragmode=False,
                    )
            )

            return bar_graph, json.dumps(unknown_transactions)
        else: return {}

    @app.callback(
        [Output('category-spending-table', 'columns'),
        Output('category-spending-table', 'data')],
        [Input('update-data-button', 'n_clicks')]
    )
    def update_table(n_clicks):
        if n_clicks is None:
            raise PreventUpdate  # If button is not clicked, do not update the table.
        # Assume createDataTable() returns a DataFrame.
        columns, data = createDataTable()
        return columns, data
        

        


    @app.callback(
    Output('unknown_transactions_dropdown', 'options'),
    Input('intermediate_storage', 'children'),
    Input('updated_intermediate_storage', 'children'),
)
    def update_unknown_transactions_dropdown(json_data, new_json_data):

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
        State('unknown_transactions_dropdown', 'value'),
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