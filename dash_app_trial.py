from dash import Dash, html

application = Dash(__name__)

application.layout = html.Div([
    html.Div(children='Hello World')
])

if __name__ == '__main__':
    application.run(debug=True)
