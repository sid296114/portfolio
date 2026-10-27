# AGENTS.md

> 本文件给 AI 编程助手（Cursor / Claude Code 等）和新加入的开发者看，快速了解项目是什么、怎么跑、有什么规矩。

---

## 1. 项目是什么

个人技术作品集网站，展示 **物联网 + AI 交叉方向** 的项目和技术博客。

- **定位**：面向求职面试官、研究生导师、同方向技术爱好者的个人主页
- **核心模块**：个人介绍、技能展示、项目展示、技术博客
- **设计风格**：简约克制、有质感，拒绝花哨特效，支持明暗双主题
- **产物形态**：纯静态站点，构建后可部署到任意静态托管（GitHub Pages / Vercel）

详细产品需求见 `PRD.md`，技术选型见 `TECH_DESIGN.md`。

---

## 2. 怎么跑起来

### 环境要求

- Node.js 18.x 或 20.x LTS
- 包管理器：**pnpm**（必须用 pnpm，不要用 npm / yarn）

### 常用命令

```bash
# 安装依赖
pnpm install

# 本地开发（热更新，默认 http://localhost:4321）
pnpm dev

# 构建生产版本（输出到 dist/ 目录）
pnpm build

# 本地预览构建产物
pnpm preview
```

### 注意事项

- 所有依赖安装、脚本运行一律用 `pnpm`，不要出现 `npm install`、`yarn add` 这类命令
- 不要在项目里生成 `package-lock.json` 或 `yarn.lock`

---

## 3. 技术栈速查表

| 类别 | ✅ 必须用这个 | ❌ 不许用这个 |
|-|-|-|
| 框架 | Astro 4.x | React / Vue / Next.js / Nuxt |
| 样式 | Tailwind CSS | Sass / Less / 手写独立 CSS 文件 |
| 博客正文 | Markdown 文件（`src/content/blog/`） | 在 JS / TS 里拼 HTML 字符串 |
| 代码高亮 | Shiki（Astro 内置） | 额外引入 highlight.js / Prism |
| 主题切换 | `dark` class + localStorage | CSS 变量做主题切换 |
| 包管理 | pnpm | npm / yarn |
| 脚本语言 | TypeScript（轻量使用） | 纯 JS / 重度类型体操 |
| 图标 | 内联 SVG | 大型图标库（如 Font Awesome 全量引入） |

---

## 4. 目录结构

```
portfolio/
├── astro.config.mjs          # Astro 配置
├── tailwind.config.mjs       # Tailwind 配置（色板、darkMode）
├── public/                   # 静态资源（原样拷贝到 dist）
│   └── assets/projects/     # 项目缩略图
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro  # 全局布局（head、导航、页脚、防闪烁脚本）
│   ├── components/          # UI 组件（每个区块一个文件）
│   ├── data/                # 项目数据、站点配置
│   ├── pages/              # 页面入口
│   │   ├── index.astro     # 首页
│   │   └── blog/           # 博客列表 + 详情
│   └── content/
│       └── blog/           # 博客 Markdown 文章（每篇一个 .md）
└── dist/                    # 构建产物（不要手动改）
```

**最常改的三个地方：**
- 加博客 → `src/content/blog/`
- 加项目 → `src/data/projects.ts`
- 改 UI → `src/components/`

---

## 5. 硬性约定

### 5.1 样式约定

- 一律用 Tailwind class，**不许写内联 style**，不许新建 `.css` 文件（`src/styles/global.css` 除外）
- 颜色用 `tailwind.config.mjs` 里定义好的色板，**不许自己随便选十六进制颜色**
- 卡片圆角统一 `12px`，阴影用低透明度柔和阴影，不要厚重投影
- 明暗主题的样式用 `dark:` 前缀写，不要用 JS 切换样式表

### 5.2 动效约定

**✅ 允许的动效：**
- 滚动进入视口时淡入（300~500ms）
- 卡片 hover 时 Y 轴轻微上移 + 阴影柔和放大
- 主题切换平滑过渡

**❌ 禁止的动效：**
- 粒子背景、流光边框、弹跳动画、闪烁文字
- 自动播放的背景视频 / GIF
- 任何"炫技"类特效

**必须遵守：**
- 所有动效要尊重 `prefers-reduced-motion`，用户开启"减少动态效果"时关闭滚动渐显和 hover 上浮

### 5.3 代码风格约定

- **注释用中文**
- **组件文件名用英文 PascalCase**，比如 `ProjectCard.astro`、`BlogDetail.astro`
- 数据文件、配置文件用英文小驼峰或全小写，比如 `projects.ts`、`site.ts`
- 组件结构清晰，每个组件职责单一，不要一个文件塞太多东西

### 5.4 数据约定

- **新增博客** = 在 `src/content/blog/` 丢一个 `.md` 文件，frontmatter 字段必须齐全（title、date、tags、summary）
- **新增项目** = 在 `src/data/projects.ts` 数组里追加一条，字段和现有条目保持一致
- **不许把数据硬编码在组件里**，所有项目、博客、站点配置都从 data 或 content 目录读

### 5.5 性能约定

- 页面默认输出零 JS HTML，只有弹窗交互和滚动渐显可以写少量客户端脚本
- 图片必须加 `loading="lazy"`，缩略图统一比例
- 首屏 JS 总量不许超过 50KB
- 不引入大型第三方库（比如完整的 Lodash、完整的 Moment）

### 5.6 其他硬性要求

- 邮箱地址做混淆处理（JS 拼接或 `[at]` 形式），防止被爬虫抓取
- 每页要有独立的 `<title>`、`meta description`、Open Graph 标签
- 图片必须有 `alt` 属性

---

## 6. 常见任务操作指南

### 加一篇博客

1. 在 `src/content/blog/` 新建文件 `post-xxx.md`（比如 `post-003.md`）
2. 开头写 frontmatter：

```markdown
---
title: "文章标题"
date: "2026-10-27"
tags: ["STM32", "踩坑"]
summary: "列表页显示的摘要，一两句话"
---

正文写 Markdown，代码块用 \`\`\`js 包裹
```

3. 保存即可，博客列表页和首页预览会自动出现

### 加一个项目

1. 缩略图放到 `public/assets/projects/` 目录
2. 编辑 `src/data/projects.ts`，在数组末尾追加一条：

```ts
{
  id: "proj-002",
  name: "项目名称",
  description: "简短描述",
  thumbnail: "/assets/projects/proj-002.png",
  tags: ["标签1", "标签2"],
  detail: "详情文字（弹窗展示）",
}
```

### 改导航栏

- 编辑 `src/components/Navbar.astro`

### 改主色调 / 配色

- 编辑 `tailwind.config.mjs` 里的 `theme.extend.colors`，所有页面自动生效

### 改博客详情页的代码高亮主题

- 编辑 `astro.config.mjs` 里的 Shiki 配置

---

## 7. 提交规范（建议）

commit message 用简单的前缀格式，方便回溯：

| 前缀 | 用途 | 例子 |
|-|-|-|
| `feat:` | 新功能 / 新内容 | `feat: 新增一篇 STM32 踩坑博客` |
| `fix:` | 修 bug | `fix: 修复移动端导航菜单错位` |
| `style:` | 样式调整，不改逻辑 | `style: 调整卡片圆角和阴影` |
| `docs:` | 文档更新 | `docs: 更新 PRD 到 V1.1` |
| `chore:` | 构建、依赖、配置 | `chore: 升级 Astro 到 4.x` |
