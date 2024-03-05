import { defineStore } from 'pinia';


// Define the store and its properties
export const drawStage = defineStore("stage", {
    // The state of the store
    state: () => ({ 
        stageVar: null,
        drawCtrl: false
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
        },
        activateDrawCtrl() {
            this.drawCtrl = true;
            console.log('Draw controls: ',this.drawCtrl);
        },
        deactivateDrawCtrl() {
            this.drawCtrl = false;
            console.log('Draw controls: ',this.drawCtrl);
        }
    }
});
