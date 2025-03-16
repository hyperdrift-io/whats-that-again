import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    proxy: {
      '/search': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
