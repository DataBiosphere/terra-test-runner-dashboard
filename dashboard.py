import asyncio
from datetime import datetime, timedelta, date

import numpy as np
import pandas as pd
import pytz
from dash import Output, Input, callback_context, dcc
from dash.dcc import Clipboard, DatePickerSingle, Loading
from dash.html import Div, Header, H1, A, Main, Section, Label, Nav

from test_runner_components import Tooltips, IntegrationTestsTable, PerfTestsTable

from api.routes.test_run_summary import get_mc_terra_test_results
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
                                        A('MC Terra Services', href='#', id='a-mc',
                                          className='navigation-tabs__tab pt-3 navigation-tabs__tab--active',
                                          style={'textDecoration': 'none'}, **{'aria-current': 'page'})
                                    ], className='navigation-tabs pt-1 px-4'),
                                    className='shadow-scroller__head d-flex flex-column bg-white flex-shrink-0 '
                                              'trdash-output-detail__navigation'),
                                    Loading(Div(Section(id='output-detail',
                                                className='trdash-output-details p-4', role='region'),
                                                className='shadow-scroller__body flex-grow-1 overflow-none '
                                                'trdash-output-detail__content'),
                                            type="dot", fullscreen=True, color="rgba(22, 22, 22, 255)")
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
        print(f"nav_tabs_id: {nav_tabs_id}")

        begin_date = date.fromisoformat(d) - timedelta(4)
        end_date = date.fromisoformat(d)
        end_month_day_str = end_date.strftime('%-m/%-d')

        l1, dfg = asyncio.run(get_mc_terra_test_results(begin_date, end_date))
        for test_config in l1:
            config = test_config[0]
            suite = test_config[1]
            git = {}
            remoteoriginurl = None
            helm = {}
            service_uri_dict = {}
            output = []
            for test_script_name in dfg.loc[test_config].index.values:
                test_result = dfg.loc[test_config].loc[test_script_name]
                date_range = test_result['date']

                if date_range[-1] == end_month_day_str:
                    # print('{}, {}, {}, {}'.format(config, suite, test_script_name, date_range[-1]))
                    if len(git) == 0:
                        # print('git: {}'.format(test_result['git']))
                        g = test_result['git']
                        if len(g) > 0:
                            git = g['shortRefHeadCommit']
                            remoteoriginurl = g['remoteOriginUrl'] + "/commit/" + g['refHeadCommit']

                    if len(helm) == 0:
                        # print('helm: {}'.format(test_result['helm']))
                        h = test_result['helm']
                        if len(h) > 0:
                            helm = h['appName'] \
                                + ": " + h['helmAppVersion'] \
                                + " / " + h['helmChartVersion']
                    if len(service_uri_dict) == 0:
                        # print('service_uri_dict: {}'.format(service_uri_dict))
                        s = test_result['server']
                        if len(s) > 0:
                            service_uri_dict = s

                    date_range = np.unique(test_result['date'])

                    mean_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['mean']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.round(np.mean(e, 0)))

                    mean_intraday = [mean_trend.loc[mmdd] for mmdd in date_range]

                    p50_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['p50']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.round(np.median(e, 0)))

                    p50_intraday = [p50_trend.loc[mmdd] for mmdd in date_range]

                    p95_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['p95']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.round(np.percentile(e, 95)))

                    p95_intraday = [p95_trend.loc[mmdd] for mmdd in date_range]

                    min_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['min']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.round(np.min(e, 0)))

                    min_intraday = [min_trend.loc[mmdd] for mmdd in date_range]

                    max_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['max']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.round(np.max(e, 0)))

                    max_intraday = [max_trend.loc[mmdd] for mmdd in date_range]

                    total_run_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['totalRun']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.sum(e, 0))

                    total_run_intraday = [total_run_trend.loc[mmdd] for mmdd in date_range]

                    num_completed_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['numCompleted']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.sum(e, 0))

                    num_completed_intraday = [num_completed_trend.loc[mmdd] for mmdd in date_range]

                    num_exceptions_thrown_trend = pd.DataFrame({
                        'x': test_result['date'],
                        'y': test_result['numExceptionsThrown']
                    }).set_index('x')['y']\
                        .groupby('x')\
                        .apply(list)\
                        .apply(lambda e: np.sum(e, 0))

                    num_exceptions_thrown_intraday = [num_exceptions_thrown_trend.loc[mmdd] for mmdd in date_range]

                    output.append(
                        {
                            'startUserJourneyTimestamp': np.datetime_as_string(
                                test_result['timestamp'][-1], timezone=pytz.timezone('US/Eastern')),
                            'testScriptName': test_script_name,
                            'totalRun': test_result['totalRun'][-1],
                            'numCompleted': test_result['numCompleted'][-1],
                            'numExceptionsThrown': test_result['numExceptionsThrown'][-1],
                            'min': round(test_result['min'][-1]),
                            'max': round(test_result['max'][-1]),
                            'mean': round(test_result['mean'][-1]),
                            'sd': round(test_result['sd'][-1]),
                            'p50': round(test_result['p50'][-1]),
                            'p95': round(test_result['p95'][-1]),
                            'trend_date': date_range,
                            'trend_mean': mean_intraday,
                            'trend_p50': p50_intraday,
                            'trend_p95': p95_intraday,
                            'trend_min': min_intraday,
                            'trend_max': max_intraday,
                            'trend_totalRun': total_run_intraday,
                            'trend_numCompleted': num_completed_intraday,
                            'trend_numExceptionsThrown': num_exceptions_thrown_intraday,
                            'trend_numExceptionsThrown_neg': [-v for v in num_exceptions_thrown_intraday],
                        })

            title = config + " - " + suite

            if len(output) > 0:
                output_detail.append(Div([Div(
                    [
                        Tooltips(id='git' + title, label='Git', tooltip=git, fa='fa fa-github')
                        if len(git) > 0 else '',
                        dcc.Input(id='remotegiturl' + title, type='hidden', value=remoteoriginurl)
                        if remoteoriginurl is not None else '',
                        Clipboard(target_id='remotegiturl' + title,
                                  title='Copy git url',
                                  style={
                                      'display': 'inline-block',
                                      'fontSize': 20,
                                      'verticalAlign': 'top',
                                  })
                        if remoteoriginurl is not None else '',
                        Tooltips(id='helm' + title, label='Helm', tooltip=helm, fa='fa fa-info-circle')
                        if len(helm) > 0 else ''
                    ] +
                    [
                        Tooltips(id=k + title, label=k, tooltip=v, fa='fa fa-link')
                        for k, v in service_uri_dict.items()], style={'margin': '5px 1px'})
                                          if len(service_uri_dict) > 0 else '',
                                          IntegrationTestsTable(id=title, data=output, title=title)
                                          if 'integ' in suite.lower()
                                          else PerfTestsTable(id=title, data=output, title=title)
                    ]))

        return [output_detail,
                'navigation-tabs__tab pt-3  navigation-tabs__tab--active']

    app.server.register_blueprint(workspacemanager, url_prefix='/workspacemanager')

    app.run_server(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
