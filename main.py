#The entry point of your application. You'd import the above modules and tie everything together here. This is the script you'd run to start your Dash app.
from dash import Dash
from app_layout import layout
from app_callbacks import *

app = Dash(__name__)
app.layout = layout

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)