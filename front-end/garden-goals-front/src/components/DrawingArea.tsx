import { useEffect, useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup, Tooltip, Rectangle, ScaleControl } from 'react-leaflet';

import { EditControl } from "react-leaflet-draw"
import osm from "../osm-providers"
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css"
import 'leaflet-geometryutil'
import { Footer } from './Footer';



export const DrawingArea = () => {

    const [center, setCenter] = useState({lat: 24.4539, lng: 54.3773});
    let [coords, setCoords] = useState(null);
    let [coordsOptimized, setcoordsOptimized] = useState<number[] | null>(null);
    const [map, setMap] = useState(null)
    const [featureGroup, setFeatureGroup] = useState(null)
    const ZOOM_LEVEL = 16;
    const scaleRef = useRef(null)

    //useEffect(() => {
    //    if (coords != [] && coords){
    //        const fetchData = async () => {
    //            await api.post('/run_solver',coords).then((response) => set_rectangles(response))
    //        }
    //        fetchData()
    //    }
    //}, [coords])
    
    function _created(e) {

        //Added function to show coordenate if clicked
        if (e.layerType === 'rectangle') {
            e.layer.on('mouseclick', function() {
                console.log(e.layer.getBounds());    
            });
        }
    
        featureGroup.addLayer(e.layer);

        const polygon = {
            polygon: e.layerType,
            coordenates: e.layer._latlngs[0],
            width: e.layer._latlngs[0][0].distanceTo(e.layer._latlngs[0][1]),
            height: e.layer._latlngs[0][1].distanceTo(e.layer._latlngs[0][2])
        }
        setCoords(polygon)
    }

    return (
        <>
            <div className='row'>
                <div className='col text-center'>
                    <div className='col'>
                        <MapContainer center={center} zoom={ZOOM_LEVEL} ref={setMap}>
                            <FeatureGroup ref={setFeatureGroup}>
                                
                                <EditControl
                                    position="topright"
                                    draw={{circle: false, polygon: false, circlemarker: false, marker:false, polyline: false}}
                                    onCreated={(e) => {_created(e)}}
                                />  
                                                              
                            </FeatureGroup> 

                            <div>
                                {
                                coordsOptimized && (
                                    coordsOptimized.map((bounds, index)=>{
                                        return <Rectangle key={index} bounds={bounds} color='green'></Rectangle>

                                    })
                                )}
                            </div>  

                            <ScaleControl ref={scaleRef}></ScaleControl>
                            <Tooltip direction='right' offset={[-8, -2]} opacity={1} permanent>
                                </Tooltip>                    
                            <TileLayer url={osm.custom.url} ></TileLayer>
                        </MapContainer>
                    </div>
                </div>
            </div>
            <Footer coords={coords} setCoordsInFront={setcoordsOptimized}></Footer>
        
        </>
    )
};