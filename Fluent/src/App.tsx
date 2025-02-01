import { useState } from 'react'

function App() {
  const [value, setValue] = useState('');
  const [count, setCount] = useState(0)

  function handleClick() {
    setCount(count+1);
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setValue(event.target.value);
  }

  return (
    <div>      
      <h1>Fluent</h1>
      <button type="button" onClick={() => handleClick()}>
        {count}g
      </button>
      <input type="text" value={value} onChange={(value) => handleChange(value)} />
      <p>Value: {value}</p>
    </div>
  )
}

export default App
