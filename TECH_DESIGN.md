# 个人作品集网站 技术设计文档

文档版本：V1.0
对应 PRD：`PRD.md` V1.1
编写日期：2026-10-27

---

## 1. 文档目的

记录本项目的技术选型结论、架构设计与实现方案，作为后续开发执行的依据。本文档基于 `PRD.md` 的产品需求展开，只回答"用什么技术、怎么搭"的问题，不重复产品层面的功能定义。

---

## 2. 技术选型结论

### 2.1 最终选型

**Astro（静态站点生成器）+ Tailwind CSS + TypeScript（轻量）**

### 2.2 选型决策过程

在 PRD 原有方案（纯 HTML + Tailwind CLI + 原生 JS）基础上，对比了三条路线：

| 方案 | 描述 | 优势 | 劣势 |
|-|-|-|-|
| 方案一 | 纯静态多页 HTML + Tailwind CLI 编译 | 零框架、零构建复杂度、双击即开 | 公共组件需复制粘贴、博客正文用 HTML 字符串难维护 |
| **方案二（选定）** | **Astro 静态站点生成器** | **组件化复用、Markdown 写博客、默认零 JS 运行时、热更新** | **需 Node 环境、多一步构建** |
| 方案三 | Vite + 原生 JS | 热更新、模块化 | 两头不靠，无组件化收益 |

### 2.3 为什么选 Astro

1. **性能目标完全兼容**：Astro 构建产物是纯静态 HTML，默认不打包前端框架运行时，天然满足 PRD"首屏 JS < 50KB、无前端框架运行时"的量化要求
2. **组件化解决公共部分复用**：导航栏、页脚做成 `.astro` 组件，三个页面引用同一组件，改一处全站生效，不再需要复制粘贴
3. **博客用 Markdown 写**：文章正文直接写 `.md` 文件，不用在 JS 对象里拼 HTML 字符串，写作体验和后续维护都好得多
4. **Tailwind 原生集成**：官方 `@astrojs/tailwind` 集成，开发时热更新，不用自己配 CLI watch
5. **学习成本可控**：`.astro` 文件语法接近 HTML + 组件，对前端基础一般的开发者友好，比 React/Vue 简单

### 2.4 与 PRD 的差异说明

PRD 第 4 章原定"纯静态多页（HTML + JS）"，本设计调整为 Astro 实现，以下方面保持一致：

- 三个页面的路由结构不变（首页、博客列表、博客详情）
- Tailwind CSS 作为样式方案不变
- 明暗主题机制不变（`dark` class 策略 + localStorage + 防 FOUC）
- 代码高亮方案不变（highlight.js 或 Astro 内置 Shiki）
- 数据驱动理念不变（博客和项目数据与页面结构分离）

---

## 3. 技术栈明细

| 类别 | 选型 | 说明 |
|-|-|-|
| 静态站点生成 | Astro 4.x | 构建纯静态 HTML，默认零 JS |
| 样式 | Tailwind CSS | 通过 `@astrojs/tailwind` 集成，`darkMode: 'class'` |
| 脚本语言 | TypeScript（轻量使用） | 数据文件和工具函数用 `.ts`，组件里少量类型标注 |
| 博客格式 | Markdown / MDX | 文章正文写 `.md`， frontmatter 存元信息 |
| 代码高亮 | Shiki（Astro 内置） | 替代 highlight.js，明暗双主题自动适配，效果更好 |
| 图标 | 内联 SVG | 不引入图标库，手工写 SVG 或用少量开源图标 |
| 部署 | GitHub Pages / Vercel | 构建产物为纯静态文件，任意静态托管均可 |
| 包管理 | pnpm | 轻量、快 |

---

## 4. 项目结构设计

