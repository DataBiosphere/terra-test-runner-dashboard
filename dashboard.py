import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import bigquery

bq = bigquery.Client(project="terra-kernel-k8s")

SELECT_workspace_wsmtest_today = '''
SELECT t.startTime, name, elapsedTime_percentile95 
 FROM `terra-kernel-k8s.test_runner_results.testScriptResults` r 
   INNER JOIN 
    `terra-kernel-k8s.test_runner_results.testRun` t 
   ON r.testRun_id = t.id
 WHERE t.server_name = 'workspace-wsmtest' AND EXTRACT(DATE FROM CURRENT_TIMESTAMP()) = EXTRACT(DATE FROM t.startTime)
 ORDER BY t.startTime, r.elapsedTime_percentile95
'''

workspace_wsmtest_today_df = bq.query(SELECT_workspace_wsmtest_today).to_dataframe()

y_perf = workspace_wsmtest_today_df.iloc[21:27]['elapsedTime_percentile95'].values

y_int = workspace_wsmtest_today_df.iloc[0:21]['elapsedTime_percentile95'].values

y_resiliy = workspace_wsmtest_today_df.iloc[27:28]['elapsedTime_percentile95'].values

x_perf = workspace_wsmtest_today_df.iloc[21:27]['name'].values
x_int = workspace_wsmtest_today_df.iloc[0:21]['name'].values
x_resiliy = workspace_wsmtest_today_df.iloc[27:28]['name'].values

# Creating two subplots
fig = make_subplots(rows=1, cols=3, specs=[[{}, {}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001)

fig.append_trace(go.Bar(
    x=y_perf,
    y=x_perf,
    hoverlabel={"bgcolor": "rgb(0, 0, 0)", "font": {"color": "rgb(255, 255, 255)"}},
    hovertemplate="%{y}<br>%{x} ms",
    marker=dict(
        color='rgba(130,191,119,153)',  # rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(130,191,119,255)',  # rgba(50, 171, 96, 1.0)',
            width=1),
    ),
    name='Workspace Manager: Performance Tests',
    textfont=dict(color='rgba(102,117,255,255)'),
    orientation='h',
), 1, 1)

fig.append_trace(go.Bar(
    x=y_int,
    y=x_int,
    marker=dict(
        color='rgba(255,117,255,153)',
        line=dict(
            color='rgba(255,117,255,255)',
            width=1),
    ),
    name='Workspace Manager: Integration Tests',
    textfont=dict(color='rgba(102,117,255,255)'),
    orientation='h',
), 1, 2)

fig.append_trace(go.Bar(
    x=y_resiliy,
    y=x_resiliy,
    marker=dict(
        color='rgba(106,255,255,153)',
        line=dict(
            color='rgba(106,255,255,255)',
            width=1),
    ),
    name='Workspace Manager: Resiliency Tests',
    textfont=dict(color='rgba(102,117,255,255)'),
    orientation='h',
), 1, 3)

fig.update_layout(
    title=dict(
        text='MC Terra Services Test Results Dashboard',
        font=dict(color='rgba(206,206,206,255)')
    ),
    yaxis=dict(
        color='rgba(206,206,206,255)',
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis2=dict(
        color='rgba(206,206,206,255)',
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis3=dict(
        color='rgba(206,206,206,255)',
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.25],
        tickfont=dict(color='rgb(255, 255, 255)')
    ),
    xaxis2=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.37, 0.62],
        tickfont=dict(color='rgb(255, 255, 255)')
    ),
    xaxis3=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.75, 1],
        tickfont=dict(color='rgb(255, 255, 255)')
    ),
    legend=dict(x=0.029, y=1.038, font=dict(color='rgb(255, 255, 255)', size=10)),
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgb(0, 0, 0)',  # 'rgb(248, 248, 255)',
    plot_bgcolor='rgb(0, 0, 0)'  # 'rgb(248, 248, 255)',
)

annotations = []

y_s = np.rint(y_perf)
y_nw = np.rint(y_int)
y_r = np.rint(y_resiliy)

# Adding labels
for yd, xd in zip(y_s, x_perf):
    # labeling the perf test
    annotations.append(dict(xref='x2', yref='y2',
                            y=xd, x=yd + 10,
                            text='{:,}'.format(yd) + 'ms',
                            font=dict(family='Arial', size=12,
                                      color='rgba(206,206,206,255)'  # 'rgb(128, 0, 128)'
                                      ),
                            showarrow=False))

for yd, xd in zip(y_nw, x_int):
    # labeling the integration test
    annotations.append(dict(xref='x1', yref='y1',
                            y=xd, x=yd + 3,
                            text=str(yd) + 'ms',
                            font=dict(family='Arial', size=12,
                                      color='rgba(206,206,206,255)'  # 'rgb(50, 171, 96)'
                                      ),
                            showarrow=False))
for yd, xd in zip(y_r, x_resiliy):
    # labeling the resiliency test
    annotations.append(dict(xref='x3', yref='y3',
                            y=xd, x=yd,
                            text=str(yd) + 'ms',
                            font=dict(family='Arial', size=12,
                                      color='rgba(206,206,206,255)'  # 'rgb(50, 171, 96)'
                                      ),
                            showarrow=False))


# Source
annotations.append(dict(xref='paper', yref='paper',
                        x=-0.2, y=-0.109,
                        text='TestRunner "' +
                             'Workspace Manager, ' +
                             'Buffer Services, ' +
                             'External Cred Services',
                        font=dict(family='Arial', size=10, color='rgba(206,206,206,255)'  # 'rgb(150,150,150)'
                                  ),
                        showarrow=False))

fig.update_layout(annotations=annotations)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Button("Perf", id="env-perf-button", key="env-perf-button",
                                                       style={"backgroundColor": "#a6a6a8", "color": "#e6e5e6",
                                                              "height": "80px", "width": "150px",
                                                              "marginBottom": "15px", "marginTop": "25px",
                                                              "marginRight": "2px", "textAlign": "left",
                                                              "paddingTop": "1px"}),
                                            dbc.Button("Stage", id="env-stage-button", key="env-stage-button",
                                                       style={"backgroundColor": "#60626b", "color": "#abadb3",
                                                              "height": "80px", "width": "150px",
                                                              "marginBottom": "15px", "marginTop": "25px",
                                                              "marginRight": "2px", "textAlign": "left",
                                                              "paddingTop": "1px"}),
                                            dbc.Button("Test", id="env-test-button", key="env-test-button",
                                                       style={"backgroundColor": "#60626b", "color": "#abadb3",
                                                              "height": "80px", "width": "150px",
                                                              "marginBottom": "15px", "marginTop": "25px",
                                                              "marginRight": "2px", "textAlign": "left",
                                                              "paddingTop": "1px"}),
                                            dbc.Button("Dev", id="env-dev-button", key="env-dev-button",
                                                       style={"backgroundColor": "#60626b", "color": "#abadb3",
                                                              "height": "80px", "width": "150px",
                                                              "marginBottom": "15px", "marginTop": "25px",
                                                              "marginRight": "2px", "textAlign": "left",
                                                              "paddingTop": "1px"})
                                        ]
                                    )
                                ]
                            ),
                        ],
                        width={"size": 6, "offset": 3}
                    )
                )
            ],
            id="testrunner-dashboard-container",
            style={"backgroundColor": "#191b28", "textAlign": "center"}
        ),
        dcc.Graph(
            id='testrunner-graph',
            figure=fig,
            style={"backgroundColor": "#000000"}
        )
    ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=443, ssl_context='adhoc')
