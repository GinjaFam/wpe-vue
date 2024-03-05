<template>
    <div v-if="isLoggedIn" class="btn-group" role="group" aria-label="Basic radio toggle button group">  
        <input
            v-model="selectedStage"
            @click="controlsOff()"

            type="radio"
            value="watershed-stage" 
            class="btn-check"
            name="btnradio" 
            id="wsBtn" 
            autocomplete="off" 
            checked>
        <label class="btn btn-outline-primary btn-sm" for="wsBtn">Wathersheds</label>

        <input 
            v-model="selectedStage"
            @click="controlsOff()"    

            type="radio" 
            value="zone-stage"
            class="btn-check" 
            name="btnradio" 
            id="znBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary btn-sm" for="znBtn">Zones</label>
        
        <input  
            v-model="selectedStage"
            @click="controlsOff()"

            type="radio"
            value="lulc-stage"
            class="btn-check" 
            name="btnradio" 
            id="lulcBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary btn-sm" for="lulcBtn">LULC</label>

        <input 
            v-model="selectedStage"
            @click="controlsOff()"

            type="radio" 
            value="hru-stage"
            class="btn-check" 
            name="btnradio" 
            id="hruBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary btn-sm" for="hruBtn">HRUs</label>
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
            drawCtrl() {
                return drawStage().drawCtrl;
                
            }
        },
        watch: {
            // Watcher to react whenever the selected radio-button changes
            selectedStage(newStage) {
            const stageStore  = drawStage();
            // Then register the stage 
            stageStore.registerStage(newStage);
            
            }
        },
        methods: {
            controlsOff() {
                drawStage().drawCtrl = false; 
            },
            
        }
        
    };

</script>