```
portfolio/
├── astro.config.mjs          # Astro 配置（Tailwind 集成、站点地址等）
├── tailwind.config.mjs       # Tailwind 配置（darkMode、自定义色板）
├── package.json
├── tsconfig.json
├── public/                   # 静态资源（不经过构建处理）
│   ├── favicon.svg
│   └── assets/
│       └── projects/        # 项目缩略图
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro  # 全局布局：<head>、导航、页脚、主题防闪烁脚本
│   ├── components/
│   │   ├── Navbar.astro      # 顶部导航栏（固定、滚动毛玻璃效果）
│   │   ├── Footer.astro      # 页脚（联系方式、版权）
│   │   ├── ThemeToggle.astro # 明暗主题切换按钮
│   │   ├── Hero.astro        # 首屏区域
│   │   ├── About.astro       # 关于我
│   │   ├── Skills.astro      # 技能栈分组卡片
│   │   ├── ProjectCard.astro # 单个项目卡片
│   │   ├── Projects.astro    # 项目列表 + 弹窗详情
│   │   ├── BlogCard.astro    # 单个博客卡片
│   │   ├── BlogPreview.astro # 首页博客预览区
│   │   └── ProjectModal.astro# 项目详情弹窗
│   ├── data/
│   │   ├── projects.ts       # 项目数据（数组，与 projects.js 同结构）
│   │   └── site.ts           # 站点全局配置（姓名、邮箱、Slogan 等）
│   ├── pages/
│   │   ├── index.astro       # 首页（组装 Hero/About/Skills/Projects/BlogPreview）
│   │   ├── blog/
│   │   │   ├── index.astro   # 博客列表页（标签过滤）
│   │   │   └── [id].astro    # 博客详情页（按 id 动态路由）
│   └── styles/
│       └── global.css        # Tailwind 指令 + 少量全局样式
└── src/content/
    └── blog/                 # 博客 Markdown 文章目录
        ├── post-001.md
        └── post-002.md
```

### 4.1 目录设计要点

- **`src/layouts/`**：全局布局只写一次，所有页面继承它，导航和页脚自动出现
- **`src/components/`**：每个视觉区块独立成组件，职责单一，便于单独调整样式
- **`src/data/`**：项目数据和站点配置是 TS 文件，有类型提示，改起来安全
- **`src/content/blog/`**：每篇博客一个 `.md` 文件，Astro 的 Content Collections 自动做类型校验，新增文章只需丢一个 `.md` 进去

---

## 5. 核心模块实现方案

### 5.1 路由与页面

| 页面 | Astro 文件 | 路由路径 | 说明 |
|-|-|-|-|
| 首页 | `src/pages/index.astro` | `/` | 单页滚动，组装各组件 |
| 博客列表 | `src/pages/blog/index.astro` | `/blog` | 全部文章卡片 + 标签过滤 |
| 博客详情 | `src/pages/blog/[id].astro` | `/blog/post-001` | 从 Markdown 文件读取正文 |

相比 PRD 原方案的 `blog-detail.html?id=xxx`，Astro 的动态路由生成 `/blog/post-001` 这样的路径，**SEO 更友好**，也不需要自己解析 URL 参数。

### 5.2 主题切换

沿用 PRD 设计，机制不变：

- **策略**：Tailwind `darkMode: 'class'`，在 `<html>` 标签上加/移除 `dark` class
- **持久化**：`localStorage` 存用户选择
- **防 FOUC**：在 `BaseLayout.astro` 的 `<head>` 里写一段内联脚本，页面渲染前先读 localStorage，给 `<html>` 加好 class，避免刷新闪白/闪黑
- **切换按钮**：`ThemeToggle.astro` 组件，点击切换 class 并写入 localStorage

### 5.3 博客系统

**写法变化**：PRD 原来用 `posts.js` 存 HTML 字符串，现在改为 Markdown 文件：

