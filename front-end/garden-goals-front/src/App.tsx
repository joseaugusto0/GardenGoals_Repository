import { DrawingArea } from './components/DrawingArea'
import Header from './components/Header'


function App() {

  return (
      <>
        <Header name="José"></Header>
        <div className="mr-2">
          <DrawingArea></DrawingArea>
        </div>
        
      </>
  )
}

export default App
