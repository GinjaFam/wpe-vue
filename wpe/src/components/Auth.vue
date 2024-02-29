<template>
    <div id="user_auth">
        <button type="button" @click="openLoginModal" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">Login</button>
        <Registration ref="registrationComponent" />
        <button type="button" @click="openRegistrationModal" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#signupModal">Register</button>
        <Login ref="loginComponent" />
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#logoutModal">Logout</button>
    </div>
</template>

<script>
import Registration from './Register.vue';
import Login from './Login.vue';

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
        }

    }
}
</script>