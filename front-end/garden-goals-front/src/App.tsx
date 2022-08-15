import { useState } from 'react'
import { DrawingArea } from './components/DrawingArea'
import Header from './components/Header'


function App() {

  return (
      <>
        <Header name="José"></Header>
        <DrawingArea className="mr-2"></DrawingArea>
        <button>Teste</button>
      </>
  )
}

export default App
