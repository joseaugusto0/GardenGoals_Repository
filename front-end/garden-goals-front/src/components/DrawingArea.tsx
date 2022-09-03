import { useEffect, useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup, Tooltip, Rectangle } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw"
import osm from "../osm-providers"
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css"
import { api } from '../lib/api';
import 'leaflet-geometryutil'
import  * as L  from 'leaflet'



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
        const first_coordenate = coords['coordenates'][0]
        var new_coordenates = []
        console.log(first_coordenate)
        for (var key in response.data.x){
            var new_point_2 = null
            
            var value = L.GeometryUtil.destination(first_coordenate,0,response.data.x[key]+response.data.h[key])
            value = L.GeometryUtil.destination(value,90,response.data.y[key])
            new_point_2 = L.GeometryUtil.destination(value,90,response.data.w[key])
            new_point_2 = L.GeometryUtil.destination(new_point_2,180,response.data.h[key])
            
            //value = L.GeometryUtil.destination(first_coordenate,90,response.data.y[key]+response.data.h[key])
            console.log(response.data.x[key],response.data.w[key])
            console.log(value)
            //console.log(first_coordenate.distanceTo(value))
            //new_point_2.push(L.GeometryUtil.destination(first_coordenate,90,response.data.x[key] + response.data.w[key]))


            //new_point_1.push(L.GeometryUtil.destination(first_coordenate,90,response.data.y[key]))
            
            new_coordenates.push([value,new_point_2])
        }
       
        setcoordsOptimized(new_coordenates)
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
                                {
                                coordsOptimized && (
                                    coordsOptimized.map((bounds, index)=>{
                                        
                                        //console.log(coordsOptimized)
                                        return <Rectangle key={index} bounds={bounds} color='green'></Rectangle>

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