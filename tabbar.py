import test_runner_components
from dash import Dash
import dash_html_components as html

app = Dash(__name__)

app.layout = html.Div([
    test_runner_components.TabBar(id='clickcount')
])

if __name__ == '__main__':
    app.run_server(debug=True)
