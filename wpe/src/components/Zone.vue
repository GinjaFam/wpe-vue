<template>
    <div id="zoneWrapper" v-if="stageZn">
        <h4>
            Landscape Zones
        </h4>
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
    }
}

</script>

<style>

</style>