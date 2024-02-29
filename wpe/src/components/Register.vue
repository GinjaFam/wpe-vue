<template>
    <div v-if="showModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Signup</h5>
                    <button type="button" @click="toggleModal" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
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
    name: 'Register',
    data() {
        return {
            showModal: false,
            user: {
                name: '',
                last_name: '',
                username: '',
                organization: '',
                email: '',
                country: '',
                language: '',
                password: '',
                confirm_password: '',
                newsletter: false,
            }
        }
    },
    methods: {
        toggleModal() {
            this.showModal = !this.showModal;
        },
        submitForm() {
            fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(this.user),
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw response.json();
                }
            })
            .then(data => {
                if (data.success) {
                    alert(data.success);
                }
                this.closeModal();
            })
            .catch(async (errorPromise) => {
                const errorData = await errorPromise;
                if (errorData.errors) {
                    this.errors = errorData.errors;
                } else if (errorData.error) {
                    alert(errorData.error);
                }
            });
        },
        initForm() {
            this.user.name = '';
            this.user.last_name = '';
            this.user.username = '';
            this.user.organization = '';
            this.user.email = '';
            this.user.country = '';
            this.user.language = '';
            this.user.password = '';
            this.user.confirm_password = '';
            this.user.newsletter = false;
        },
        closeModal() {
            this.showModal = false; // Close the modal
            this.initForm(); // Clear the form
        }
    }
}
</script>
