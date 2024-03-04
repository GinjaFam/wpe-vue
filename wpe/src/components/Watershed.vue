<template>
    <div>
        <h1>Watersheds</h1>
        <button @click="fetch">Fetch</button>
        <table>
            <thead>
                <tr>
                    <th>Watershed ID</th>
                    <th>Watershed Name</th>
                    <th>Watershed Area</th>
                </tr>
            </thead>
            <tbody>
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
                wsTable: null
            };
        },
        methods: {
            fetch () {
                fetch('/api/watershed', {
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