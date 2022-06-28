import MaterialTable from "@material-table/core";
import React, {Component} from 'react';
import Plot from 'react-plotly.js';
import PropTypes from "prop-types";

class PerfTestsTable extends Component {
    render() {
        const {data, title} = this.props;
        const cols = [
            {title: 'Test time', field: 'startUserJourneyTimestamp', type: 'datetime'},
            {title: 'Name', field: 'testScriptName', type: 'string'},
            {title: 'Trend date', field: 'trend_date', hidden: true},
            {title: 'Trend mean', field: 'trend_mean', hidden: true},
            {title: 'Trend p50', field: 'trend_p50', hidden: true},
            {title: 'Trend p95', field: 'trend_p95', hidden: true},
            {title: 'Trend min', field: 'trend_min', hidden: true},
            {title: 'Trend max', field: 'trend_max', hidden: true},
            {
                title: 'Outcome trend', field: 'perf_trend', sorting: false,
                render: (row) =>
                    <div><Plot
                        config={
                            {
                                displayModeBar: false,
                            }
                        }
                        data={
                            [
                                {
                                    x: row.trend_date,
                                    y: row.trend_min,
                                    name: 'min [ms]',
                                    type: 'scatter',
                                    mode: 'lines',
                                    line: {
                                        width: 0,
                                    },
                                    showlegend: false,
                                },
                                {
                                    x: row.trend_date,
                                    y: row.trend_mean,
                                    name: 'mean [ms]',
                                    type: 'scatter',
                                    mode: 'lines',
                                    line: {
                                        color: 'rgba(63, 176, 198, 255)',
                                        dash: 'dash',
                                    },
                                    fill: 'tonexty',
                                    fillcolor: 'rgba(170, 218, 277, 255)',
                                    showlegend: false,
                                },
                                {
                                    x: row.trend_date,
                                    y: row.trend_p95,
                                    name: 'p95 [ms]',
                                    type: 'scatter',
                                    mode: 'lines',
                                    line: {
                                        width: 0,
                                    },
                                    fill: 'tonexty',
                                    fillcolor: 'rgba(130, 200, 213, 255)',
                                    showlegend: false,
                                },
                                {
                                    x: row.trend_date,
                                    y: row.trend_max,
                                    name: 'max [ms]',
                                    type: 'scatter',
                                    mode: 'lines',
                                    line: {
                                        width: 0,
                                    },
                                    fill: 'tonexty',
                                    fillcolor: 'rgba(170, 218, 277, 255)',
                                    showlegend: false,
                                },
                                {
                                    x: row.trend_date,
                                    y: row.trend_p50,
                                    name: 'p50 [ms]',
                                    type: 'scatter',
                                    mode: 'lines',
                                    line: {
                                        color: 'rgba(67, 178, 199, 255)',
                                    },
                                    showlegend: false,
                                },
                            ]
                        }
                        layout={{
                            paper_bgcolor: 'rgba(0,0,0,0)',
                            plot_bgcolor: 'rgba(0,0,0,0)',
                            width: 200,
                            height: 80,
                            legend: {
                                font: {
                                    family: "'Lato', 'Helvetica Neue', Arial, sans-serif",
                                    size: "9px",
                                },
                                yanchor: 'top',
                                y: 1.01,
                                xanchor: 'left',
                                x: 0.1,
                            },
                            margin: {
                                l: 40,
                                r: 20,
                                b: 20,
                                t: 0,
                                pad: 1
                            },
                            xaxis: {
                                tickfont: {
                                    family: "'Lato', 'Helvetica Neue', Arial, sans-serif",
                                    size: "8px",
                                },
                            },
                            yaxis: {
                                tickfont: {
                                    family: "'Lato', 'Helvetica Neue', Arial, sans-serif",
                                    size: "8px",
                                },
                            },
                        }}
                    /></div>
            },
            {
                title: 'Min [ms]', field: 'min',
                cellStyle: {
                    paddingRight: '40px',
                    verticalAlign: 'top',
                }, type: 'numeric'
            },
            {
                title: 'Max [ms]', field: 'max',
                cellStyle: {
                    paddingRight: '40px',
                    verticalAlign: 'top',
                }, type: 'numeric'
            },
            {
                title: 'Mean [ms]', field: 'mean',
                cellStyle: {
                    paddingRight: '40px',
                    verticalAlign: 'top',
                }, type: 'numeric'
            },
            {
                title: 'Standard deviation [ms]', field: 'sd',
                cellStyle: {
                    paddingRight: '40px',
                    verticalAlign: 'top',
                }, type: 'numeric'
            },
            {
                title: 'p50 [ms]', field: 'p50',
                cellStyle: {
                    paddingRight: '40px',
                    verticalAlign: 'top',
                }, type: 'numeric'
            },
            {
                title: 'p95 [ms]', field: 'p95',
                cellStyle: {
                    paddingRight: '40px',
                    verticalAlign: 'top',
                }, type: 'numeric'
            },
        ];

        return (
            <div>
                <MaterialTable
                    columns={cols}
                    data={data}
                    title={title}
                    options={{
                        cellStyle: {
                            fontFamily: "'Lato', 'Helvetica Neue', Arial, sans-serif",
                            fontSize: "12px",
                            verticalAlign: "top",
                        },
                        headerStyle: {
                            fontFamily: "'Lato', 'Helvetica Neue', Arial, sans-serif",
                        },
                        rowStyle: (row, i) => ({
                            backgroundColor: i % 2 === 0 ? "#ffffff" : "#eeeeee",
                            maxHeight: "50px",
                        }),
                    }}
                />
            </div>
        );
    }
}

PerfTestsTable.defaultProps = {};

PerfTestsTable.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * The data rendered by the table.
     */
    data: PropTypes.array,
    /**
     * The title of the table.
     */
    title: PropTypes.string
};

export default PerfTestsTable;
