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
])

# In app_layout.py
html.Button('Update Data', id='update-data-button'),