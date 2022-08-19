import { useEffect } from "react";
import L from "leaflet"
import { useLeafletContext } from '@react-leaflet/core'
//import "../scripts/measurements-leaflet.js"
//import "../scripts/measurements-leaflet.css"


function CustomSquare(props) {
    const context = useLeafletContext()
  
    useEffect(() => {
      const bounds = L.latLng(props.center).toBounds(props.size)
      const square = new L.Rectangle(bounds)
      const container = context.layerContainer || context.map
      
  
      return () => {
        container.removeLayer(square)
      }
    })
  
    return null
  }

export default CustomSquare;