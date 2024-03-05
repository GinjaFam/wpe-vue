<template>
    <div id="hruWrapper" v-if="stageHru">
        <h4>
            Landscape Zones
        </h4>
        <button 
            @click="drawOn"

            class="btn btn-outline-secondary btn-sm" 
            id="hruDrawBtn">
            Draw
        </button>
    </div>
</template>

<script>
import {drawStage} from '@/stores/stage';

export default {
    name: 'Hru',
    computed: {
        stageHru(){
            if (drawStage().stageVar === "hru-stage") {
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