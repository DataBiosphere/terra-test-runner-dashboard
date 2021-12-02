from dash import html

from api.workspacemanager.views import workspacemanager
from app import app
from test_runner_components import MainDash, SummaryCard

# TODO: The dashboard.py will eventually be replaced by this app when ready
if __name__ == '__main__':
    app = app.start("trdash")

    app.layout = html.Div([
        #        html.Div([html.Div("Test tooltip")],
        #                 **{'data-for': 'element-id1', 'data-tip': 'true'}),
        #        test_runner_components.TooltipsTheme1(
        #            id='input',
        #            label='my-label'
        #        ),
        MainDash([SummaryCard(testSuiteName='FullIntegration', testScriptName='ServiceStatus',
                              totalRun=10, numCompleted=7, numExceptionsThrown=3, serverSpecificationFile='dev.json'),
                  SummaryCard(testSuiteName='FullIntegration', testScriptName='EnumerateDataRepo',
                              totalRun=5, numCompleted=5, numExceptionsThrown=0, serverSpecificationFile='dev.json')],
                 id='main-dash',
                 isPrintModal=False
                 )
    ], id="root")

    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
