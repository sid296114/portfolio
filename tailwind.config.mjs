/** @type {import('tailwindcss').Config} */
export default {
  // 明暗主题：class 策略，由 <html> 上的 dark class 控制
  darkMode: 'class',
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // 主色：低饱和灰蓝
        primary: '#446688',
        'primary-hover': '#35557a',
        // 辅助色：浅青
        accent: '#68b8b8',
        'accent-hover': '#56a6a6',
        // 浅色模式
        light: {
          bg: '#f7f5f0',
          text: '#333333',
          'text-secondary': '#666666',
          card: '#ffffff',
          border: '#e5e0d6',
        },
        // 深色模式
        dark: {
          bg: '#1f2429',
          text: '#e6e6e6',
          'text-secondary': '#a0a0a0',
          card: '#2a3038',
          border: '#3a424c',
        },
      },
      borderRadius: {
        card: '12px',
      },
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          '"PingFang SC"',
          '"Microsoft YaHei"',
          'sans-serif',
        ],
        mono: [
          '"JetBrains Mono"',
          'ui-monospace',
          '"SF Mono"',
          '"Fira Code"',
          'Menlo',
          'Consolas',
          'monospace',
        ],
      },
    },
  },
  plugins: [],
};
