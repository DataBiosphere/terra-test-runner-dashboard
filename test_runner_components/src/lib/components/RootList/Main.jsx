import './root-list.scss'

import React, {Component} from 'react';
import PropTypes from 'prop-types';

class Main extends Component {
    render() {
        return (
            <ul className="root-list">
                <li key="root-key">
                    <label className="root-list__card">
                        <span className="root-list__name">DEV</span>
                        <span className="root-list__root">7</span>
                    </label>
                </li>
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
}

export default Main;
