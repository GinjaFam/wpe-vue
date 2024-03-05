Install node to have access to npm
then with npm install vue via vite with > npm install vue@latest


CORS fuckup

So the flask server in the terminal is not the real address exposed. But codespaces uses something more comple that you can see if you open the url ( something like: 'https://verbose-invention-965wj5xpvjxfp4-5000.app.github.dev') instead of http://127.0.0.1:5000.

This will cause all sort of CORS problems. Even if you set CORS correctly in flask.

That is why you need to change the setings in vite.config.js to the following (the server bit is the new part)

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      // Proxying API requests to your backend server
      '^/api': {
        // The target should be the base URL of your backend server
        target: 'https://verbose-invention-965wj5xpvjxfp4-5000.app.github.dev',
        changeOrigin: true, // Needed for virtual hosted sites
        secure: false, // If the backend uses self-signed certificates, for example
        rewrite: (path) => path.replace(/^\/api/, ''), // Optional: Rewrite the API request path if necessary
      },
    },
  },
})


    
    
    server: {
    proxy: {
      // Proxying API requests to your backend server
      '/api': {
        // The target should be the base URL of your backend server
        target: 'https://verbose-invention-965wj5xpvjxfp4-5000.app.github.dev',
        changeOrigin: true, // Needed for virtual hosted sites
        secure: false, // If the backend uses self-signed certificates, for example
        rewrite: (path) => path.replace(/^\/api/, ''), // Optional: Rewrite the API request path if necessary
      },
    },

    