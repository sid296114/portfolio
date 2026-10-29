# -*- coding: utf-8 -*-
"""
数据读写层：管理 portfolio 的源数据文件。
- src/data/site.ts     站点配置（姓名、邮箱、Slogan、技能组）
- src/data/projects.ts 项目数据
- src/content/blog/*.md 博客文章

策略：保留文件头部的 interface / 注释原样，只重建数据区块，
保证格式与 Astro 构建兼容。
"""
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parents[3]          # portfolio/
DATA_DIR = BASE_DIR / "src" / "data"
BLOG_DIR = BASE_DIR / "src" / "content" / "blog"
SITE_FILE = DATA_DIR / "site.ts"
PROJECTS_FILE = DATA_DIR / "projects.ts"

# ---------------------------------------------------------------- site.ts

_SITE_BLOCK_RE = re.compile(
    r"(?ms)^export const site\s*=\s*\{.*?\}\s*as const;"
)
_SITE_TAIL_RE = re.compile(r"(?ms)^(export const site\s*=\s*\{)(.*?)(\}\s*as const;)")
# 顶层字段行（固定 2 空格缩进、行尾逗号）
_SIMPLE_FIELD_RE = re.compile(
    r"(?m)^  (name|role|slogan|lead|about|email|emailObfuscated):\s*'(.*?)',$"
)
# 整块剥离 skillGroups（含内部所有行，到顶层 2 空格 "  ]," 为止）
_SKILLGROUPS_SPAN_RE = re.compile(r"(?ms)^  skillGroups:\s*\[.*?\n  \],")
_GROUP_RE = re.compile(r"(?ms)\{\s*title:\s*'(.*?)',\s*icon:\s*'(.*?)',\s*skills:\s*\[(.*?)\]\s*,?\s*\}")
_SKILL_RE = re.compile(r"\{\s*name:\s*'(.*?)',\s*level:\s*'(.*?)'\s*\}")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def read_site() -> Dict[str, Any]:
    """解析 site.ts，返回站点配置字典。"""
    text = _read_text(SITE_FILE)
    block = _SITE_TAIL_RE.search(text)
    if not block:
        raise ValueError("site.ts 结构无法解析")
    body = block.group(2)

    site: Dict[str, Any] = {}
    # 先剥离 skillGroups 块，避免技能名里的 name/level 污染顶层字段
    body_core = _SKILLGROUPS_SPAN_RE.sub("", body)
    for m in _SIMPLE_FIELD_RE.finditer(body_core):
        site[m.group(1)] = m.group(2)

    groups: List[Dict[str, Any]] = []
    for gm in _GROUP_RE.finditer(body):
        skills = [
            {"name": sm.group(1), "level": sm.group(2)}
            for sm in _SKILL_RE.finditer(gm.group(3))
        ]
        groups.append({"title": gm.group(1), "icon": gm.group(2), "skills": skills})
    site["skillGroups"] = groups
    return site


def _render_site_block(site: Dict[str, Any]) -> str:
    """把站点配置渲染为 site.ts 中的 export const site = {...} 数据块。"""
    simple_fields = [
        "name", "role", "slogan", "lead", "about", "email", "emailObfuscated",
    ]
    lines = ["export const site = {"]
    for key in simple_fields:
        lines.append(f"  {key}: '{site.get(key, '')}',")
    lines.append("  skillGroups: [")
    for g in site.get("skillGroups", []):
        lines.append("    {")
        lines.append(f"      title: '{g.get('title', '')}',")
        lines.append(f"      icon: '{g.get('icon', 'chip')}',")
        lines.append("      skills: [")
        for s in g.get("skills", []):
            lines.append(f"        {{ name: '{s.get('name', '')}', level: '{s.get('level', '')}' }},")
        lines.append("      ],")
        lines.append("    },")
    lines.append("  ],")
    lines.append("} as const;")
    return "\n".join(lines)


def update_site(site: Dict[str, Any]) -> Dict[str, Any]:
    """整体重建 site 数据块，保留头部注释与 interface。"""
    text = _read_text(SITE_FILE)
    rendered = _render_site_block(site)
    if _SITE_BLOCK_RE.search(text):
        new_text = _SITE_BLOCK_RE.sub(rendered, text)
    else:
        # 兜底：追加到文件末尾
        new_text = text.rstrip("\n") + "\n\n" + rendered + "\n"
    _write_text(SITE_FILE, new_text)
    return read_site()


# ------------------------------------------------------------ projects.ts

_PROJECTS_RE = re.compile(
    r"(?ms)^(export const projects:\s*Project\[\]\s*=\s*)(\[.*?\])(\s*;)"
)


def _ts_value_to_json(value: str) -> str:
    """把 TS 字面量转成 JSON：单引号->双引号、去掉注释/尾逗号、合并跨行字段值。"""
    # 合并跨行字段值（如 detail:\n  '...' -> detail: '...'，保留冒号）
    value = re.sub(r"(?m)^(\s*\w+:)\s*\n\s*(')", r"\1 \2", value)
    value = re.sub(r"(?m)//.*?$", "", value)
    value = value.replace("'", '"')
    # TS 对象字面量的 key 不带引号，转为 JSON 时补上（仅行首 key）
    value = re.sub(r"(?m)(^\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)", r'\1"\2"\3', value)
    value = re.sub(r",\s*([}\]])", r"\1", value)
    return value


