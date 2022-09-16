import { ChangeEvent, Dispatch, MouseEvent, SetStateAction, useEffect, useState } from "react"
import { AxiosResponse } from "axios"
import { api } from "../lib/api"
import { LatLng } from "leaflet"
import  GeometryUtil  from 'leaflet-geometryutil'

interface iCoordsToSubmit{
    coords: {
        polygon: string,
        coordenates: LatLng[],
        width: number,
        height: number,
        radius: number
    },
    setCoordsInFront: Dispatch<SetStateAction<number[] | null>>,
    setCirclesInFront: Dispatch<SetStateAction<number[] | null>>
}

interface iPlantInfos{
    name: string,
    space_between_lines: number,
    space_between_plants: number
}

export const Footer = ({coords, setCoordsInFront, setCirclesInFront}: iCoordsToSubmit) => {

    
    var _coordsToSubmit = coords
    const _setCoordsInFront = setCoordsInFront
    const _setCirclesInFront = setCirclesInFront
    const [plants, setPlants] = useState<string[]>([])
    const [selectedPlants, setSelectedPlants] = useState({
        dropbox0: "",
        dropbox1: "",
        dropbox2: "",
    })


    const onChangeOption = (e: ChangeEvent<HTMLSelectElement>) => {
        if (e.target.value!="-"){
            const id: string|null = e.target.getAttribute("id");

            if (id){
                setSelectedPlants(selectedPlants => ({
                    ...selectedPlants,
                    [id]: e.target.value
                }));
            }
        }
    }

    const handleSubmit = (event: MouseEvent<HTMLButtonElement>) => {
        event.preventDefault()
        var submitInfos = {..._coordsToSubmit, selectedPlants}
        
        const runSolver = async function () {
            await api.post('/run_solver',submitInfos).then((response) => set_rectangles_in_front(response))
        }

        runSolver()
    }

    function set_response_for_rectangle(response: AxiosResponse){
        const first_coordenate: LatLng = _coordsToSubmit['coordenates'][0]
        var new_coordenates: any = [];

        for (var key in response.data.x){
            var new_point_2: LatLng;
            
            var value: LatLng = GeometryUtil.destination(first_coordenate,90,response.data.x[key])
            value = GeometryUtil.destination(value,0,response.data.y[key]+response.data.w[key])
            new_point_2 = GeometryUtil.destination(value,90,response.data.h[key])
            new_point_2 = GeometryUtil.destination(new_point_2,180,response.data.w[key])
            
            new_coordenates.push([value,new_point_2])
        }
       
        _setCoordsInFront(new_coordenates)
    }

    function set_response_for_circle_with_circle(response: AxiosResponse){

        var first_coordenate: LatLng = _coordsToSubmit['coordenates']
        var new_coordenates: any = [];
        var radius: any = [];

        for (var key in response.data.x){
            var x: LatLng;
            var y: LatLng;
            x = GeometryUtil.destination(first_coordenate,90,response.data.x[key])
            y = GeometryUtil.destination(x,180,response.data.y[key])

            new_coordenates.push(y)
            radius.push(response.data.item_radius[key])

            //var value: LatLng = GeometryUtil.destination(first_coordenate,90,response.data.x[key])
            //value = GeometryUtil.destination(value,0,response.data.y[key]+response.data.w[key])
            //new_point_2 = GeometryUtil.destination(value,90,response.data.h[key])
            //new_point_2 = GeometryUtil.destination(new_point_2,180,response.data.w[key])
        }
        
        var infos ={
            'coordenates': new_coordenates,
            'radius': radius
        }
        console.log(response.data)
        _setCirclesInFront(infos)
    }

    function set_response_for_circle(response: AxiosResponse){
        const square_circunscripted_side = (2*_coordsToSubmit.radius)/Math.sqrt(2)
        const center_coordenate: LatLng = _coordsToSubmit['coordenates']
        var new_coordenates: any = [];
        var first_coordenate = GeometryUtil.destination(center_coordenate,270,square_circunscripted_side/2)
        first_coordenate = GeometryUtil.destination(first_coordenate,180,square_circunscripted_side/2)

        for (var key in response.data.x){
            var new_point_2: LatLng;
            
            var value: LatLng = GeometryUtil.destination(first_coordenate,90,response.data.x[key])
            value = GeometryUtil.destination(value,0,response.data.y[key]+response.data.w[key])
            new_point_2 = GeometryUtil.destination(value,90,response.data.h[key])
            new_point_2 = GeometryUtil.destination(new_point_2,180,response.data.w[key])
            
            new_coordenates.push([value,new_point_2])
        }
        

        _setCoordsInFront(new_coordenates)

    }

    function set_rectangles_in_front(response: AxiosResponse){
        console.log(response.data)
        if (response.data.polygon[0]=='rectangle'){
            set_response_for_rectangle(response)
        }else if (response.data.polygon[0]=='circle'){
            if (response.data.optimizer_type[0]=="circle_packing"){
                set_response_for_circle_with_circle(response)
            }else{
                set_response_for_circle(response)
            }
            
        }
        
    }

    
    useEffect(() => {
        async function fetchData() {
            const request = await api.post('/get_plant_infos')
            const body = await request.data;
            console.log(request)
            var values = ["-"]
            body.map(({name,space_between_lines,space_between_plants}: iPlantInfos) => {
                values.push(name)
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