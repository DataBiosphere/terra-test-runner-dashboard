import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * A function component that increments a counter by clicking.
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
export function ClickCount(props) {
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

ClickCount.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string
}