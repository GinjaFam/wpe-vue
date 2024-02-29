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
                            <Auth/>
                            <Navigation/>
                        </div> 
                    </div>
                </div>  
            </div>
        </div>
    </div>


</template>

<script>
import MainMap from './Map.vue';
import Auth from './Auth.vue';
import Navigation from './Navigation.vue';

    export default {
        name: 'Home',
        components: {
            MainMap, //: () => import('./Map.vue'),
            Auth, //: () => import('./Auth.vue'),
            Navigation, //: () => import('./Navigation.vue')
        }
    }
</script>

<style>

    #sidebar-wrapper {
        width: 25%; /* Sidebar takes up 1/4th of the screen width */
        position: absolute; /* if not absolute the modals will be grayed out */
        right: 0; 
        top: 0; 
        margin-right: 15px; 
        overflow: auto; 
        background-color: rgba(255,255,0,0); 
    } 

    #title {
        position: absolute;
        left: 30%;
        font-size: 45px;
        z-index: 1;
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 4px;
        padding: 10px;
        font-family: Verdana, Geneva, Tahoma, sans-serif;
        color: rgba(0, 0, 0, 0.65);
    }
</style>