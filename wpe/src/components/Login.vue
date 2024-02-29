<template>
    <div v-if="showModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Login</h5>
                    <button type="button" @click="toggleModal" class="btn-close" data-bs-dismiss="modal" aria-label="Close">Login</button>
                </div>

                <div class="modal-body">
                    <form @submit.prevent="submitForm" action="/register" method="POST" autocomplete="off">
                        <div class="mb-3">
                            <input v-model="user.name" placeholder="Name" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.last_name" placeholder="Last Name" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.username" placeholder="Username" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.organization" placeholder="Organization" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.email" placeholder="Email" type="email" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.country" placeholder="Country" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.language" placeholder="Language" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.password" placeholder="Password" type="password" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="user.confirm_password" placeholder="Confirm Password" type="password" class="form-control">
                        </div>
                        <div class="mb-3 form-check">
                            <input v-model="user.newsletter" type="checkbox" class="form-check-input">
                            <label class="form-check-label">Subscribe to newsletter</label>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Login',
        data() {
            return {
                showModal: false,
                userLogginIn: {
                    email: '',
                    password: ''
                }
        }
    }
</script>