import { defineStore } from 'pinia';
import { userAuthStore } from '@/stores/auth';

// This stores holds the global variables that pertain drawing controls and drawing actions
export const mapStore = defineStore("mapGloStore", {
    // Have a bool to store if the draw controls are active
    // have a bool to store if the draw mode is active
    state: () => ({ 
        drawCtrl: false,
        drawMode: false,
        // Initialize empty geojson objects to store drawn polygons
        
        loadedWatershed: {
            "type": "FeatureCollection",
            "features": [
            ]
        },
        loadedZones: {
            "type": "FeatureCollection",
            "features": [
            ]
        },
        loadedLulcs: {
            "type": "FeatureCollection",
            "features": [
            ]
        },
        loadedHrus: {
            "type": "FeatureCollection",
            "features": [
            ]
        },
    }),
    actions: {
        toggleDrawMode() {
            this.drawMode = !this.drawMode;
            console.log('Drawing Mode: ', this.drawMode);
        },
        activateDrawCtrl() {
            this.drawCtrl = !this.drawCtrl;
            console.log('Draw controls: ',this.drawCtrl);
        },
        loadWatershed() {
            const authStore = userAuthStore();
            console.log('The email is: ',authStore.mailUser);

            fetch('/api/ws_load', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // body: JSON.stringify({
                //     'email': authStore.mailUser,
                // })
            })
            .then(response => {
                if (response.status === 200){
                    return response.json();
                } else { 
                    console.log('The response status is: ', response.status); 
                    return Promise.reject('Failed to load watershed data'); // Reject promise if not OK.
                }
            })
            .then(data => {
                this.loadedWatershed = data;
                console.log('The loaded watershed is: ',this.loadedWatershed);
                return data;
            })
            .catch((error) => console.error('Error loading watershed:', error)); // Handle any errors.
            
        },
    }
});
