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
    
    import { watch} from 'vue'; 
    import { mapStore } from '@/stores/drawStore';
    import { userAuthStore } from '@/stores/auth';
    import {drawStage} from '@/stores/stage';
    import { map } from 'leaflet';



    export default {
        name: 'MainMap',
        data () { 
            return {
                // map: null,
                watershedLayer: null,
                zoneLayer: null,
                lulcLayer: null,
                hruLayer: null,
                };
        },
        computed: {
            isDrawCtrl() {
                return drawStore().drawCtrl;
            },  
        },
        mounted() {
            const userAuth = userAuthStore();
            extendLeafletBasemaps(); // Extend Leaflet with custom control before initializing the map
            
            this.initializeMap();
            this.controls();
            this.watchDrawControl();
            

            // this.userAuthWatch();
        },

        
       
        methods: {
            initializeMap() {
                // Create the map
                this.map = L.map('map').fitBounds([
                    [11.69364, 0.16169675], // southWest [lat, lng]
                    [23.500196, 15.999085]  // northEast [lat, lng]
                ]);
                console.log('basemapSwitcher',L.basemapsSwitcher);

                // Define basemap layers for the switcher
                const basemapLayers = [
                {
                    layer: L.tileLayer.provider('OpenTopoMap'), // Set as default map
                    icon: '/../assets/images/img1.PNG',
                    name: 'OpenTopo'
                },
                {
                    layer: L.tileLayer.provider('USGS.USImageryTopo'),
                    icon: '/assets/static/images/img2.PNG',
                    name: 'USGS'
                },
                {
                    layer: L.tileLayer.provider('Esri.WorldImagery').addTo(this.map),
                    icon: '/assets/static/images/img3.PNG',
                    name: 'ESRI satellite'
                }
                ];
        
                // Add the basemap switcher to the map
                L.basemapsSwitcher(basemapLayers, { position: 'topleft' }).addTo(this.map);
        
            },
            controls(enable) {
                if (enable === true) {
                    // Add Geoman.io controls
                    this.map.pm.addControls({  
                        position: 'topleft',  
                        drawCircleMarker: false,
                        rotateMode: false,
                        drawCircle: false,
                        drawRectangle: false,
                        drawMarker: false,
                        drawText: false
                    });
                } else {
                    // Remove Geoman.io controls
                    this.map.pm.removeControls();
                }; 
            },
            watchDrawControl() {
                const drawSt = drawStage(); 
                // Watch for changes in drawCtrl and update controls accordingly
                watch(() => drawSt.drawCtrl, (newVal) => {
                    this.controls(newVal);
                });
            },

            setWsLayer() {
                this.watershedLayer = L.geoJSON(mapStore().loadedWatershed, {
                    style: {
                        color: 'blue',
                        weight: 2,
                        opacity: 1
                    }
                }).addTo(this.map);
                console.log('watershedLayer',this.watershedLayer);
            },
            
            
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
  