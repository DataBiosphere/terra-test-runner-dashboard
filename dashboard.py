import asyncio
from datetime import datetime, timedelta, date
from os.path import splitext

import pytz
from dash import Output, Input, callback_context
from dash.dcc import DatePickerSingle, Dropdown
from dash.html import Button, Div, Header, H1, A, Main, Section, Label, Nav, H5, Table, Thead, Tr, Th, Tbody, Td

from test_runner_components import SimpleTable, Tooltips

from api.routes.test_run_summary import all_summaries, distinct_test_config, all_service_summaries
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


# Renderers
def datepicker_renderer(component_id, classname, min_date):
    current_datetime = get_time()
    return DatePickerSingle(id=component_id, className=classname,
                            min_date_allowed=min_date,
                            max_date_allowed=current_datetime['d'],
                            initial_visible_month=datetime(current_datetime['Y'], current_datetime['m'], 1),
                            date=current_datetime['d'])


if __name__ == '__main__':
    cols = [
        {'title': 'Start time', 'field': 'startUserJourneyTimestamp', 'type': 'datetime'},
        {'title': 'Name', 'field': 'testScriptName'},
        {'title': 'Pass', 'field': 'numCompleted', 'type': 'numeric'},
        {'title': 'Fail', 'field': 'numExceptionsThrown', 'type': 'numeric'},
        {'title': 'Min [ms]', 'field': 'min', 'type': 'numeric'},
        {'title': 'Max [ms]', 'field': 'max', 'type': 'numeric'},
        {'title': 'Mean [ms]', 'field': 'mean', 'type': 'numeric'},
        {'title': 'Standard deviation [ms]', 'field': 'sd', 'type': 'numeric'},
        {'title': 'p50 [ms]', 'field': 'p50', 'type': 'numeric'},
        {'title': 'p95 [ms]', 'field': 'p95', 'type': 'numeric'}
    ]

    app = app.start("trdash")

    app.layout = Div([
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
                                    Div(id='date-picker-container', className='root-panel-list__env-type-select')
                                ], className='root-panel-list__env-type-dropdown')],
                                    className='root-panel-list__dropdown-bar'),
                                    Div(Div([Label('Env type:', className='mb-0', htmlFor='env-type'),
                                             Div(Dropdown(id='test-env-selector', className='custom-input',
                                                          options=[{'label': 'alpha', 'value': 'workspace-alpha.json'},
                                                                   {'label': 'dev', 'value': 'workspace-dev.json'},
                                                                   {'label': 'wsmtest',
                                                                    'value': 'workspace-wsmtest.json'}],
                                                          clearable=False, style={'width': '60px !important'},
                                                          optionHeight=24, placeholder=None),
                                                 className='-root-panel-list__env-type-select')],
                                            className='root-panel-list__env-type-dropdown', style={'display': 'none'}),
                                        className='root-panel-list__dropdown-bar')],
                                    className='root-panel-list__filter-controls'),
                                className='root-panel-list__header'),
                            className='env-list', role='region'),
                        className='home__sidebar'),
                        Div(
                            [Div(
                                [Div(
                                    Nav([
                                        A('All', href='#', id='a-mc',
                                          className='navigation-tabs__tab pt-3 navigation-tabs__tab--active',
                                          style={'textDecoration': 'none'}, **{'aria-current': 'page'}),
                                        A('Summary', href='#', id='a-summaries',
                                          className='navigation-tabs__tab pt-3',
                                          style={'textDecoration': 'none'}),
                                        A('Results', href='#', id='a-results',
                                          className='navigation-tabs__tab pt-3',
                                          style={'textDecoration': 'none'}),
                                        A('Charts', href='#', id='a-charts', className='navigation-tabs__tab pt-3',
                                          style={'textDecoration': 'none', 'pointerEvents': 'none', 'cursor': 'default',
                                                 'color': 'black'})
                                    ], className='navigation-tabs pt-1 px-4'),
                                    className='shadow-scroller__head d-flex flex-column bg-white flex-shrink-0 '
                                              'trdash-output-detail__navigation'),
                                    Div(Section(id='output-detail',
                                                className='trdash-output-details p-4', role='region'),
                                        className='shadow-scroller__body flex-grow-1 overflow-none '
                                                  'trdash-output-detail__content')
                                ],
                                className='shadow-scroller d-flex flex-column bg-white trdash-output-detail'),
                            ],
                            className='root-detail__content')],
                    className='home'),
                className='app__content', role='main'),
        ], id='main-dash', className='app'),
    ], id="root")


    @app.callback(
        Output(component_id='date-picker-container', component_property='children'),
        Input(component_id='date-picker-container', component_property='children')
    )
    def initialize_datepicker(children):
        return datepicker_renderer('test-date-picker', 'custom-input', min_date=date(2021, 11, 29))


    @app.callback(
        Output(component_id='output-detail', component_property='children'),
        Output(component_id='a-mc', component_property='className'),
        Output(component_id='a-summaries', component_property='className'),
        Output(component_id='a-results', component_property='className'),
        #        Output(component_id='test-date-picker', component_property='date'),
        #        Output(component_id='test-date-picker', component_property='max_date_allowed'),
        Output(component_id='test-env-selector', component_property='options'),
        Input(component_id='test-date-picker', component_property='date'),
        Input(component_id='test-env-selector', component_property='value'),
        Input(component_id='a-mc', component_property='className'),
        Input(component_id='a-summaries', component_property='className'),
        Input(component_id='a-results', component_property='className'),
        Input(component_id='a-mc', component_property='n_clicks'),
        Input(component_id='a-summaries', component_property='n_clicks'),
        Input(component_id='a-results', component_property='n_clicks'),
        #        Input(component_id='test-date-picker', component_property='loading_state')
    )
    def update_results(d, e, mc, summaries, results, mc_n_clicks, summaries_n_clicks, results_n_clicks):
        ctx = callback_context
        nav_tabs_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # current_datetime_dict = get_time()
        # current_date = current_datetime_dict['d']
        # select_date = date.fromisoformat(d) if date.fromisoformat(d) < current_date else current_date
        output_detail = []
        select_env_options = []
        print(f"ctx: {ctx}")
        print(f"d: {d}")
        print(f"e: {e}")
        print(f"all: {mc}")
        print(f"summaries: {summaries}")
        print(f"results: {results}")
        print(f"mc_n_clicks: {mc_n_clicks}")
        print(f"summaries_n_clicks: {summaries_n_clicks}")
        print(f"results_n_clicks: {results_n_clicks}")
        print(f"nav_tabs_id: {nav_tabs_id}")
        # print(f"current_datetime: {current_datetime_dict['US/Eastern']}")
        # print(f"current_date: {current_date}")
        # print(f"select_date: {select_date}")

        with app.server.app_context():
            test_config = asyncio.run(distinct_test_config(d))

        for tc in test_config:
            print(tc)
            select_env_options.append({'label': splitext(tc[0])[0], 'value': tc[0]})

        if e is not None:
            with app.server.app_context():
                test_config = asyncio.run(distinct_test_config(d))
                all_results = asyncio.run(all_summaries(d, e))

            if all_results:
                if nav_tabs_id == 'a-summaries' or (nav_tabs_id != 'a-results' and 'active' in summaries):
                    print("In nav_tabs_id == 'a-summaries' or 'active' in summaries")
                    for testsuite in all_results:
                        tot_testcase_pass = 0
                        tot_testcase = 0
                        output_detail.append(H5(testsuite, className='section-header'))
                        for y in [x.testScriptResultSummaries for x in all_results[testsuite]]:
                            tot_testcase += len(y)
                            for s in y:
                                tot_testcase_pass += s['numCompleted'] == s['totalRun']
                        shortRefHeadCommit = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                            'shortRefHeadCommit']
                        remoteOriginUrl = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                            'remoteOriginUrl']
                        refHeadCommit = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                            'refHeadCommit']
                        helmVersions = all_results[testsuite][0].versionScriptResults[0]['helmVersions'][0][
                            'helmAppVersion']
                        end = all_results[testsuite][0].startTimestamp.strftime("%m/%d/%Y, %H:%M:%S")
                        begin = all_results[testsuite][-1].startTimestamp.strftime("%m/%d/%Y, %H:%M:%S")
                        output_detail.append(Div(Div([Div(Table(Thead(
                            [Tr([Th(Div('Duration',
                                        className='trdash-table__col-label'),
                                    className='trdash-table__head-col'),
                                 Th(Div('Total test case(s)',
                                        className='trdash-table__col-label'),
                                    className='trdash-table__head-col'),
                                 Th(Div('% pass',
                                        className='trdash-table__col-label'),
                                    className='trdash-table__head-col'),
                                 Th(Div('Git Version',
                                        className='trdash-table__col-label'),
                                    className='trdash-table__head-col'),
                                 Th(Div('Helm Version',
                                        className='trdash-table__col-label'),
                                    className='trdash-table__head-col')
                                 ])]),
                            className='trdash-table__head'),
                            className='trdash-table__head-wrapper'),
                            Div(className='trdash-table__head-wrapper'),
                            Div(Table(Tbody([Tr([Td(f"{begin} - {end}",
                                                    className='trdash-table__body-col',
                                                    style={'width': '20%'}),
                                                 Td(tot_testcase,
                                                    className='trdash-table__body-col',
                                                    style={'width': '20%'}),
                                                 Td(f"{tot_testcase_pass / tot_testcase:.0%}",
                                                    className='trdash-table__body-col',
                                                    style={'width': '20%'}),
                                                 Td(A(shortRefHeadCommit,
                                                      href=f"{remoteOriginUrl}/commit/{refHeadCommit}",
                                                      className='Link--secondary text-monospace ml-2 d-none d-lg-inline',
                                                      target='_blank'),
                                                    className='trdash-table__body-col',
                                                    style={'width': '20%'}),
                                                 Td(helmVersions,
                                                    className='trdash-table__body-col',
                                                    style={'width': '20%'})],
                                                className='trdash-table__body-row '
                                                          'trdash-table__body-row--expandable')]),
                                      className='trdash-table__body'),
                                className='trdash-table__body-wrapper',
                                style={'height': '100%'})],
                            className='trdash-table__table'),
                            className='trdash-table'))
                    return [output_detail, 'navigation-tabs__tab pt-3', 'navigation-tabs__tab pt-3 navigation-tabs__tab--active',
                            'navigation-tabs__tab pt-3', select_env_options]
                elif nav_tabs_id == 'a-results' or (nav_tabs_id != 'a-summaries' and 'active' in results):
                    print("nav_tabs_id == 'a-results' or 'active' in results")
                    for testsuite in all_results:
                        tot_testcase = 0
                        output_detail.append(H5(testsuite, className='section-header'))
                        shortRefHeadCommit = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                            'shortRefHeadCommit']
                        remoteOriginUrl = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                            'remoteOriginUrl']
                        refHeadCommit = all_results[testsuite][0].versionScriptResults[1]['gitVersions'][0][
                            'refHeadCommit']
                        helmVersions = all_results[testsuite][0].versionScriptResults[0]['helmVersions'][0][
                            'helmAppVersion']
                        if 'perf' in testsuite.lower() or 'resiliency' in testsuite.lower():
                            rs = []
                            for y in [x.testScriptResultSummaries for x in all_results[testsuite]]:
                                tot_testcase += len(y)
                                for s in y:
                                    rs.append(Tr([Td(s['testScriptName'],
                                                     className='trdash-table__body-col',
                                                     style={'width': '20%', 'wordWrap': 'break-word'}),
                                                  Td(s['totalRun'],
                                                     className='trdash-table__body-col',
                                                     style={'width': '20%'}),
                                                  Td(f"{s['numCompleted'] / s['totalRun']:.0%}",
                                                     className='trdash-table__body-col',
                                                     style={'width': '20%'}),
                                                  Td(f"{s['elapsedTimeStatistics']['percentile95']:.0f}",
                                                     className='trdash-table__body-col',
                                                     style={'width': '20%'}),
                                                  Td(A(shortRefHeadCommit,
                                                       href=f"{remoteOriginUrl}/commit/{refHeadCommit}",
                                                       className='Link--secondary text-monospace ml-2 d-none d-lg-inline',
                                                       target='_blank'),
                                                     className='trdash-table__body-col',
                                                     style={'width': '20%'}),
                                                  Td(helmVersions,
                                                     className='trdash-table__body-col',
                                                     style={'width': '20%'})],
                                                 className='trdash-table__body-row '
                                                           'trdash-table__body-row--expandable'))
                            output_detail.append(Div(Div([Div(Table(Thead(
                                [Tr([Th(Div('Test case',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('Concurrency',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('% pass',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('p95 (ms)',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('Git Version',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('Helm Version',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col')
                                     ])]),
                                className='trdash-table__head'),
                                className='trdash-table__head-wrapper'),
                                Div(className='trdash-table__head-wrapper'),
                                Div(Table(Tbody(rs),
                                          className='trdash-table__body'),
                                    className='trdash-table__body-wrapper',
                                    style={'height': '100%'} if tot_testcase <= 10 else None)],
                                className='trdash-table__table'),
                                className='trdash-table'))
                        else:
                            tot_testcase = len(all_results[testsuite])
                            output_detail.append(Div(Div([Div(Table(Thead(
                                [Tr([Th(Div('Test case',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('Total pass',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('% pass',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('Git Version',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col'),
                                     Th(Div('Helm Version',
                                            className='trdash-table__col-label'),
                                        className='trdash-table__head-col')
                                     ])]),
                                className='trdash-table__head'),
                                className='trdash-table__head-wrapper'),
                                Div(className='trdash-table__head-wrapper'),
                                Div(Table(Tbody([Tr([Td(u.testScriptResultSummaries[0]['testScriptName'],
                                                        className='trdash-table__body-col',
                                                        style={'width': '20%', 'wordWrap': 'break-word'}),
                                                     Td(u.testScriptResultSummaries[0]['numCompleted'],
                                                        className='trdash-table__body-col',
                                                        style={'width': '20%'}),
                                                     Td(f"{u.testScriptResultSummaries[0]['numCompleted'] / u.testScriptResultSummaries[0]['totalRun']:.0%}",
                                                        className='trdash-table__body-col',
                                                        style={'width': '20%'}),
                                                     Td(A(u.versionScriptResults[1]['gitVersions'][0][
                                                              'shortRefHeadCommit'],
                                                          href=f"{u.versionScriptResults[1]['gitVersions'][0]['remoteOriginUrl']}/commit/{u.versionScriptResults[1]['gitVersions'][0]['refHeadCommit']}",
                                                          className='Link--secondary text-monospace ml-2 d-none d-lg-inline',
                                                          target='_blank')
                                                        if len(u.versionScriptResults[1]['gitVersions']) > 0
                                                        else f"{u.versionScriptResults[1]['helmVersions'][0]['helmAppVersion']}",
                                                        className='trdash-table__body-col',
                                                        style={'width': '20%'}),
                                                     Td(A(u.versionScriptResults[0]['gitVersions'][0][
                                                              'shortRefHeadCommit'],
                                                          href=f"{u.versionScriptResults[0]['gitVersions'][0]['remoteOriginUrl']}",
                                                          className='Link--secondary text-monospace ml-2 d-none d-lg-inline')
                                                        if len(u.versionScriptResults[0]['gitVersions']) > 0
                                                        else f"{u.versionScriptResults[0]['helmVersions'][0]['helmAppVersion']}",
                                                        className='trdash-table__body-col',
                                                        style={'width': '20%'})],
                                                    className='trdash-table__body-row '
                                                              'trdash-table__body-row--expandable') for u in
                                                 all_results[testsuite]]),
                                          className='trdash-table__body'),
                                    className='trdash-table__body-wrapper',
                                    style={'height': '100%'} if tot_testcase <= 10 else None)],
                                className='trdash-table__table'),
                                className='trdash-table'))
                    return [output_detail, 'navigation-tabs__tab pt-3', 'navigation-tabs__tab pt-3',
                            'navigation-tabs__tab pt-3 navigation-tabs__tab--active', select_env_options]
            else:
                return ['Select environment type to view test runs.',
                        'navigation-tabs__tab pt-3  navigation-tabs__tab--active',
                        'navigation-tabs__tab pt-3', 'navigation-tabs__tab pt-3', select_env_options]
        else:
            # test_run_dataset = {}
            test_suite = ''
            git = ''
            helm = ''
            service_uri_dict = {}
            daily_test_run_results = asyncio.run(all_service_summaries(d))
            for spec in daily_test_run_results:
                output = []
                test_run_results = daily_test_run_results[spec]
                for result in test_run_results:
                    test_suite = result.testSuiteName
                    git = result.git_version['shortRefHeadCommit']
                    helm = result.helm_version['appName'] + ": " + result.helm_version['helmAppVersion'] + " / " + result.helm_version['helmChartVersion']
                    service_uri_dict = result.service_uri_dict

                    test_run_summaries = result.testScriptResultSummaries
                    for summary in test_run_summaries:
                        output.append(
                            {
                                'startUserJourneyTimestamp': result.startUserJourneyTimestamp.strftime('%d-%b-%Y %I.%M %p'),
                                'testScriptName': summary['testScriptName'],
                                'totalRun': summary['totalRun'],
                                'numCompleted': summary['numCompleted'],
                                'numExceptionsThrown': summary['numExceptionsThrown'],
                                'min': round(summary['elapsedTimeStatistics']['min']),
                                'max': round(summary['elapsedTimeStatistics']['max']),
                                'mean': round(summary['elapsedTimeStatistics']['mean']),
                                'sd': round(summary['elapsedTimeStatistics']['standardDeviation']),
                                'p50': round(summary['elapsedTimeStatistics']['median']),
                                'p95': round(summary['elapsedTimeStatistics']['percentile95'])
                            })
                        print(result.startUserJourneyTimestamp.strftime('%d-%b-%Y %I.%M %p'))
                        print(result.endUserJourneyTimestamp.strftime('%d-%b-%Y %I.%M %p'))
                        print(summary['testScriptName'])
                        print(summary['totalRun'])
                        print(summary['numCompleted'])
                        print(summary['numExceptionsThrown'])
                        # print('Y' if summary['isfailure'] else 'N')
                        print(summary['elapsedTimeStatistics']['min'])
                        print(summary['elapsedTimeStatistics']['max'])
                        print(summary['elapsedTimeStatistics']['mean'])
                        print(summary['elapsedTimeStatistics']['standardDeviation'])
                        print(summary['elapsedTimeStatistics']['median'])
                        print(summary['elapsedTimeStatistics']['percentile95'])

                title = spec + " - " + test_suite
                service_uri_dict = dict(sorted(service_uri_dict.items()))
                output_detail.append(Div([Div(
                    [
                        Tooltips(id='git'+title, label='Git', tooltip=git, fa='fa fa-github'),
                        Tooltips(id='helm'+title, label='Helm', tooltip=helm, fa='fa fa-info-circle')
                    ] +
                    [
                        Tooltips(id=k+title, label=k, tooltip=v, fa='fa fa-link')
                        for k, v in service_uri_dict.items()], style={'margin': '5px 1px'}),
                    SimpleTable(id=title, data=output, title=title)
                ]))

            # output_detail.append(SimpleTable(id='st', columns=cols, data=dat))
            return [output_detail,
                    'navigation-tabs__tab pt-3  navigation-tabs__tab--active',
                    'navigation-tabs__tab pt-3', 'navigation-tabs__tab pt-3', select_env_options]


    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
