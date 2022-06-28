import MaterialTable from "@material-table/core";
import React, {Component} from 'react';
import Plot from 'react-plotly.js';
import PropTypes from "prop-types";

const cols = [
    {title: 'Start time', field: 'startUserJourneyTimestamp', type: 'datetime'},
    {title: 'Name', field: 'testScriptName'},
    {title: 'Total', field: 'totalRun', type: 'numeric', hidden: true},
    {title: 'Trend date', field: 'trend_date', hidden: true},
    {title: 'Trend totalRun', field: 'trend_totalRun', hidden: true},
    {title: 'Trend numCompleted', field: 'trend_numCompleted', hidden: true},
    {title: 'Trend numExceptionsThrown', field: 'trend_numExceptionsThrown', hidden: true},
    {title: 'Trend numExceptionsThrown neg', field: 'trend_numExceptionsThrown_neg', hidden: true},
    {title: 'Outcome trend', field: 'trend',
        render: (row) =>
            <Plot
                config={
                    {
                        displayModeBar: false,
                    }
                }
                data={
                    [
                        {
                            x: row.trend_date,
                            y: row.trend_numCompleted,
                            name: 'Passed',
                            type: 'bar',
                            width: 0.3,
                            hovertemplate: '<i>%{x} Passed</i>: %{y}',
                            marker: {
                                color: 'rgba(50, 171, 96, 0.7)',
                            },
                        },
                        {
                            x: row.trend_date,
                            y: row.trend_numExceptionsThrown_neg,
                            text: row.trend_numExceptionsThrown,
                            name: 'Failed',
                            type: 'bar',
                            width: 0.3,
                            hovertemplate: '<i>%{x} Failed</i>: %{text}',
                            marker: {
                                color: 'rgba(219, 64, 82, 0.7)',
                            }
                        }
                    ]
                }
                layout={ {
                    width: 200,
                    height: 120,
                    barmode: 'relative',
                    showlegend: false,
                    margin: {
                        l: 50,
                        r: 50,
                        b: 50,
                        t: 50,
                        pad: 4
                    },
                    xaxis: {
                        visible: false,
                        showticklabels: false,
                    },
                    yaxis: {
                        visible: false,
                        showticklabels: false,
                    },
                } }
            />
    },
    {title: 'Failed', field: 'numExceptionsThrown', cellStyle: {
        textAlign: 'center', verticalAlign: "top",
        }, headerStyle: {
        textAlign: 'center',
        }, type: 'numeric'},
    {title: 'Passed', field: 'numCompleted', cellStyle: {
        textAlign: 'center', verticalAlign: "top",
        }, headerStyle: {
        textAlign: 'center',
        }, type: 'numeric'},
    {title: 'Skipped', field: 'numSkipped', cellStyle: {
        textAlign: 'center', verticalAlign: "top",
        }, headerStyle: {
        textAlign: 'center',
        }, type: 'numeric',
        render: (row) =>
            row.totalRun - row.numCompleted - row.numExceptionsThrown
    },
];

class IntegrationTestsTable extends Component {
    render() {
        const {data, title, barWidth} = this.props;
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
                            textAlign: "left",
                            verticalAlign: "top",
                        },
                        headerStyle: {
                            fontFamily: "'Lato', 'Helvetica Neue', Arial, sans-serif",
                        },
                    }}
                />
            </div>
        );
    }
}

IntegrationTestsTable.defaultProps = {};

IntegrationTestsTable.propTypes = {
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
    title: PropTypes.string,
    /**
     * The bar width of the Bar Charts.
     */
    barWidth: PropTypes.number,
};

export default IntegrationTestsTable;
