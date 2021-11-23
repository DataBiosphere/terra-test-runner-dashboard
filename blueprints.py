from dash import html

import test_runner_components
from api.workspacemanager.views import workspacemanager
from app import app

# TODO: The dashboard.py will eventually be replaced by this app when ready
if __name__ == '__main__':
    app = app.start("trdash")

    app.layout = html.Div([
        html.Div([html.Div("Test tooltip")],
                 **{'data-for': 'element-id1', 'data-tip': 'true'}),
        test_runner_components.TooltipsTheme1(
            id='input',
            label='my-label'
        )
    ])

    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
