import { useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw"
import osm from "../osm-providers"
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css"
import CustomSquare from './Square';

export const DrawingArea = () => {

    const [center, setCenter] = useState({lat: 24.4539, lng: 54.3773});
    const ZOOM_LEVEL = 12;
    const mapRef = useRef();
    const featureGroup = useRef()

    const _created = e => {
        console.log(e)
        if (e.layerType=="rectangle"){
            const coordenates = e.layer._latlngs
        }
    }

    const _export = e => {
        e.layers.eachLayer(a => {
            console.log(a.toGeoJSON())
        });
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
                                    onCreated={_created}
                                    onEdited={_export}

                                />
                            </FeatureGroup>     
                            <TileLayer url={osm.custom.url} ></TileLayer>
                        </MapContainer>
                    </div>
                </div>
            </div>
        
        </>
    )
};