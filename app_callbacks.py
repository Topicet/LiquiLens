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
import plotly.express as px

# Local application/library specific imports
from data_processing import *
from transactionDictionary import add_transaction
import os

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

            # Create a bar graph using plotly express
            bar_graph = px.bar(
                x=categories, 
                y=amounts,
                text=amounts,
                labels={'x': 'Categories', 'y': 'Amount'},
            )
            bar_graph.update_layout(
                xaxis=dict(
                    title="Categories",
                    title_font=dict(size=24, family='Tommy', color='#FFCB9A'),
                    tickfont=dict(color='#FFCB9A')  # Set the color for x-axis label fonts
                ),
                yaxis=dict(
                    title="Amount",
                    title_font=dict(size=24, family='Tommy', color='#FFCB9A'),
                    tickfont=dict(color='#FFCB9A'),  # Set the color for y-axis label fonts
                    range=[-1000, 1000]
                ),
                title={
                    'text': "Expenditure Amounts by Category",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(
                        family="Tommy",  # Specify the font family for the title
                        size=24,  # Specify the font size for the title
                        color="#FFCB9A"
                    )
                },
                autosize=False,
                dragmode=False,
                plot_bgcolor='#F9F5F6',  # This sets the background color outside the bar graph
                paper_bgcolor='#F9F5F6',  # This sets the background color for the entire layout of the graph
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
    
    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def update_output(uploaded_file_content, uploaded_file_name):
        if uploaded_file_content is not None:
            
            absolute_path = os.path.abspath(uploaded_file_name)
            print(absolute_path)
            
            # Write the absolute path to a text file
            with open('file_paths.txt', 'w') as f:
                f.write(absolute_path + '\n')



