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

