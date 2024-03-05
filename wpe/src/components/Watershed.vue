<template>
    <div v-if="stageWs">
        <h4>Watersheds</h4>
        <!-- <button @click="fetch">Fetch</button> -->
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
                <tr>
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
                </tr>
                <!-- <tr v-for="ws in wsTable" :key="ws.id">
                    <td>{{ ws.id }}</td>
                    <td>{{ ws.name }}</td>
                    <td>{{ ws.area }}</td>
                </tr> -->
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
                wsTable: null
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
        
        
        methods: {
            drawOn(){
                drawStage().activateDrawCtrl();
            },
            fetch () {
                fetch('/api/ws_load', {
                    method: 'get',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                })
                .then(response => { 
                    if (response.ok) {
                        if (response.headers.get("Content-Length") === "0") {
                            throw new Error("Empty response from server");
                        }
                        return  response.json();
                    } else {
                        throw new Error("Server returned " + response.status + " : " + response.statusText);
                    }
                })
                .then(data => {
                    this.wsTable = data;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        },
    };

</script>

<style>

</style>