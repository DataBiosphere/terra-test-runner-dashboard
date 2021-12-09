import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Main from "../../RootList/Main";

class EnvList extends Component {
    render() {
        const {children} = this.props;
        const datePicker = children.pop();
        return (
            <section className="env-list" role="region">
                <div className="env-list__header">
                    <h2 className="env-list__heading">Environment Summaries</h2>
                </div>
                <div className="env-list__listing">
                    <Main children={children}/>
                </div>
            </section>
        );
    }
}

EnvList.dafaultProps = {}

EnvList.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * A list of dash components.
     */
    children: PropTypes.element,
}

export default EnvList;
