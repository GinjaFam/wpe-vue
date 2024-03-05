import { defineStore } from 'pinia';


// Define the store and its properties
export const userAuthStore = defineStore("auth", {
    // The state of the store
    state: () => ({ 
        isLoggedIn: false,
        mailUser: null,
    }),
    // The actions of the store
    actions: {
        // The action to log in the user
        logUserIn(userData) {
            // Set the user data and the logged in status
            this.isLoggedIn = true;
            this.mailUser = userData;
            console.log('The logged in user un store is', this.mailUser);
        },
        logUserOut() {
            this.isLoggedIn = false;
            this.mailUser = null;
            console.log('The logged out user is: ',this.mailUser);
        }
    }
});
