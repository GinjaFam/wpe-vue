<template>
    <div id="user_auth">
        <button type="button" @click="openLoginModal" class="btn btn-outline-secondary btn-sm" data-bs-toggle="modal" data-bs-target="#loginModal">Login</button>
        
        <button type="button" @click="openRegistrationModal" class="btn btn-outline-secondary btn-sm" data-bs-toggle="modal" data-bs-target="#signupModal">Register</button>
        
        <button type="button" @click="logOut" class="btn btn-outline-secondary btn-sm" data-bs-toggle="modal" data-bs-target="#logoutModal">Logout</button>
    </div>
    <Login ref="loginComponent" />
    <Registration ref="registrationComponent" />
    <div>User Email: {{ mailUser }}</div>
</template>

<script>
import Registration from './Register.vue';
import Login from './Login.vue';
import { userAuthStore } from '@/stores/auth';


export default {
    name: 'Auth',
    computed: {
            // Expose the store and its state as a computed property - then i can use it in the DOM
            mailUser() {
                return userAuthStore().mailUser;
            }
        },
    components: {
        Registration,
        Login
    },
    methods: {
        openRegistrationModal() {
            this.$refs.registrationComponent.showModal = true;
            // close the login modal
            this.$refs.loginComponent.showModal = false;

        },
        openLoginModal() {
            this.$refs.loginComponent.showModal = true;
            // close the registration modal
            this.$refs.registrationComponent.showModal = false;
        },
        logOut () {
            // close the registration modal
            this.$refs.registrationComponent.showModal = false;
            this.$refs.loginComponent.showModal = false;
            
            fetch('/api/logout', {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
            })
            .then(response => { 
                if (response.ok) {
                    return response.json();
                } else {
                    throw response.json();
                }
            })
            .then(data => {
                console.log(data);
                // set global variable to null
                const authStore = userAuthStore();
                authStore.logUserOut();
                // redirect to home
                this.$router.push({ path: '/' });
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

    }
}
</script>

<style>
.btn {
    margin: 1px;
}
</style>