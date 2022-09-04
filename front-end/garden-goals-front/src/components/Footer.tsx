import { FormEvent, useEffect, useState } from "react"
import {api} from "../lib/api"

export const Footer = () => {

    const [plants, setPlants] = useState([])
    const [selectedPlants, setSelectedPlants] = useState({
        dropbox0: "",
        dropbox1: "",
        dropbox2: "",
    })


    function onChangeOption(e){
        const id = e.target.getAttribute("id");
        const el = document.getElementById(id);
        setSelectedPlants(selectedPlants => ({
            ...selectedPlants,
            [id]: e.target.value
        }));
    }

    function handleSubmit(event) {
        console.log(selectedPlants)
    }

    
    useEffect(() => {
        async function fetchData() {
            const request = await api.post('/get_plant_infos')
            const body = await request.data;
            
            var values = ["-"]
            body.map((plant,_) => {
                values.push(plant.name)
            })
            setPlants(values)
        }

        fetchData();
        
    }, [])

    return(
        <>
        <div className="flex place-content-between justify-center my-1">
            
            {[...Array(3)].map((_,i) => {
                return <select id={`dropbox${i}`} key={i} onChange={onChangeOption} defaultValue="-">
                    {plants && (
                        plants.map((plant,index) => {
                            return <option  key={index} value={plant}  className="mx-4">{plant}</option>
                        })
                    )}
                </select>                    
            })}
            
            <button className="rounded-2xl px-2 bg-background-300" onClick={handleSubmit}>Enviar</button>
        </div>
            
        </>
    )
   

}