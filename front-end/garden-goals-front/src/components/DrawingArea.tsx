import { useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup, Tooltip, Rectangle, ScaleControl, Circle } from 'react-leaflet';

import { EditControl } from "react-leaflet-draw"
import osm from "../osm-providers"
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css"
import { Footer } from './Footer';
import { LatLng } from 'leaflet';
window.type = true;


interface iPolygon{
    polygon: string,
    coordenates: LatLng[],
    width: number,
    height: number,
    radius: number
}

export const DrawingArea = () => {

    const [center, setCenter] = useState({lat: 24.4539, lng: 54.3773});
    let [coords, setCoords] = useState<any>(null);
    let [coordsOptimized, setcoordsOptimized] = useState<any[] | null>(null);
    let [circlesOptimized, setcirclesOptimized] = useState<any[] | null>(null);
    const [featureGroup, setFeatureGroup] = useState<any>(null)
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
    
    function _created(e: any) {

        if (e.layerType == 'circle'){
            
            const polygon: iPolygon = {
                polygon: e.layerType,
                coordenates: e.layer._latlng,
                radius: e.layer._mRadius,
                width: 0,
                height: 0
            }
            setCoords(polygon)
            console.log(e)
        }
        
        //Added function to show coordenate if clicked
        if (e.layerType == 'rectangle') {
            e.layer.on('mouseclick', function() {
                console.log(e.layer.getBounds());    
            });

            if (featureGroup){
                featureGroup.addLayer(e.layer);
            }

            const polygon: iPolygon = {
                polygon: e.layerType,
                coordenates: e.layer._latlngs[0],
                height: e.layer._latlngs[0][0].distanceTo(e.layer._latlngs[0][1]),
                width: e.layer._latlngs[0][1].distanceTo(e.layer._latlngs[0][2]),
                radius: 0
            }
            setCoords(polygon)
        }
            


    }

    return (
        <>
            <div className='row'>
                <div className='col text-center'>
                    <div className='col'>
                        <MapContainer center={center} zoom={ZOOM_LEVEL}>
                            <FeatureGroup ref={setFeatureGroup}>
                                
                                <EditControl
                                    position="topright"
                                    draw={
                                        {
                                            polygon: false, 
                                            circlemarker: false, 
                                            marker:false, 
                                            polyline: false
                                        }
                                    }
                                    onCreated={(e) => {_created(e)}}
                                />  
                                                              
                            </FeatureGroup> 

                            <div>
                                {
                                coordsOptimized && (
                                    coordsOptimized.map((bounds, index)=>{
                                        return <Rectangle key={index} bounds={[bounds[0],bounds[1]]} color={bounds[2]}></Rectangle>

                                    })
                                )}
                                {
                                circlesOptimized && (
                                    circlesOptimized['coordenates'].map((coords, index)=>{
                                       
                                        return <Circle key={index} center={[coords['lat'],coords['lng']]} radius={circlesOptimized['radius'][index]}></Circle>

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
            <Footer coords={coords} setCoordsInFront={setcoordsOptimized} setCirclesInFront={setcirclesOptimized}></Footer>
        
        </>
    )
};