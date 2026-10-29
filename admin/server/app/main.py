# -*- coding: utf-8 -*-
"""
portfolio 内容管理后台 - FastAPI 后端
启动：uvicorn app.main:app --reload --port 8002（云端可设环境变量 PORT）
口令：环境变量 ADMIN_TOKEN，默认 admin123（建议首次修改）
"""
import os
from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import data_store, git_sync

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin123")

app = FastAPI(title="Portfolio Admin API", version="1.1.0")

# 云端部署时管理前端与 API 同源（由本服务托管静态文件），本地保留 dev 端口；
# 令牌鉴权已保护所有写接口，CORS 放开以兼容任意访问域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------- 模型
class Skill(BaseModel):
    name: str = ""
    level: str = ""


class SkillGroup(BaseModel):
    title: str
    icon: str = "chip"
    skills: List[Skill] = Field(default_factory=list)


class SiteModel(BaseModel):
    name: str = ""
    role: str = ""
    slogan: str = ""
    lead: str = ""
    about: str = ""
    email: str = ""
    emailObfuscated: str = ""
    skillGroups: List[SkillGroup] = Field(default_factory=list)


class ProjectModel(BaseModel):
    id: Optional[str] = None
    name: str
    description: str = ""
    thumbnail: str = ""
    tags: List[str] = Field(default_factory=list)
    detail: str = ""


class PostModel(BaseModel):
    slug: Optional[str] = None
    title: str = ""
    date: str = ""
    tags: List[str] = Field(default_factory=list)
    summary: str = ""
    content: str = ""


# ---------------------------------------------------------------- 鉴权
def require_token(x_admin_token: str = Header(default="")) -> None:
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="口令错误，请重新登录")


def _with_sync(payload: dict, reason: str) -> dict:
    """保存/删除成功后同步 GitHub，把同步结果附到响应里。"""
    ok, msg = git_sync.sync_now(reason)
    payload["sync"] = {"ok": ok, "message": msg}
    return payload


@app.post("/api/login")
def login(body: dict):
    if body.get("token") == ADMIN_TOKEN:
        return {"ok": True}
    raise HTTPException(status_code=401, detail="口令错误")


@app.get("/api/sync", dependencies=[Depends(require_token)])
def manual_sync():
    """手动触发一次 git 同步。"""
    ok, msg = git_sync.sync_now("manual sync via admin")
    return {"sync": {"ok": ok, "message": msg}}


# ---------------------------------------------------------------- 站点配置
@app.get("/api/site", dependencies=[Depends(require_token)])
def get_site():
    try:
        return data_store.read_site()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"读取站点配置失败: {e}") from e


@app.put("/api/site", dependencies=[Depends(require_token)])
def put_site(site: SiteModel):
    try:
        payload = data_store.update_site(site.model_dump())
        return _with_sync(payload, "site config updated via admin")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"保存站点配置失败: {e}") from e


# ---------------------------------------------------------------- 项目
@app.get("/api/projects", dependencies=[Depends(require_token)])
def get_projects():
    try:
        return data_store.read_projects()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"读取项目失败: {e}") from e


@app.post("/api/projects", dependencies=[Depends(require_token)])
def create_project(project: ProjectModel):
    try:
        projects = data_store.read_projects()
        project.id = project.id or data_store.next_project_id(projects)
        if any(p["id"] == project.id for p in projects):
            raise HTTPException(status_code=400, detail=f"项目 ID 已存在: {project.id}")
        projects.append(project.model_dump())
        data_store.update_projects(projects)
        return _with_sync(project.model_dump(), "project created via admin")
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"新增项目失败: {e}") from e


@app.put("/api/projects/{project_id}", dependencies=[Depends(require_token)])
def update_project(project_id: str, project: ProjectModel):
    try:
        projects = data_store.read_projects()
        for i, p in enumerate(projects):
            if p["id"] == project_id:
                payload = project.model_dump()
                payload["id"] = project_id
                projects[i] = payload
                data_store.update_projects(projects)
                return _with_sync(payload, f"project updated via admin ({project_id})")
        raise HTTPException(status_code=404, detail=f"项目不存在: {project_id}")
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"更新项目失败: {e}") from e


@app.delete("/api/projects/{project_id}", dependencies=[Depends(require_token)])
def delete_project(project_id: str):
    try:
        projects = data_store.read_projects()
        new_projects = [p for p in projects if p["id"] != project_id]
        if len(new_projects) == len(projects):
            raise HTTPException(status_code=404, detail=f"项目不存在: {project_id}")
        data_store.update_projects(new_projects)
        return _with_sync({"ok": True}, f"project deleted via admin ({project_id})")
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"删除项目失败: {e}") from e


# ---------------------------------------------------------------- 博客
@app.get("/api/posts", dependencies=[Depends(require_token)])
def get_posts():
    try:
        return data_store.list_posts()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"读取博客失败: {e}") from e


@app.post("/api/posts", dependencies=[Depends(require_token)])
def create_post(post: PostModel):
    try:
        payload = data_store.create_post(post.model_dump())
        return _with_sync(payload, "post created via admin")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"新增博客失败: {e}") from e


@app.put("/api/posts/{slug}", dependencies=[Depends(require_token)])
def update_post(slug: str, post: PostModel):
    try:
        payload = data_store.update_post(slug, post.model_dump())
        return _with_sync(payload, f"post updated via admin ({slug})")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"文章不存在: {slug}")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"更新博客失败: {e}") from e


@app.delete("/api/posts/{slug}", dependencies=[Depends(require_token)])
def delete_post(slug: str):
    try:
        data_store.delete_post(slug)
        return _with_sync({"ok": True}, f"post deleted via admin ({slug})")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"删除博客失败: {e}") from e


# ---------------------------------------------------------------- 构建
@app.post("/api/rebuild", dependencies=[Depends(require_token)])
def rebuild():
    return data_store.rebuild_site()


# ---------------------------------------------------------------- 托管管理前端（云端单服务部署）
# 若 admin/web/dist 已构建（npm run build 产物），则由本服务直接托管，
# 云端访问同一个地址即可用后台，无需单独部署前端。
_DIST_DIR = Path(__file__).resolve().parents[2] / "web" / "dist"
if _DIST_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(_DIST_DIR), html=True), name="admin-web")

