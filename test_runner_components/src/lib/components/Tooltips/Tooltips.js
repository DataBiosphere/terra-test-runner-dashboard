import '../../styles/font-awesome.scss';
import '../../styles/tooltips/tooltips.scss';

import React, {Component} from 'react';
import ReactTooltip from "react-tooltip";
import PropTypes from "prop-types";

const TOOLTIP_DEFINITIONS = [{
    id: 'element-id1',
    content: (<span>Tooltip1.</span>)
}, {
    id: 'element-id2',
    content: (<span>Tooltip2.</span>)
}];

/**
 * Tooltips is a React tooltip component
 */
class Tooltips extends Component {

    render() {
        const tooltips = [];
        for (const definition of TOOLTIP_DEFINITIONS) {
            tooltips.push(<ReactTooltip key={definition.id} id={definition.id} className="summary-tooltips__tooltip"
                                        place="right" type="dark" effect="solid" delayShow={300}><i
                className="summary-tooltips__tooltip-icon fa fa-info-circle"/>{definition.content}</ReactTooltip>);
        }

        return (
            <div className="summary-tooltips">
                {tooltips}
            </div>
        );
    }
}

Tooltips.dafaultProps = {};

Tooltips.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * A label that will be printed when this component is rendered.
     */
    label: PropTypes.string.isRequired,
}

export default Tooltips;
