<template>
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">  
        <!-- Can do double attribute - see hx-trigger -->
        <input 
            hx-get="/ws_load"
            hx-target="#wsIsland"
            hx-swap="innerHTML"
            hx-trigger="load, change"  

            type="radio" 
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="wsBtn" 
            autocomplete="off" 
            checked>
        <label class="btn btn-outline-primary" for="wsBtn">Wathersheds</label>

        <input 
            hx-get="/z_load"
            hx-target="#wsIsland"
            hx-swap="innerHTML"

            type="radio" 
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="znBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary" for="znBtn">Zones</label>
        
        <input  
            hx-get="/l_load"
            hx-target="#wsIsland"
            hx-swap="innerHTML"

            type="radio"
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="lulcBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary" for="lulcBtn">LULC</label>

        <input 
            hx-get="/h_load"
            hx-target="#wsIsland"
            hx-swap="innerHTML"

            type="radio" 
            class="btn-check to-clean-map" 
            name="btnradio" 
            id="hruBtn" 
            autocomplete="off">
        <label class="btn btn-outline-primary" for="hruBtn">HRUs</label>
    </div>
</template>

<script>
    export default {
        name: 'Navigation'
    }
</script>