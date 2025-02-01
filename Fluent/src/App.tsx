import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  function handleClick() {
    setCount(count+1);
  }

  return (
    <>
      <h1>Free protein</h1>
      <button type="button" onClick={() => handleClick()}>
        {count}g
      </button>
    </>
  )
}

export default App
