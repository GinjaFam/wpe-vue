<template>
    <div v-if="showModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Login</h5>
                    <button type="button" @click="toggleModal" class="btn-close" data-bs-dismiss="modal" aria-label="Close">Login</button>
                </div>

                <div class="modal-body">
                    <form @submit.prevent="submitForm" action="/login" method="POST" autocomplete="off">
                        <div class="mb-3">
                            <input v-model="userLogginIn.email" placeholder="E-Mail" type="email" class="form-control">
                        </div>
                        <div class="mb-3">
                            <input v-model="userLogginIn.password" placeholder="Password" type="password" class="form-control">
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
        },
        methods: {
            toggleModal() {
                this.showModal = !this.showModal;
            },
            submitForm() {
                fetch('/api/login', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(this.userLogginIn)
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
                this.userLogginIn.email = '';
                this.userLogginIn.password = '';
            },
            closeModal() {
                this.showModal = false;
                this.initForm();
            }
        } 
    }

</script>
