import React, { useState } from 'react';
import PropTypes from 'prop-types';

export default function Click(props) {
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

Click.propTypes = {
    description: PropTypes.string
}