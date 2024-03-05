<template>
    <div id="lulcWrapper" v-if="stageLulc">
        <h4>
            LULC
        </h4>
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
    }
}

</script>

<style>

</style>