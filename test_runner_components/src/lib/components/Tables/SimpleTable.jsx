import MaterialTable from "@material-table/core";
import React, {Component} from 'react';
import PropTypes from "prop-types";
import {Chart} from "react-google-charts";

const dat = [
    ["Date", "% pass rate"],
    ["6/17", 100],
    ["6/16", 100],
    ["6/15", 100],
    ["6/14", 100],
    ["6/13", 100]
];

const options = {
  title: "5-Day Trend",
};

const cols = [
    {title: 'Test time', field: 'startUserJourneyTimestamp', type: 'datetime'},
    {title: 'Name', field: 'testScriptName'},
    {title: 'Pass', field: 'numCompleted', type: 'numeric'},
    {title: 'Fail', field: 'numExceptionsThrown', type: 'numeric'},
    {title: 'Min [ms]', field: 'min', type: 'numeric'},
    {title: 'Max [ms]', field: 'max', type: 'numeric'},
    {title: 'Mean [ms]', field: 'mean', type: 'numeric'},
    {title: 'Standard deviation [ms]', field: 'sd', type: 'numeric'},
    {title: 'p50 [ms]', field: 'p50', type: 'numeric'},
    {title: 'p95 [ms]', field: 'p95', type: 'numeric'},
    {title: 'Pass Rate trend', field: 'trend',
        render: (row) =>
            <Chart chartType="ColumnChart"
                   data={dat}
                   options={options}
                   width={"200px"}
                   height={"100px"}
            />
    },
    {title: 'Response time trend', field: 'perf_trend',
        render: (row) =>
            <Chart chartType="ScatterChart"
                   data={[["Date", "Response Time [ms]"], ["6/13", 50], ["6/14", 70], ["6/15", 80], ["6/16", 50], ["6/17", 100]]}
                   width={"200px"}
                   height={"100px"}
            />
    }
];

class SimpleTable extends Component {
    render() {
        const {data, title} = this.props;
        return (
            <MaterialTable columns={cols} data={data} title={title}/>
        );
    }
}

SimpleTable.defaultProps = {};

SimpleTable.propTypes = {
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

export default SimpleTable;
