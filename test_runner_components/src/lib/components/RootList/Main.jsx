import './root-list.scss';

import React, {Component} from 'react';
import PropTypes from 'prop-types';

class Main extends Component {
    render() {
        const {children} = this.props;
        let root_list = [];
        if (React.Children.count(children) > 0) {
                root_list = [...children]
        } else {
            root_list.push(<li key="7">
                <label className="root-list__card">
                    <span className="root-list__name">Enumerate DataRepo</span>
                    <span className="root-list__root">7 pass / 10</span>
                </label>
            </li>);
            root_list.push(<li key="8">
                <label className="root-list__card">
                    <span className="root-list__name">Service Status</span>
                    <span className="root-list__num-completed">10 pass</span>
                </label>
            </li>);
        }
        return (
            <ul className="root-list">
                {root_list}
            </ul>
        );
    }
}

Main.dafaultProps = {}

Main.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * A list of dash components.
     */
    children: PropTypes.element,
}

export default Main;
