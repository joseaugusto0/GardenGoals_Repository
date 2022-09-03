import { useEffect, useRef, useState } from 'react';
import { TileLayer, MapContainer, FeatureGroup, Tooltip, Rectangle, ScaleControl, useMap  } from 'react-leaflet';
import withLeaflet from 'react-leaflet'
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
    const [map, setMap] = useState(null)
    const [featureGroup, setFeatureGroup] = useState(null)
    const ZOOM_LEVEL = 16;
    const scaleRef = useRef(null)

    //const MeasureControl = withLeaflet(MeasureControlDefault);
    const measureOptions = {
        position: 'topright',
        primaryLengthUnit: 'meters',
        secondaryLengthUnit: 'kilometers',
        primaryAreaUnit: 'sqmeters',
        secondaryAreaUnit: 'acres',
        activeColor: '#db4a29',
        completedColor: '#9b2d14'
      };

    useEffect(() => {
        if (coords != [] && coords){
            const fetchData = async () => {
                await api.post('/run_solver',coords).then((response) => set_rectangles(response))
            }

            fetchData()
        }
    }, [coords])
    
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

    function set_rectangles(response){
        
        const first_coordenate = coords['coordenates'][0]
        var new_coordenates = []
        var cont = 0

        for (var key in response.data.x){
            var new_point_2 = null
                 
            //console.log(response.data.x[key]+response.data.h[key])
            
            var value = L.GeometryUtil.destination(first_coordenate,90,response.data.x[key])
            value = L.GeometryUtil.destination(value,0,response.data.y[key]+response.data.w[key])
            new_point_2 = L.GeometryUtil.destination(value,90,response.data.h[key])
            new_point_2 = L.GeometryUtil.destination(new_point_2,180,response.data.w[key])
            
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
                        <MapContainer center={center} zoom={ZOOM_LEVEL} ref={setMap}>
                            <FeatureGroup ref={setFeatureGroup}>
                                
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
                            <ScaleControl ref={scaleRef}></ScaleControl>
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