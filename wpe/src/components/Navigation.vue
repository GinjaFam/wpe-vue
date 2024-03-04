<template>
    <div v-if="isLoggedIn" class="btn-group" role="group" aria-label="Basic radio toggle button group">  
        <input
            v-model="selectedStage"

            type="radio"
            value="watershed-stage" 
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="wsBtn" 
            autocomplete="off" 
            checked>
        <label class="btn btn-outline-primary" for="wsBtn">Wathersheds</label>

        <input 
            v-model="selectedStage"    

            type="radio" 
            value="zone-stage"
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="znBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary" for="znBtn">Zones</label>
        
        <input  
            v-model="selectedStage"

            type="radio"
            value="lulc-stage"
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="lulcBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary" for="lulcBtn">LULC</label>

        <input 
            v-model="selectedStage"

            type="radio" 
            value="hru-stage"
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="hruBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary" for="hruBtn">HRUs</label>
    </div>

</template>

<script>
import { computed } from 'vue';
import { userAuthStore } from '@/stores/auth';
import { drawStage } from '@/stores/stage';

    export default {
        
        name: 'Navigation',
        data() {
            return {
                selectedStage: 'watershed-stage'
            };
        },
        computed: {
            // Expose the store and its state as a computed property - then i can use it in the DOM
            isLoggedIn() {
                return userAuthStore().mailUser;
            },
        },
        watch: {
            // Watcher to react whenever the selected stage changes
            selectedStage(newStage) {
            const stageStore  = drawStage();
            stageStore.registerStage(newStage);
            // Here you can also call methods or perform actions based on the newStage
            // For example, updating a store or triggering side effects
            }
        }
    };

</script>