# Portfolio 内容管理后台

给 `portfolio/` 个人作品集网站配套的本地内容管理系统：改个人信息、增删改项目、写博客，保存后直接写入网站源文件（`src/data/site.ts`、`src/data/projects.ts`、`src/content/blog/*.md`），Astro 开发服务热更新即时生效。

## 目录结构

```
admin/
├── server/          # FastAPI 后端（读写源数据文件）
│   ├── app/
│   │   ├── main.py        # API 路由 + 鉴权 + CORS
│   │   └── data_store.py  # 读写 site.ts / projects.ts / blog/*.md
│   ├── requirements.txt
│   └── run.ps1            # 后端启动脚本（自动建 venv、装依赖）
└── web/             # Vue3 + Vite + Tailwind 管理界面
    ├── src/views/  # SiteView / ProjectsView / PostsView / LoginView
    └── ...
```

## 启动

### 一键启动（推荐）

```powershell
powershell -ExecutionPolicy Bypass -File admin\start.ps1
```

### 分开启动

后端（8002 端口，带热重载）：

```powershell
powershell -ExecutionPolicy Bypass -File admin\server\run.ps1
```

前端（5175 端口）：

```powershell
cd admin\web
npm install      # 首次
npm run dev
```

## 使用

1. 打开 `http://localhost:5175`，输入口令（默认 `admin123`，可用环境变量 `ADMIN_TOKEN` 修改）
2. 三个标签页：
   - **站点配置**：姓名、角色、Slogan、关于我、邮箱、技能组（增删技能/组）
   - **项目**：项目卡片增删改（名称/简介/缩略图/标签/详情）
   - **博客**：文章增删改（标题/日期/标签/摘要/Markdown 正文）
3. 保存后改动直接写入 `portfolio/src/` 下的源文件

## 生效方式

- **本地开发**：`pnpm dev`（portfolio 根目录）开着时，保存后页面自动热更新
- **上线**：保存后运行 `pnpm build` 重新构建，再部署（Netlify / GitHub Pages 均可）
- 管理后台里提供了 `POST /api/rebuild` 接口（可在站点配置页触发 `pnpm build`）

## API 一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/login` | 口令登录 |
| GET/PUT | `/api/site` | 站点配置读写 |
| GET/POST | `/api/projects` | 项目列表 / 新增 |
| PUT/DELETE | `/api/projects/{id}` | 更新 / 删除项目 |
| GET/POST | `/api/posts` | 博客列表 / 新增 |
| PUT/DELETE | `/api/posts/{slug}` | 更新 / 删除文章 |
| POST | `/api/rebuild` | 执行 pnpm build 重新构建站点 |
