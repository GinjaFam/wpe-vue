<template>
    <div id="lulcWrapper" v-if="stageLulc">
        <h4>
            LULC
        </h4>
        <button 
            @click="drawOn"

            class="btn btn-outline-secondary btn-sm" 
            id="lulcDrawBtn">
            Draw
        </button>
    </div>
</template>

<script>
import {drawStage} from '@/stores/stage';

export default {
    name: 'Lulc',
    computed: {
        stageLulc(){
            if (drawStage().stageVar === "lulc-stage") {
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