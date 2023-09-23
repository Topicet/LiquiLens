#Houses the logic for the interactive components of your Dash app. For example, if you have a dropdown to select a date range, the callback to update your graphs would go here.

from dash.dependencies import Input, Output, State
from plotly import graph_objects as go
from data_processing import *
from dash import Dash

def register_callbacks(app: Dash):
    @app.callback(
        Output('output', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('category-dropdown', 'value')]
    )
    @app.callback(
        Output('spending-bar-graph', 'figure'),
        [Input('update-button', 'value')]
    )

    def update_transaction_dict(n_clicks, selected_category):
        if n_clicks is None:
            return "Please select categories for unknown descriptions."
        
        # Update transaction_dict here
        # You can access the selected_category which holds the category selected from the dropdown
        # transaction_dict[unknown_description] = selected_category
        
        return f"Updated category: {selected_category}"
    
    def update_spending_bar_graph(n_clicks):

        figure = go.Figure(data=[
            go.Bar(x=list(category_amount_dict.keys()), y=list(category_amount_dict.values()))
        ])
        figure.update_layout(title='Spending by Category',
                             xaxis_title='Category',
                             yaxis_title='Amount ($)')
        
        return figure