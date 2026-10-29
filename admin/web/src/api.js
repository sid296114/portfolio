// 与后端 FastAPI 通信的封装
const TOKEN_KEY = 'portfolio_admin_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}
export function setToken(t) {
  localStorage.setItem(TOKEN_KEY, t)
}
export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers['x-admin-token'] = token
  const res = await fetch('/api' + path, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  if (res.status === 401) {
    clearToken()
    window.dispatchEvent(new CustomEvent('admin-unauthorized'))
    throw new Error('登录已失效，请重新输入口令')
  }
  let data = null
  try {
    data = await res.json()
  } catch {
    data = null
  }
  if (!res.ok) throw new Error((data && data.detail) || `请求失败（${res.status}）`)
  return data
}

export const api = {
  login: (token) => request('POST', '/login', { token }),
  getSite: () => request('GET', '/site'),
  saveSite: (site) => request('PUT', '/site', site),
  getProjects: () => request('GET', '/projects'),
  createProject: (p) => request('POST', '/projects', p),
  updateProject: (id, p) => request('PUT', '/projects/' + id, p),
  deleteProject: (id) => request('DELETE', '/projects/' + id),
  getPosts: () => request('GET', '/posts'),
  createPost: (p) => request('POST', '/posts', p),
  updatePost: (slug, p) => request('PUT', '/posts/' + slug, p),
  deletePost: (slug) => request('DELETE', '/posts/' + slug),
  rebuild: () => request('POST', '/rebuild'),
}
