import { useState } from 'react'
import Header from './components/Header'

function App() {
  const [count, setCount] = useState(0)

  return (
    <body>
      <div>
        <Header name="José"></Header>
      </div>
    </body>
  )
}

export default App
