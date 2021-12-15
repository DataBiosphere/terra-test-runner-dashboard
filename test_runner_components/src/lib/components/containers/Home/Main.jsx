import '../../../styles/app/index.scss'
import '../../../styles/home/index.scss'
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import EnvList from "./EnvList";

class Main extends Component {
    render() {
        const {children} = this.props;
        return (
            <div className="home">
                <div className="home__sidebar">
                    <EnvList children={children}/>
                </div>
                <div className="home__content">
                    <div className="home__content-body">
                        <div className="home__load-status">
                        </div>
                    </div>
                </div>
            </div>
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
