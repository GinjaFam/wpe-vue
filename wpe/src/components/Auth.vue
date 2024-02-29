<template>
    <div id="user_auth">
        <button type="button" @click="openLoginModal" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">Login</button>
        <Registration ref="registrationComponent" />
        <button type="button" @click="openRegistrationModal" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#signupModal">Register</button>
        <Login ref="loginComponent" />
        <button type="button" @click="logOut" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#logoutModal">Logout</button>
    </div>
</template>

<script>
import Registration from './Register.vue';
import Login from './Login.vue';
import { userAuthStore } from '@/stores/auth';


export default {
    name: 'Auth',
    components: {
        Registration,
        Login
    },
    methods: {
        openRegistrationModal() {
            this.$refs.registrationComponent.showModal = true;
        },
        openLoginModal() {
            this.$refs.loginComponent.showModal = true;
        },
        logOut () {
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