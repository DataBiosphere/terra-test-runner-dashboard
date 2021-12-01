import '../../../styles/app/index.scss'
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import {BrowserRouter, Link} from "react-router-dom";
import Main from "../Home/Main";

class MainDash extends Component {
    render() {
        const {id, isPrintModal} = this.props;
        return (
            <BrowserRouter>
                <div id={id} className={classNames('app', {'app--modal-print': isPrintModal})}>
                    <header className="app__header" role="banner">
                        <h1 className="app__title">
                            <Link to="/" arial-label="Go to home page." tabIndex="-1">
                                Test Runner Dashboard
                            </Link>
                        </h1>
                    </header>
                    <main className="app__content" role="main">
                        <Main/>
                    </main>
                </div>
            </BrowserRouter>
        );
    }
}

MainDash.dafaultProps = {}

MainDash.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Values for class name app--modal-print
     */
    isPrintModal: PropTypes.bool.isRequired
}

export default MainDash;
