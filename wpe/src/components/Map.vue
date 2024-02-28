<template>
    <div id="map" class="map-container"></div>
</template>
  
  <script>

    import L from 'leaflet';
    import 'leaflet-providers';
    import '@geoman-io/leaflet-geoman-free';
    import 'leaflet/dist/leaflet.css'; 
    import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css'; 
    import '../assets/L.switchBasemap.css'; // 
    import { extendLeafletBasemaps } from '../utils/switchBasemap.js'; // Ensure this path is correct
  
    export default {
        name: 'MainMap',
        mounted() {
            extendLeafletBasemaps(); // Extend Leaflet with your custom control first
            this.initializeMap();
        },
        methods: {
            initializeMap() {
                // Create the map
                const map = L.map('map').fitBounds([
                    [11.69364, 0.16169675], // southWest [lat, lng]
                    [23.500196, 15.999085]  // northEast [lat, lng]
                ]);
        
                
        
                // Define basemap layers for the switcher
                const basemapLayers = [
                {
                    layer: L.tileLayer.provider('OpenTopoMap').addTo(map), // Set as default map
                    icon: '/../assets/images/img1.PNG',
                    name: 'OpenTopo'
                },
                {
                    layer: L.tileLayer.provider('USGS.USImageryTopo'),
                    icon: '/assets/static/images/img2.PNG',
                    name: 'USGS'
                },
                {
                    layer: L.tileLayer.provider('Esri.WorldImagery'),
                    icon: '/assets/static/images/img3.PNG',
                    name: 'ESRI satellite'
                }
                ];
        
                // Add the basemap switcher to the map
                L.basemapsSwitcher(basemapLayers, { position: 'topleft' }).addTo(map);
        
                // Add Geoman.io controls
                map.pm.addControls({  
                position: 'topleft',  
                drawCircleMarker: false,
                rotateMode: false,
                drawCircle: false,
                drawRectangle: false,
                drawMarker: false,
                drawText: false
                }); 
            }
        }
    };
  </script>
  
  <style>
#map {
    height: 100vh;
    width: 100vw;
    position: fixed;
}
  </style>
  