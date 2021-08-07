import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * A function component that increments a counter by hook.
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
export function ExampleFuncComponentWithHook(props) {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  )
}

ExampleFuncComponentWithHook.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string
}