#Houses the logic for the interactive components of your Dash app. For example, if you have a dropdown to select a date range, the callback to update your graphs would go here.

from dash.dependencies import Input, Output, State
from plotly import graph_objects as go
from data_processing import process_data
from dash import Dash
from transactionDictionary import add_transaction
from transactionDictionary import transaction_dict

predefined_categories = sorted(list(set(transaction_dict.values())))
unknown_transactions = {}

def register_callbacks(app: Dash):
    @app.callback(
        Output('bar-graph', 'figure'),  # Update the 'bar-graph' component
        [Input('update-data-button', 'n_clicks')]  # Triggered by 'update-data-button'
    )
    def update_bar_graph(n_clicks):
        if n_clicks is not None:
            category_amount_dict, unknown_transactions = process_data()  # Ignore 'unknown_transactions' for now

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

            return bar_graph
        else:
            return {}

    @app.callback(
        Input('assign-category-button', 'n_clicks'),
        Output('unknown-transactions', 'children'),
        Output('unknown-transactions-dropdown', 'options'),
        Output('category-dropdown', 'options'),
        Output('category-dropdown', 'value'),
        State('category-dropdown', 'value'),
        State('unknown-transactions-dropdown', 'value'),
        State('unknown-transactions', 'children'),
    )
    def assign_category(n_clicks, selected_category, unknown_transactions):
        if n_clicks and selected_category and unknown_transactions:
            # Update the data structure with the selected category
            add_transaction(unknown_transactions, selected_category)
        return unknown_transactions, [{'label': category, 'value': category} for category in predefined_categories], None