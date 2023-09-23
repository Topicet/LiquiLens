#Houses the logic for the interactive components of your Dash app. For example, if you have a dropdown to select a date range, the callback to update your graphs would go here.

from dash.dependencies import Input, Output, State
from plotly import graph_objects as go
from data_processing import process_data
from dash import Dash

def register_callbacks(app: Dash):
    @app.callback(
        Output('output', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('category-dropdown', 'value')]
    )
    @app.callback(
    Output('some-output-div', 'children'),
    [Input('update-data-button', 'n_clicks')]
    )

    def update_transaction_dict(n_clicks, selected_category):
        if n_clicks is None:
            return "Please select categories for unknown descriptions."
        
        # Update transaction_dict here
        # You can access the selected_category which holds the category selected from the dropdown
        # transaction_dict[unknown_description] = selected_category
        
        return f"Updated category: {selected_category}"   

    

    def update_data(n_clicks):
        if n_clicks is not None:
            category_amount_dict, unknown_transactions = process_data()
        return f"Data updated! Categories: {category_amount_dict}, Unknowns: {unknown_transactions}"
    
    