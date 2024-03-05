<template>
    <div id="hruWrapper" v-if="stageHru">
        <h4>
            Landscape Zones
        </h4>
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
    }
}

</script>

<style>

</style>