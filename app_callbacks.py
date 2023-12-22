#Houses the logic for the interactive components of your Dash app. For example, if you have a dropdown to select a date range, the callback to update your graphs would go here.

from dash.dependencies import Input, Output, State
import json
from plotly import graph_objects as go
from data_processing import process_data
from dash import Dash
from transactionDictionary import add_transaction
from transactionDictionary import transaction_dict

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
    Output('unknown_transactions_dropdown', 'options'),
    [Input('intermediate_storage', 'children')]
)
    def update_unknown_transactions_dropdown(json_data):
        transactions = json.loads(json_data)
        options = [{'label': key, 'value': key} for key in transactions.keys()]
        return options


    @app.callback(
        Output('assignment_output', 'children'),
        Output('intermediate_storage', 'children'),  # Update the intermediate storage
        Input('assign_category_button', 'n_clicks'),
        State('category_dropdown', 'value'),
        State('unknown_transactions_dropdown', 'value'),
        State('intermediate_storage', 'children')  # Current state of unknown transactions
    )
    def assign_category(n_clicks, selected_category, selected_transaction, json_data):
        if n_clicks and selected_category and selected_transaction:
            add_transaction(selected_transaction, selected_category)

            # Load the current unknown transactions, remove the assigned one, and update the list
            current_transactions = json.loads(json_data)
            if selected_transaction in current_transactions:
                del current_transactions[selected_transaction]

            updated_transactions_json = json.dumps(current_transactions)
            return f"Assigned {selected_transaction} to {selected_category}", updated_transactions_json
        return "No assignment made", json_data