<template>
    <div id="zoneWrapper" v-if="stageZn">
        <h4>
            Landscape Zones
        </h4>
        <button 
            @click="drawOn"
            class="btn btn-outline-secondary btn-sm" 
            id="znDrawBtn">
            Draw
        </button>
    </div>
</template>

<script>
import {drawStage} from '@/stores/stage';

export default {
    name: 'Zone',
    computed: {
        stageZn(){
            if (drawStage().stageVar === "zone-stage") {
                return true;
            } else {
                return false;
            }
        }
    },
    methods: {
        drawOn(){
            drawStage().activateDrawCtrl();
        },
    }
}

</script>

<style>

</style>