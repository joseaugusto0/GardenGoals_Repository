import { useEffect, useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup, Tooltip } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw"
import osm from "../osm-providers"
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css"
import { api } from '../lib/api';


export const DrawingArea = () => {

    const [center, setCenter] = useState({lat: 24.4539, lng: 54.3773});
    let [coords, setCoords] = useState(null);
    const ZOOM_LEVEL = 12;
    const mapRef = useRef(null);
    const featureGroup = useRef(null)

    useEffect(() => {
        if (coords != [] && coords){
            api.post('/cordenates',coords).then((response) => console.log(response))
        }
    }, [coords])
    
    function _created(e) {
        const polygon = {
            type: e.layerType,
            coordenates: e.layer._latlngs
        }    

        setCoords(polygon)
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