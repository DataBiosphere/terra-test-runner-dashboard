import asyncio

from dash import html

from api.routes.test_run_summary import test_run_summaries_today
from api.workspacemanager.views import workspacemanager
from app import app
from test_runner_components import MainDash, SummaryCard

# TODO: The dashboard.py will eventually be replaced by this app when ready
if __name__ == '__main__':
    app = app.start("trdash")

    with app.server.app_context():
        summaries = asyncio.run(test_run_summaries_today())

    summary_cards = [SummaryCard(id=u.id, testSuiteName=u.testSuiteName,
                                 testScriptName=u.testScriptResultSummaries[0]['testScriptName'],
                                 totalRun=u.testScriptResultSummaries[0]['totalRun'],
                                 numCompleted=u.testScriptResultSummaries[0]['numCompleted'],
                                 numExceptionsThrown=u.testScriptResultSummaries[0]['numExceptionsThrown'],
                                 serverSpecificationFile=u.testConfiguration['serverSpecificationFile'])
                     for u in summaries]

    app.layout = html.Div([
        #        html.Div([html.Div("Test tooltip")],
        #                 **{'data-for': 'element-id1', 'data-tip': 'true'}),
        #        test_runner_components.TooltipsTheme1(
        #            id='input',
        #            label='my-label'
        #        ),
        MainDash(summary_cards,
                 id='main-dash',
                 isPrintModal=False
                 )
    ], id="root")

    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
