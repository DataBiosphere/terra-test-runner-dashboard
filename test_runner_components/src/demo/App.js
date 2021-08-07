/* eslint no-magic-numbers: 0 */
import React, {Component} from 'react';

import { ExampleComponent, Welcome } from '../lib';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            value: ''
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        return (
            <div>
                <ExampleComponent
                    setProps={this.setProps}
                    {...this.state}
                />
                <Welcome name={"TestRunner"} />
            </div>
        )
    }
}

export default App;