```markdown
---
title: "STM32 串口调试踩坑记录"
date: "2026-10-27"
tags: ["STM32", "踩坑"]
summary: "列表页显示的摘要"
---

正文直接写 Markdown，代码块用 ```js 包裹，Shiki 自动高亮。
```

Astro Content Collections 会自动：
- 校验 frontmatter 字段是否齐全
- 按日期排序
- 生成每篇文章的静态页面
- 列表页读取所有文章的元信息生成卡片

### 5.4 项目展示与弹窗

- 项目数据放 `src/data/projects.ts`，结构和 PRD 的 `projects.js` 一致
- 项目卡片组件 `ProjectCard.astro` 接收单个项目数据渲染
- 弹窗用一个轻量的客户端交互实现（约 1KB JS），点击"查看详情"打开遮罩层展示 `detail` 内容
- 一期用弹窗，后续要加独立详情页时，只需在 `src/pages/projects/` 下加动态路由，数据已经是分离的，不用改结构

### 5.5 代码高亮

PRD 原定 highlight.js，这里**替换为 Astro 内置的 Shiki**，原因：
- 不需要额外引入库，零额外 JS
- 明暗主题自动跟随 `<html>` 的 `dark` class 切换
- 高亮效果比 highlight.js 更细腻（TextMate 语法）

配置上选两个主题：浅色用 `github-light`，深色用 `github-dark`，和整体灰蓝/炭灰的配色协调。

### 5.6 响应式与动效

- **响应式**：Tailwind 的断点系统（`sm`/`md`/`lg`）天然支持，PC 多列、平板少列、手机单列
- **滚动渐显**：用 `IntersectionObserver` 写一个极简的客户端脚本（约 2KB），给进入视口的元素加 `visible` class，配合 CSS transition 实现淡入
- **尊重 prefers-reduced-motion**：CSS 里加媒体查询，用户开启"减少动态效果"时关闭所有动画
- **卡片 hover**：纯 CSS 实现（`transform: translateY(-4px)` + 阴影变化），不需要 JS

---

## 6. 构建与运行

### 6.1 开发

```bash
pnpm install
pnpm dev        # 启动开发服务器，热更新，默认 4321 端口
```

### 6.2 构建

```bash
pnpm build      # 输出静态文件到 dist/ 目录
pnpm preview    # 本地预览构建产物
```

### 6.3 部署

`dist/` 目录是纯静态文件，可部署到：
- **GitHub Pages**：搭配 GitHub Actions 自动构建部署
- **Vercel / Netlify**：连仓库后自动识别 Astro 项目，零配置
- **本地服务器 / 任意静态托管**：直接把 `dist/` 扔上去

---

## 7. 性能目标与实现路径

| PRD 要求 | 实现方式 |
|-|-|
| 无前端框架运行时 | Astro 默认输出零 JS 的 HTML，只有弹窗和滚动渐显各约 1-2KB 客户端脚本 |
| 首屏 JS < 50KB | 上述两个脚本加起来 < 5KB，远低于目标 |
| 无多余网络请求 | 所有静态资源本地托管，字体用系统字体栈或本地引入 |
| 图片压缩 + 懒加载 | Astro 内置 `<Image>` 组件自动压缩，原生 `loading="lazy"` |
| SEO | 每页独立 title、meta description、OG 标签，Astro 的 `<head>` 管理统一处理 |

---

## 8. 后续扩展预留

1. **项目独立详情页**：数据已分离，加动态路由即可，不用重构
2. **博客标签过滤升级**：Content Collections 已自动收集所有标签，加搜索/筛选是增量工作
3. **接入评论系统**：可接入 Giscus（基于 GitHub Discussion），纯前端嵌入式，不影响主体架构
4. **RSS 订阅**：用 `@astrojs/rss` 集成，几行配置生成 RSS feed

---

## 9. 待确认事项

以下内容在开发前需要确认：

- [ ] Node.js 环境是否已安装（建议 18.x 或 20.x LTS）
- [ ] 包管理器偏好（默认 pnpm，也可用 npm / yarn）
- [ ] 部署平台选择（GitHub Pages / Vercel / 其他）
- [ ] 博客文章首批内容的数量和主题
- [ ] 项目缩略图的准备进度（统一比例建议 16:9 或 4:3）
