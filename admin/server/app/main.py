# -*- coding: utf-8 -*-
"""
portfolio 内容管理后台 - FastAPI 后端
启动：uvicorn app.main:app --reload --port 8002
口令：环境变量 ADMIN_TOKEN，默认 admin123（建议首次修改）
"""
import os
from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import data_store

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin123")

app = FastAPI(title="Portfolio Admin API", version="1.0.0")

# 管理前端 dev 服务器跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
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


@app.post("/api/login")
def login(body: dict):
    if body.get("token") == ADMIN_TOKEN:
        return {"ok": True}
    raise HTTPException(status_code=401, detail="口令错误")


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
        return data_store.update_site(site.model_dump())
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
        return project
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
                return payload
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
        return {"ok": True}
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
        return data_store.create_post(post.model_dump())
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"新增博客失败: {e}") from e


@app.put("/api/posts/{slug}", dependencies=[Depends(require_token)])
def update_post(slug: str, post: PostModel):
    try:
        return data_store.update_post(slug, post.model_dump())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"文章不存在: {slug}")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"更新博客失败: {e}") from e


@app.delete("/api/posts/{slug}", dependencies=[Depends(require_token)])
def delete_post(slug: str):
    try:
        data_store.delete_post(slug)
        return {"ok": True}
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"删除博客失败: {e}") from e


# ---------------------------------------------------------------- 构建
@app.post("/api/rebuild", dependencies=[Depends(require_token)])
def rebuild():
    return data_store.rebuild_site()
