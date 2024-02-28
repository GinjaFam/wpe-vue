<template>
    <div id="map" class="map-container"></div>
</template>

<script>
import L from 'leaflet';
import 
// import 'leaflet/dist/leaflet.css';

export default {
    name: 'MainMap',
    mounted() {
        this.initializeMap();
    },
    methods: {
        initializeMap() {
            // Create the map
            const map = L.map('map').fitBounds([
                [11.69364, 0.16169675], // southWest [lat, lng]
                [23.500196, 15.999085]  // northEast [lat, lng]
            ]); //setView([15, 9], 12);

            // Set up the OSM layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            // Can get different providers from http://leaflet-extras.github.io/leaflet-providers/preview/index.html#filter=OpenTopoMap
            new L.basemapsSwitcher([
            {
                layer: L.tileLayer.provider('OpenTopoMap',{
                }).addTo(map), //DEFAULT MAP
                icon: '/static/images/mapIcons/img1.PNG',
                name: 'OpenTopo'
            },

            {
                layer: L.tileLayer.provider('USGS.USImageryTopo'),
                icon: '/static/images/mapIcons/img2.PNG',
                name: 'USGS'
            },

            {
                layer: L.tileLayer.provider('Esri.WorldImagery'),
                icon: '/static/images/mapIcons/img3.PNG',
                name: 'ESRI satellite'
            }

            ], { position: 'topleft' }).addTo(map);

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
.map-container {
height: 400px; /* Set the height of the map */
}
</style>
