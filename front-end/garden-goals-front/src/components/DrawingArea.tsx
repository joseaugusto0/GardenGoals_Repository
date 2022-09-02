import { useEffect, useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup, Tooltip, Rectangle } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw"
import osm from "../osm-providers"
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css"
import { api } from '../lib/api';
import L from "leaflet"

import { useLeafletContext } from '@react-leaflet/core'



export const DrawingArea = () => {

    const [center, setCenter] = useState({lat: 24.4539, lng: 54.3773});
    let [coords, setCoords] = useState(null);
    let [coordsOptimized, setcoordsOptimized] = useState(null);
    const ZOOM_LEVEL = 16;
    const mapRef = useRef(null);
    const featureGroup = useRef(null)

    useEffect(() => {
        if (coords != [] && coords){
            const fetchData = async () => {
                console.log(coords)
                await api.post('/run_solver',coords).then((response) => set_rectangles(response))
            }

            fetchData()
        }
    }, [coords])
    
    function _created(e) {
        const polygon = {
            polygon: e.layerType,
            coordenates: e.layer._latlngs[0]
        } 
        setCoords(polygon)
    }

    function set_rectangles(response){
        
        
        console.log(response.data)
        console.log(coords['coordenates'])

        const first_coordenate = coords['coordenates'][0]
        console.log(first_coordenate['lat'])

    }
   
    return (
        <>
            <div className='row'>
                <div className='col text-center'>
                    <div className='col'>
                        <MapContainer center={center} zoom={ZOOM_LEVEL} ref={mapRef}>
                            <FeatureGroup ref={featureGroup}>
                                <EditControl
                                    position="topright"
                                    draw={{circlemarker: false, marker:false, polyline: false}}
                                    onCreated={(e) => {_created(e)}}
                                />                                
                            </FeatureGroup> 

                            <div>
                                {coordsOptimized && (
                                    coordsOptimized.map((item, index)=>{
                                        return <Rectangle key={index} bounds={index}></Rectangle>
                                    })
                                )}
                            </div>  
                            
                            
                            <Tooltip direction='right' offset={[-8, -2]} opacity={1} permanent>
                                <span>Tes</span></Tooltip>                    
                            <TileLayer url={osm.custom.url} ></TileLayer>
                        </MapContainer>
                    </div>
                </div>
            </div>
        
        </>
    )
};