# 管理后台云端部署指南

把管理后台部署到云上之后，可以做到：**手机/电脑打开网页 → 修改内容 → 保存 → 自动推送 GitHub → Netlify 自动重新构建 → 网站线上生效**，全程不需要本地电脑。

## 部署前提（必做）

1. **Netlify 必须连接 GitHub 仓库**（自动构建模式）：
   - Netlify 后台 → Add new site → Import an existing project → 选 `sid296114/portfolio` 仓库
   - Build command: `pnpm build`，Publish directory: `dist`
   - 这样每次 GitHub 收到新提交，Netlify 自动重新构建部署，无需手动上传
2. 如果之前是拖 dist 手动部署的，改成上面这种方式（或告诉我帮你处理）。

## 架构原理

```
云端后台（本 admin 服务）
  └─ 保存/删除 → 直接改写仓库源文件 (src/data/*, src/content/blog/*)
  └─ 自动 git commit + push → GitHub 仓库
        └─ Netlify 监听 → 自动重新构建 → 线上站点更新
```

- 后台服务里的文件只是「工作副本」，**内容真正的归宿是 GitHub 仓库**，所以云平台重启/重部署不会丢内容（会从仓库拉回最新）。
- 本地 `git push` 时用的同一套 git 凭据在云端也可用（详见下面「GitHub 凭据」）。

## 方案一：Render 免费托管（无需自购服务器，推荐）

[render.com](https://render.com) 免费档即可运行本后台（个人使用足够；免费实例 15 分钟无访问会休眠，首次打开稍慢，自动唤醒）。

### 步骤

1. 登录 Render → **New → Web Service** → Connect GitHub 仓库 `sid296114/portfolio`
2. **Root Directory**：填 `admin/server`
3. **Build Command**：
   ```bash
   pip install -r requirements.txt
   cd ../web && npm install && npm run build && cd ../server
   ```
4. **Start Command**：
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   （后端已支持 `PORT` 环境变量约定，Render 自动注入）
5. **Environment Variables**：
   - `ADMIN_TOKEN`：改成你自己的后台口令（强密码）
   - `AUTO_GIT_SYNC`：`1`（默认开启，可省略）
   - `GIT_TOKEN`（可选，见下）
6. 部署完成后，访问 `https://你的服务名.onrender.com/` 即进入管理后台。

### GitHub 凭据（云端 push 需要）

Render 从 GitHub clone 仓库时默认用只读 deploy key，**push 需要额外配置**。二选一：

- **方式 A（简单）**：把仓库 remote 带上写权限 token：
  - GitHub → Settings → Developer settings → Personal access tokens → 生成一个 **Fine-grained token**（仓库 `sid296114/portfolio` 的 **Contents: Read and write** 权限）
  - 后台服务器上执行：
    ```bash
    git remote set-url origin https://x-access-token:你的token@github.com/sid296114/portfolio.git
    ```
    （Render 在 Shell 面板执行；token 只保存在该实例）
- **方式 B（更安全，推荐）**：部署前给仓库加 SSH 部署密钥，服务器用 SSH 方式 push。详见 GitHub 文档「Adding a new SSH key to your GitHub account」。

> 没有配置 token 时，后台保存仍会成功、本地文件会更新，但 push 会失败并显示「git push 失败」提示——配置好凭据即可自动恢复。

## 方案二：自购云服务器（阿里云/腾讯云轻量等）

以 Ubuntu 22.04 为例：

```bash
# 1. 安装基础环境
sudo apt update && sudo apt install -y git python3 python3-venv nodejs npm

# 2. 克隆仓库（用带权限的方式，便于自动 push）
git clone https://x-access-token:你的token@github.com/sid296114/portfolio.git
cd portfolio

# 3. 启动后台（一键脚本，自动建 venv 装依赖）
cd admin/server
sudo chmod +x run.ps1   # 本仓库为 Windows 脚本，Linux 下直接执行：
bash -c "python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8002"

# 4.（可选）用 systemd 保活 + 设置 ADMIN_TOKEN / 端口
```

云服务器安全组放行端口后，访问 `http://服务器IP:8002/` 即进入后台。建议再配 Nginx 反代 + HTTPS 域名（可选）。

## 验证清单（部署后）

1. 浏览器打开云端地址 → 输入口令进入后台
2. 改一条内容 → 保存 → 看到「已保存，改动已自动同步到 GitHub，线上稍后自动更新 ✓」
3. 打开 GitHub 仓库 → 看到新的自动提交（`content update via admin`）
4. 等 Netlify 构建完成（几分钟）→ 打开你的 Netlify 站点 → 改动已上线

## 常用设置

| 环境变量 | 说明 | 默认 |
| --- | --- | --- |
| `ADMIN_TOKEN` | 后台登录口令 | `admin123`（务必修改） |
| `AUTO_GIT_SYNC` | 保存后自动 commit+push | `1` 开启 |
| `PORT` | 服务端口（云平台自动注入） | `8002` |
| `GIT_TOKEN` | GitHub 写权限 token（配 remote 用） | 无 |

## 本地开发不受影响

- 本地照常用 `admin\start.ps1` 启动，`AUTO_GIT_SYNC=0` 可关闭自动推送。
- 云端后台与本地后台共用同一套源文件结构，改动都汇入 GitHub，互不冲突（注意别同时改同一文件，避免 push 冲突，push 失败时会提示，重新保存即可）。
