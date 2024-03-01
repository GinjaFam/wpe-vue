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
                        <button type="submit" @click="loginUser(), toggleModal()" class="btn btn-outline-secondary btn-sm">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { userAuthStore } from '@/stores/auth';
    import { defineComponent } from 'vue';

    export default defineComponent({    
        name: 'Login',
        computed: {
            // Expose the store and its state as a computed property - then i can use it in the DOM
            mailUser() {
                return userAuthStore().mailUser;
            }
        },
        data() {
            return {
                showModal: false, // Ensure this is defined
                userLogginIn: {
                    email: '',
                    password: ''
                }
            };
        },

        methods: {
            toggleModal() {
                this.showModal = !this.showModal;
            },
            submitForm() { 
                if (this.userLogginIn.email === '' || this.userLogginIn.password === '') {
                    alert('Please fill in all fields');
                    return;
                }
                else if (this.mailUser === this.userLogginIn.email) {
                    alert('You are already logged in - If you want to switch account first log out!');
                    return;
                } else {
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
                            if (response.headers.get("Content-Length") === "0") {
                                throw new Error("Empty response from server");
                            }
                            return  response.json();
                        } else {
                            throw new Error('Server responded with an error');
                        }
                    })
                    .then(data => {
                        console.log("Server response:", data);
                        if (data.success === 'success' ) {
                            alert(data.message);
                            this.closeModal();
                            console.log("Logged in user email from server:",data.mail);
                        } else {
                            alert(data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Login error:', error.message);
                        alert(error.message); // Show error message
                    });
                }
            },
            loginUser() {
                const email = this.userLogginIn.email;
                const authStore = userAuthStore();
                authStore.logUserIn(email);
            },
            initForm() {
                this.userLogginIn.email = '';
                this.userLogginIn.password = '';
            },
            closeModal() {
                this.showModal = false;
                this.initForm();
            },
        }, 
    });

</script>
