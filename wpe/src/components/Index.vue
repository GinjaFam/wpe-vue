<template>
    <div id="map-wrapper">
        <MainMap/>
    </div>

    <!-- Keep bootstrap to work only on the left of the screen, done with css ion the wrapper -->
    <div id="sidebar-wrapper">
        <div class="container-fluid">
            <div class="row">
            <div class="col-md-12">      
                <div id="sidebar">
                <div id="sidebarContent">

                    <div id="sidebarTitle">
                        <h1>Water Potential Estimator</h1>
                    </div>
                    
                    <div id="user_auth">
                        <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal">Login</a>
                        {%include 'snippets/login.html'%}
                        <a href="#" data-bs-toggle="modal" data-bs-target="#signupModal">Register</a>
                        {%include 'snippets/registration.html'%}
                        <a href="#" data-bs-toggle="modal" data-bs-target="#logoutModal">Logout</a>
                        {%include 'snippets/logout.html'%}
                    </div>
                    
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

                    <div id="wsIsland"></div>
                    </div>
                </div>  
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
    import MainMap from './Map.vue'

    export default {
        name: 'Index',
        components: {
            MainMap: () => import('./Map.vue')
        }
    }
</script>