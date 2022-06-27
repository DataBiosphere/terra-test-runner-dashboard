import '../../styles/font-awesome.scss';
import '../../styles/tooltips/tooltips.scss';

import React, {Component} from 'react';
import ReactTooltip from "react-tooltip";
import PropTypes from "prop-types";

/**
 * Tooltips is a React tooltip component
 */
class Tooltips extends Component {

    render() {
        const {id, label, tooltip, fa} = this.props;

        return (
            <span className="summary-tooltips">
                <button data-tip data-for={id} style={{display: "inline-block", margin: "1px 3px", padding: "1px 10px",
                    borderRadius: "40px", border: "1px solid black",
                    color: "black", background: "transparent"}}>{label}
                </button>
                <ReactTooltip id={id} place="top" effect="solid" delayShow={200} >
                    <i className={"summary-tooltips__tooltip-icon " + fa}/>
                    {tooltip}
                </ReactTooltip>
            </span>
        );
    }
}

Tooltips.dafaultProps = {};

Tooltips.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string.isRequired,
    /**
     * A label that will appear in this component when rendered.
     */
    label: PropTypes.string.isRequired,
    /**
     * The tooltip of this component.
     */
    tooltip: PropTypes.string.isRequired,
    /**
     * A fontawesome icon for the tooltip.
     */
    fa: PropTypes.string
}

export default Tooltips;
