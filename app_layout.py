#Contains the layout of your Dash app. All your HTML and Dash components would go here.

from dash import dcc, html
from transactionDictionary import transaction_dict

#Create a list of unique categories
unique_categories = list(set(transaction_dict.values()))

layout = html.Div([
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in unique_categories],
        value=unique_categories[0]  # default value
    ),
    dcc.Graph(id='spending-bar-graph'),
    html.Button('Submit', id='submit-button'),
    html.Button('Update Graph', id='update-button'),
    html.Div(id='unknown-list'),  # This will display unknown descriptions
    html.Div(id='output')         # This will display output messages
    
])