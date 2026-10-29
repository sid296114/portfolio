import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// 管理后台前端：dev 端口 5175，/api 代理到后端 8002
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    port: 5175,
    proxy: {
      '/api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
    },
  },
})
