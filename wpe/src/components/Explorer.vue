<template>
    <div id="explorerWrapper" v-if="isLoggedIn">   
        <h3>Explorer</h3>
        <Watershed/>
        <Zone/>
        <Lulc/>
        <Hru/>
    </div>
</template>

<script>

import Watershed from './Watershed.vue';
import Zone from './Zone.vue';
import Lulc from './Lulc.vue';
import Hru from './Hru.vue';    
import { userAuthStore } from '@/stores/auth';

export default {
    name: 'Explorer',
    components: {
        Watershed,
        Zone,
        Lulc,
        Hru
    },
    computed: {
        // Expose the store and its state as a computed property - then i can use it in the DOM
        isLoggedIn() {
            return userAuthStore().mailUser;
        },
    },
}


</script>

<style>
/* for children tables */
.table {
    margin-top: 10px;
}
</style>