import { FormEvent, useState } from "react"
import {api} from "../lib/api"

export const Footer = () => {

    const [sendCoords, setSendCoords] = useState(null)

    async function handleSentButton(event: React.MouseEvent<HTMLElement>){
        console.log(event)

        await api.post('/feedback',{
            type: feedbackType,
            comment,
            screenshot
        })
    } 

    return(
        <>
            <button 
                className="flex-1" 
                onClick={(event) => handleSentButton(event)}
            >Teste</button>
    
        </>
    )
   

}