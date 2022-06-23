import asyncio
from datetime import datetime, timedelta, date
from os.path import splitext

import pytz
from dash import Output, Input, callback_context
from dash.dcc import DatePickerSingle, Dropdown
from dash.html import Button, Div, Header, H1, A, Main, Section, Label, Nav, H5, Table, Thead, Tr, Th, Tbody, Td

from test_runner_components import Tooltips, IntegrationTestsTable, PerfTestsTable

from api.routes.test_run_summary import all_summaries, distinct_test_config, all_service_summaries, \
    get_response_time_trends
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
                [H1(
                    A('Test Runner Dashboard', href='/', tabIndex=-1),
                    **{'aria-label': 'Go to home page.'}, className='app__title'),
                        Div(
                            Div([Div([Div([
                                Label('Date:', className='mb-0', htmlFor='test-date-picker'),
                                Div(id='date-picker-container', className='root-panel-list__env-type-select')
                            ], className='root-panel-list__env-type-dropdown')],
                                className='root-panel-list__dropdown-bar')],
                                className='root-panel-list__filter-controls'),
                            className='root-panel-list__header')],
                className='app__header', role='banner'),
            Main(
                Div(
                    [
                        Div(
                            [Div(
                                [Div(
                                    Nav([
                                        A('All', href='#', id='a-mc',
                                          className='navigation-tabs__tab pt-3 navigation-tabs__tab--active',
                                          style={'textDecoration': 'none'}, **{'aria-current': 'page'})
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
        Input(component_id='test-date-picker', component_property='date'),
        Input(component_id='a-mc', component_property='className'),
        Input(component_id='a-mc', component_property='n_clicks'),
        #        Input(component_id='test-date-picker', component_property='loading_state')
    )
    def update_results(d, mc, mc_n_clicks):
        ctx = callback_context
        nav_tabs_id = ctx.triggered[0]['prop_id'].split('.')[0]
        output_detail = []
        print(f"ctx: {ctx}")
        print(f"d: {d}")
        print(f"mc_n_clicks: {mc_n_clicks}")
        print(f"nav_tabs_id: {nav_tabs_id}")

        test_suite = ''
        git = ''
        helm = ''
        service_uri_dict = {}
        daily_test_run_results = asyncio.run(all_service_summaries(d))
        begin_date = date.fromisoformat(d) - timedelta(4)
        end_date = date.fromisoformat(d)

        for spec in daily_test_run_results:
            trend = asyncio.run(get_response_time_trends(begin_date, end_date, spec))
            output = []
            test_run_results = daily_test_run_results[spec]
            for result in test_run_results:
                test_suite = result.testSuiteName
                git = result.git_version['shortRefHeadCommit']
                helm = result.helm_version['appName'] + ": " + result.helm_version['helmAppVersion'] + " / " + result.helm_version['helmChartVersion']
                service_uri_dict = result.service_uri_dict
                test_run_summaries = result.testScriptResultSummaries
                for summary in test_run_summaries:
                    tr1 = {c: trend[trend['testScriptName'] == summary['testScriptName']][c].values
                           for c in trend.columns}
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
                            'p95': round(summary['elapsedTimeStatistics']['percentile95']),
                            'trend_date': tr1['date'],
                            'trend_mean': tr1['mean'],
                            'trend_p50': tr1['median'],
                            'trend_p95': tr1['percentile95'],
                            'trend_min': tr1['min'],
                            'trend_max': tr1['max'],
                            'trend_totalRun': tr1['totalRun'],
                            'trend_numCompleted': tr1['numCompleted'],
                            'trend_numExceptionsThrown': tr1['numExceptionsThrown'],
                            'trend_numExceptionsThrown_neg': [-v for v in tr1['numExceptionsThrown']],
                        })

                    # print(result.startUserJourneyTimestamp.strftime('%d-%b-%Y %I.%M %p'))
                    # print(result.endUserJourneyTimestamp.strftime('%d-%b-%Y %I.%M %p'))
                    # print(summary['testScriptName'])
                    # print(summary['totalRun'])
                    # print(summary['numCompleted'])
                    # print(summary['numExceptionsThrown'])
                    # print('Y' if summary['isfailure'] else 'N')
                    # print(summary['elapsedTimeStatistics']['min'])
                    # print(summary['elapsedTimeStatistics']['max'])
                    # print(summary['elapsedTimeStatistics']['mean'])
                    # print(summary['elapsedTimeStatistics']['standardDeviation'])
                    # print(summary['elapsedTimeStatistics']['median'])
                    # print(summary['elapsedTimeStatistics']['percentile95'])

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
                    PerfTestsTable(id=title, data=output, title=title)
                    if 'perf' in test_suite.lower()
                    else IntegrationTestsTable(id=title, data=output, title=title)
                ]))

        # output_detail.append(SimpleTable(id='st', columns=cols, data=dat))
        return [output_detail,
                'navigation-tabs__tab pt-3  navigation-tabs__tab--active']

    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
