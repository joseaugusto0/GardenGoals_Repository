import { useState } from 'react'
import { DrawingArea } from './components/DrawingArea'
import { Footer } from './components/Footer'
import Header from './components/Header'


function App() {

  return (
      <>
        <Header name="José"></Header>
        <DrawingArea className="mr-2"></DrawingArea>
        <Footer></Footer>
      </>
  )
}

export default App
