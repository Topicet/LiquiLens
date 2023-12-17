#Houses the logic for the interactive components of your Dash app. For example, if you have a dropdown to select a date range, the callback to update your graphs would go here.

from dash.dependencies import Input, Output, State
from plotly import graph_objects as go
from data_processing import process_data
from dash import Dash

def register_callbacks(app: Dash):

    @app.callback(
    Output('output-div', 'children'),  # Output goes to 'output-div'
    [Input('update-data-button', 'n_clicks')]  # Triggered by 'update-data-button'
    )    
    def update_data(n_clicks):
        category_amount_dict, unknown_transactions = {}, {}  # Initialize to empty dictionaries
        if n_clicks is not None:
            category_amount_dict, unknown_transactions = process_data()
        return f"Data updated! Categories: {category_amount_dict}, \n Unknowns: {unknown_transactions}"
    
    