def read_projects() -> List[Dict[str, Any]]:
    text = _read_text(PROJECTS_FILE)
    m = _PROJECTS_RE.search(text)
    if not m:
        raise ValueError("projects.ts 结构无法解析")
    raw = _ts_value_to_json(m.group(2))
    return json.loads(raw)


def _render_projects_block(projects: List[Dict[str, Any]]) -> str:
    lines = ["export const projects: Project[] = ["]
    for p in projects:
        lines.append("  {")
        lines.append(f"    id: '{p.get('id', '')}',")
        lines.append(f"    name: '{p.get('name', '')}',")
        lines.append(f"    description: '{p.get('description', '')}',")
        lines.append(f"    thumbnail: '{p.get('thumbnail', '')}',")
        tags = ", ".join(f"'{t}'" for t in p.get("tags", []))
        lines.append(f"    tags: [{tags}],")
        lines.append(f"    detail: '{p.get('detail', '')}',")
        lines.append("  },")
    lines.append("];")
    return "\n".join(lines)


def update_projects(projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    text = _read_text(PROJECTS_FILE)
    rendered = _render_projects_block(projects)
    m = _PROJECTS_RE.search(text)
    if not m:
        raise ValueError("projects.ts 结构无法解析")
    new_text = text[: m.start(1)] + rendered + text[m.end(3):]
    _write_text(PROJECTS_FILE, new_text)
    return read_projects()


def next_project_id(projects: List[Dict[str, Any]]) -> str:
    nums = [int(p["id"].split("-")[-1]) for p in projects if re.match(r"proj-\d+", p.get("id", ""))]
    return f"proj-{max(nums, default=0) + 1:03d}"


# ------------------------------------------------------------ blog posts

def _parse_md(path: Path) -> Dict[str, Any]:
    text = _read_text(path)
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path.name} 缺少 frontmatter")
    meta: Dict[str, Any] = {"title": "", "date": "", "tags": [], "summary": ""}
    for line in m.group(1).splitlines():
        kv = re.match(r"^(\w+):\s*(.*)$", line)
        if not kv:
            continue
        key, val = kv.group(1), kv.group(2).strip()
        if key == "tags":
            try:
                meta[key] = json.loads(_ts_value_to_json(val))
            except json.JSONDecodeError:
                meta[key] = []
        else:
            meta[key] = val.strip("'\"")
    body = m.group(2).strip()
    return {
        "slug": path.stem,
        "title": meta.get("title", ""),
        "date": meta.get("date", ""),
        "tags": meta.get("tags", []),
        "summary": meta.get("summary", ""),
        "content": body,
    }


def list_posts() -> List[Dict[str, Any]]:
    posts = []
    for f in sorted(BLOG_DIR.glob("*.md")):
        posts.append(_parse_md(f))
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def get_post(slug: str) -> Optional[Dict[str, Any]]:
    f = BLOG_DIR / f"{slug}.md"
    return _parse_md(f) if f.exists() else None


def _render_md(post: Dict[str, Any]) -> str:
    tags = json.dumps(post.get("tags", []), ensure_ascii=False)
    lines = [
        "---",
        f'title: "{post.get("title", "")}"',
        f'date: "{post.get("date", "")}"',
        f"tags: {tags}",
        f'summary: "{post.get("summary", "")}"',
        "---",
        "",
        (post.get("content", "") or "").strip(),
        "",
    ]
    return "\n".join(lines)


def create_post(post: Dict[str, Any]) -> Dict[str, Any]:
    posts = list_posts()
    nums = [int(p["slug"].split("-")[-1]) for p in posts if re.match(r"post-\d+", p["slug"])]
    slug = f"post-{max(nums, default=0) + 1:03d}"
    post["slug"] = slug
    _write_text(BLOG_DIR / f"{slug}.md", _render_md(post))
    return get_post(slug)


def update_post(slug: str, post: Dict[str, Any]) -> Dict[str, Any]:
    f = BLOG_DIR / f"{slug}.md"
    if not f.exists():
        raise FileNotFoundError(slug)
    post["slug"] = slug
    _write_text(f, _render_md(post))
    return get_post(slug)


def delete_post(slug: str) -> None:
    """删除博客 md 文件。Windows 下文件可能被系统进程短暂占用，
    unlink 成功后文件会延迟消失，属正常现象。"""
    f = BLOG_DIR / f"{slug}.md"
    for _ in range(4):
        if not f.exists():
            return
        try:
            f.unlink()
            return
        except OSError:
            time.sleep(0.5)


# ---------------------------------------------------------------- rebuild

def rebuild_site() -> Dict[str, Any]:
    """在 portfolio 根目录执行 pnpm build（Astro 静态构建）。"""
    try:
        result = subprocess.run(
            ["pnpm", "build"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "ok": result.returncode == 0,
            "output": (result.stdout + result.stderr)[-2000:],
        }
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "output": str(e)}
