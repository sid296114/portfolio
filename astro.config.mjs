import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// Astro 配置：集成 Tailwind，博客代码块用 Shiki 明暗双主题高亮
export default defineConfig({
  site: 'https://example.com',
  integrations: [
    tailwind({
      // 不在基础样式中注入 Tailwind（由 src/styles/global.css 手动引入）
      applyBaseStyles: false,
    }),
  ],
  markdown: {
    shikiConfig: {
      // 明暗两套高亮主题，自动跟随 <html> 的 dark class 切换
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
      wrap: true,
    },
  },
});
