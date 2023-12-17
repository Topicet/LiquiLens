#Contains the layout of your Dash app. All your HTML and Dash components would go here.

from dash import dcc, html
from transactionDictionary import transaction_dict

#Create a list of unique categories
unique_categories = list(set(transaction_dict.values()))

layout = html.Div([
    html.Button('Update Data', id='update-data-button'),
    html.Div(id='output-div')
])

