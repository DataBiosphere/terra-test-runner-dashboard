import asyncio
from datetime import datetime, timedelta, date

import pytz
from dash import Output, Input, callback_context
from dash.dcc import DatePickerSingle, Dropdown
from dash.html import Div, Header, H1, A, Main, Section, Label, Nav, H5, Table, Thead, Tr, Th, Tbody, Td

from api.routes.test_run_summary import all_summaries
from api.workspacemanager.views import workspacemanager
from app import app


def get_time():
    est = datetime.today().astimezone(pytz.timezone("US/Eastern"))
    # minus_days  = random.randint(1, 10)
    minus_days = 0
    est = est - timedelta(days=minus_days)
    y = est.year
    m = est.month
    d = date(est.year, est.month, est.day)
    return {'US/Eastern': est, 'd': d, 'Y': y, 'm': m}


# TODO: The dashboard.py will eventually be replaced by this app when ready


if __name__ == '__main__':
    app = app.start("trdash")

    #    with app.server.app_context():
    #        summaries = asyncio.run(test_run_summaries_today())

    #    summary_cards = [SummaryCard(id=u.id, testSuiteName=u.testSuiteName,
    #                                 testScriptName=u.testScriptResultSummaries[0]['testScriptName'],
    #                                 totalRun=u.testScriptResultSummaries[0]['totalRun'],
    #                                 numCompleted=u.testScriptResultSummaries[0]['numCompleted'],
    #                                 numExceptionsThrown=u.testScriptResultSummaries[0]['numExceptionsThrown'],
    #                                 serverSpecificationFile=u.testConfiguration['serverSpecificationFile'])
    #                     for u in summaries]

    app.layout = Div([
        #        html.Div([html.Div("Test tooltip")],
        #                 **{'data-for': 'element-id1', 'data-tip': 'true'}),
        #        test_runner_components.TooltipsTheme1(
        #            id='input',
        #            label='my-label'
        #        ),
        # MainDash(summary_cards,
        #         id='main-dash',
        #         isPrintModal=False
        #         ),
        Div([
            Header(
                H1(
                    A('Test Runner Dashboard', href='/', tabIndex=-1),
                    **{'aria-label': 'Go to home page.'}, className='app__title'),
                className='app__header', role='banner'),
            Main(
                Div(
                    [Div(
                        Section(
                            Div(
                                Div([Div([Div([
                                    Label('Date:', className='mb-0', htmlFor='test-date-picker'),
                                    Div(DatePickerSingle(id='test-date-picker', className='custom-input',
                                                         min_date_allowed=date(2021, 11, 29),
                                                         max_date_allowed=get_time()['d'],
                                                         initial_visible_month=datetime(get_time()['Y'],
                                                                                        get_time()['m'],
                                                                                        1),
                                                         date=get_time()['d'], day_size=24),
                                        className='root-account-list__account-type-select')
                                ], className='root-account-list__account-type-dropdown')],
                                    className='root-account-list__dropdown-bar'),
                                    Div(Div([Label('Env type:', className='mb-0', htmlFor='env-type'),
                                             Div(Dropdown(id='test-env-selector', className='custom-input',
                                                          options=[{'label': 'alpha', 'value': 'workspace-alpha.json'},
                                                                   {'label': 'dev', 'value': 'workspace-dev.json'},
                                                                   {'label': 'wsmtest',
                                                                    'value': 'workspace-wsmtest.json'}],
                                                          clearable=False, style={'width': '60px !important'},
                                                          optionHeight=24, placeholder=None),
                                                 className='root-account-list__account-type-select')],
                                            className='root-account-list__account-type-dropdown'),
                                        className='root-account-list__dropdown-bar')],
                                    className='root-account-list__filter-controls'),
                                className='root-account-list__header'),
                            className='env-list', role='region'),
                        className='home__sidebar'),
                        Div(
                            [Div(
                                [Div(
                                    Nav([
                                        A('Summary', href='#', id='a-summaries',
                                          className='navigation-tabs__tab pt-3 navigation-tabs__tab--active',
                                          style={'textDecoration': 'none'}, **{'aria-current': 'page'}),
                                        A('Results', href='#', id='a-results',
                                          className='navigation-tabs__tab pt-3',
                                          style={'textDecoration': 'none'}),
                                        A('Charts', href='#', id='a-charts', className='navigation-tabs__tab pt-3',
                                          style={'textDecoration': 'none'})
                                    ], className='navigation-tabs pt-1 px-4'),
                                    className='shadow-scroller__head d-flex flex-column bg-white flex-shrink-0 '
                                              'account-detail__navigation'),
                                    Div(Section(id='output-detail',
                                                className='account-spending-details p-4', role='region'),
                                        className='shadow-scroller__body flex-grow-1 overflow-none '
                                                  'account-detail__content')
                                ],
                                className='shadow-scroller d-flex flex-column bg-white account-detail'),
                            ],
                            className='root-detail__content')],
                    className='home'),
                className='app__content', role='main'),
        ], id='main-dash', className='app'),
    ], id="root")


    @app.callback(
        Output(component_id='output-detail', component_property='children'),
        Input(component_id='test-date-picker', component_property='date'),
        Input(component_id='test-env-selector', component_property='value'),
        Input(component_id='a-summaries', component_property='n_clicks'),
        Input(component_id='a-results', component_property='n_clicks')
    )
    def update_results(d, e, summaries, results):
        ctx = callback_context
        nav_tabs_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(f"{nav_tabs_id}")
        output_detail = []
        with app.server.app_context():
            # testsuite = asyncio.run(distinct_testsuite(d, e))
            all_results = asyncio.run(all_summaries(d, e))
            # results = asyncio.run(test_run_summaries(d, e, testsuite[0]))
        if all_results:
            if nav_tabs_id == 'a-summaries':
                for testsuite in all_results:
                    tot_testcase_pass = 0
                    tot_testcase = 0
                    output_detail.append(H5(testsuite, className='section-header'))
                    for y in [x.testScriptResultSummaries for x in all_results[testsuite]]:
                        tot_testcase += len(y)
                        for s in y:
                            print(f"testScriptName: {s['testScriptName']}")
                            tot_testcase_pass += s['numCompleted'] == s['totalRun']
                    tot_pass = sum(
                        map(lambda x: x.testScriptResultSummaries[0]['numCompleted'], all_results[testsuite]))
                    tot = sum(map(lambda x: x.testScriptResultSummaries[0]['totalRun'], all_results[testsuite]))
                    shortRefHeadCommit = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                        'shortRefHeadCommit']
                    remoteOriginUrl = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                        'remoteOriginUrl']
                    refHeadCommit = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0]['refHeadCommit']
                    helmVersions = all_results[testsuite][0].versionScriptResults[0]['helmVersions'][0][
                        'helmAppVersion']
                    end = all_results[testsuite][0].startTimestamp.strftime("%m/%d/%Y, %H:%M:%S")
                    begin = all_results[testsuite][-1].startTimestamp.strftime("%m/%d/%Y, %H:%M:%S")
                    output_detail.append(Div(Div([Div(Table(Thead(
                        [Tr([Th(Div('Duration',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('Total test run(s)',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('% pass',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('Git Version',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('Helm Version',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col')
                             ])]),
                        className='transactions-table__head'),
                        className='transactions-table__head-wrapper'),
                        Div(className='transactions-table__head-wrapper'),
                        Div(Table(Tbody([Tr([Td(f"{begin} - {end}",
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(tot_testcase,
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(f"{tot_testcase_pass / tot_testcase:.0%}",
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(A(shortRefHeadCommit,
                                                  href=f"{remoteOriginUrl}/commit/{refHeadCommit}",
                                                  className='Link--secondary text-monospace ml-2 d-none d-lg-inline',
                                                  target='_blank'),
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(helmVersions,
                                                className='transactions-table__body-col',
                                                style={'width': '20%'})],
                                            className='transactions-table__body-row '
                                                      'transactions-table__body-row--expandable')]),
                                  className='transactions-table__body'),
                            className='transactions-table__body-wrapper',
                            style={'height': '100%'})],
                        className='transactions-table__table'),
                        className='transactions-table'))
                return output_detail
            elif nav_tabs_id == 'a-results':
                for testsuite in all_results:
                    output_detail.append(H5(testsuite, className='section-header'))
                    output_detail.append(Div(Div([Div(Table(Thead(
                        [Tr([Th(Div('Test case',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('Total pass',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('% pass',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('Git Version',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col'),
                             Th(Div('Helm Version',
                                    className='transactions-table__col-label'),
                                className='transactions-table__head-col')
                             ])]),
                        className='transactions-table__head'),
                        className='transactions-table__head-wrapper'),
                        Div(className='transactions-table__head-wrapper'),
                        Div(Table(Tbody([Tr([Td(u.testScriptResultSummaries[0]['testScriptName'],
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(u.testScriptResultSummaries[0]['numCompleted'],
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(f"{u.testScriptResultSummaries[0]['numCompleted'] / u.testScriptResultSummaries[0]['totalRun']:.0%}",
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(A(u.versionScriptResults[1]['gitVersions'][0]['shortRefHeadCommit'],
                                                  href=f"{u.versionScriptResults[1]['gitVersions'][0]['remoteOriginUrl']}/commit/{u.versionScriptResults[1]['gitVersions'][0]['refHeadCommit']}",
                                                  className='Link--secondary text-monospace ml-2 d-none d-lg-inline',
                                                  target='_blank')
                                                if len(u.versionScriptResults[1]['gitVersions']) > 0
                                                else f"{u.versionScriptResults[1]['helmVersions'][0]['helmAppVersion']}",
                                                className='transactions-table__body-col',
                                                style={'width': '20%'}),
                                             Td(A(u.versionScriptResults[0]['gitVersions'][0]['shortRefHeadCommit'],
                                                  href=f"{u.versionScriptResults[0]['gitVersions'][0]['remoteOriginUrl']}",
                                                  className='Link--secondary text-monospace ml-2 d-none d-lg-inline')
                                                if len(u.versionScriptResults[0]['gitVersions']) > 0
                                                else f"{u.versionScriptResults[0]['helmVersions'][0]['helmAppVersion']}",
                                                className='transactions-table__body-col',
                                                style={'width': '20%'})],
                                            className='transactions-table__body-row '
                                                      'transactions-table__body-row--expandable') for u in
                                         all_results[testsuite]]),
                                  className='transactions-table__body'),
                            className='transactions-table__body-wrapper')],
                        className='transactions-table__table'),
                        className='transactions-table'))
                return output_detail
        else:
            return ['No results']


    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
