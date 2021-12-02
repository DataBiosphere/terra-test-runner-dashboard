import './root-list.scss';
import React, {Component} from 'react';
import PropTypes from 'prop-types';

class SummaryCard extends Component {
    render() {
        const {
            id,
            testScriptName,
            totalRun,
            numCompleted,
            numExceptionsThrown,
        } = this.props;
        return (
            <li key={{id}-{testScriptName}}>
                <label className="root-list__card">
                    <span className="root-list__name">{testScriptName} ({totalRun})</span>
                    <span className="root-list__completed">{numCompleted} passed</span>
                    <span className="root-list__root"> / </span>
                    <span className="root-list__exceptions-thrown">{numExceptionsThrown} failed</span>
                </label>
            </li>
        );
    }
}

SummaryCard.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * testSuiteName.
     */
    testSuiteName: PropTypes.string,
    /**
     * testScriptName.
     */
    testScriptName: PropTypes.string.isRequired,
    /**
     * totalRun
     */
    totalRun: PropTypes.number.isRequired,
    /**
     * numCompleted
     */
    numCompleted: PropTypes.number.isRequired,
    /**
     * numExceptionsThrown
     */
    numExceptionsThrown: PropTypes.number.isRequired,
    /**
     * serverSpecificationFile
     */
    serverSpecificationFile: PropTypes.string,
}

export default SummaryCard;
