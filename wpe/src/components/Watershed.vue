<template>
    <div v-if="stageWs">
        <h4>Watersheds</h4>
        <button @click="fetchWithDelay()">Fetch</button>
        <button 
            @click="drawOn"

            class="btn btn-outline-secondary btn-sm" 
            id="wsDrawBtn">
            Draw
        </button>
        <table class="table table-sm table-hover table-striped">
            <thead>
                <tr>
                    <th>Watershed ID</th>
                    <th>Watershed Name</th>
                    <th>Watershed Area</th>
                </tr>
            </thead>
            <tbody>
                <!-- <tr>
                    <td>foo</td>
                    <td>foo</td>
                    <td>foo</td>
                </tr>
                <tr>
                    <td>buz</td>
                    <td>bux</td>
                    <td>buz</td>
                </tr>
                <tr>
                    <td>boo</td>
                    <td>booo</td>
                    <td>boo</td>
                </tr> -->
                <tr v-for="ws in wsTable" :key="ws.id">
                    <td>{{ ws.id }}</td>
                    <td>{{ ws.name }}</td>
                    <td>{{ ws.area }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { computed } from 'vue';
import { userAuthStore } from '@/stores/auth';
import { drawStage } from '@/stores/stage';

    export default {
        
        name: 'Watershed',
        data() {
            return {
                wsTable: []
            };
        },

        computed: {
            stageWs(){
                if (drawStage().stageVar === "watershed-stage") {
                    return true;
                } else {
                    return false;
                }
            }
        },
        
        // mounted() {
        //     this.fetch();
        //     console.log(localStorage.getItem('access_token'))
        // },
        methods: {
            drawOn(){
                drawStage().activateDrawCtrl();
            },
            fetchWithDelay() {
                setTimeout(this.fetch, 0); // Wait for 1 second before calling fetch
            },
            // Fetches data from the server
            fetch () {
                const token = localStorage.getItem('access_token');
                fetch('/api/ws_load', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                })
                .then(response => { 
                    if (!response.ok) {
                        // Throw an error with status text, which will be caught by the catch block
                        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
                    }
                    return response.json(); // Parse JSON regardless of Content-Length
                })
                .then(data => {
                    // Check if the data object is empty after parsing
                    if (Object.keys(data).length === 0 && data.constructor === Object) {
                        throw new Error("Empty response from server");
                    }
                    // Assign the fetched data to the wsTable property
                    this.wsTable = data;
                    // Optional: Log the data for debugging
                    console.log('Fetched data:', data);
                })
                .catch(error => {
                    // Log any errors that occur during the fetch operation
                    console.error('Fetch Error:', error);
                });
            }
            }
        }
    

</script>

<style>

</style>