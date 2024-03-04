import { defineStore } from 'pinia';


// Define the store and its properties
export const drawStage = defineStore("stage", {
    // The state of the store
    state: () => ({ 
        stageVar: null
    }),
    // The actions of the store
    actions: {
        // The action to log in the user
        registerStage(currentStage) {
            // Set the user data and the logged in status
            this.clearStage()
            this.stageVar = null;
            this.stageVar = currentStage;
            console.log('The current stage in store is', this.stageVar);
        },
        clearStage() {
            this.stageVar = null;
            console.log('Stage cleared in store');
        }
    }
});
