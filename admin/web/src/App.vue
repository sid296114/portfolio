<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import LoginView from './views/LoginView.vue'
import SiteView from './views/SiteView.vue'
import ProjectsView from './views/ProjectsView.vue'
import PostsView from './views/PostsView.vue'

const route = ref(window.location.hash || '#/site')
const authed = ref(!!localStorage.getItem('portfolio_admin_token'))
const toast = ref('')

function onHashChange() {
  route.value = window.location.hash || '#/site'
}
function onUnauthorized() {
  authed.value = false
  route.value = '#/login'
  window.location.hash = '#/login'
}

onMounted(() => {
  window.addEventListener('hashchange', onHashChange)
  window.addEventListener('admin-unauthorized', onUnauthorized)
})
onUnmounted(() => {
  window.removeEventListener('hashchange', onHashChange)
  window.removeEventListener('admin-unauthorized', onUnauthorized)
})

function logout() {
  localStorage.removeItem('portfolio_admin_token')
  authed.value = false
  window.location.hash = '#/login'
}

const currentView = computed(() => {
  const r = route.value.replace('#/', '')
  if (r === 'login') return 'login'
  if (r === 'projects') return 'projects'
  if (r === 'posts') return 'posts'
  return 'site'
})
</script>

<template>
  <div v-if="!authed" class="min-h-screen">
    <LoginView @ok="authed = true; window.location.hash = '#/site'" />
  </div>

  <div v-else class="min-h-screen">
    <!-- 顶栏 -->
    <header class="sticky top-0 z-10 bg-[#446688] text-white shadow-sm">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div class="flex items-center gap-2">
          <span class="text-lg font-semibold">Portfolio 内容管理</span>
          <span class="rounded-full bg-white/15 px-2 py-0.5 text-xs">本地后台</span>
        </div>
        <button class="rounded-lg px-3 py-1.5 text-sm hover:bg-white/15" @click="logout">
          退出登录
        </button>
      </div>
    </header>

    <!-- 导航 -->
    <nav class="mx-auto flex max-w-6xl gap-2 px-4 pt-4">
      <a
        href="#/site" :class="currentView === 'site' ? 'bg-[#446688] text-white shadow-sm' : 'bg-white text-[#446688] hover:bg-[#e8eef5]'"
        class="rounded-lg px-4 py-2 text-sm font-medium transition"
      >站点配置</a>
      <a
        href="#/projects" :class="currentView === 'projects' ? 'bg-[#446688] text-white shadow-sm' : 'bg-white text-[#446688] hover:bg-[#e8eef5]'"
        class="rounded-lg px-4 py-2 text-sm font-medium transition"
      >项目</a>
      <a
        href="#/posts" :class="currentView === 'posts' ? 'bg-[#446688] text-white shadow-sm' : 'bg-white text-[#446688] hover:bg-[#e8eef5]'"
        class="rounded-lg px-4 py-2 text-sm font-medium transition"
      >博客</a>
      <a
        href="/" target="_blank" class="ml-auto rounded-lg bg-white/80 px-4 py-2 text-sm font-medium text-[#446688] hover:bg-white"
      >查看站点 ↗</a>
    </nav>

    <!-- 内容 -->
    <main class="mx-auto max-w-6xl px-4 pb-16 pt-4">
      <SiteView v-if="currentView === 'site'" />
      <ProjectsView v-else-if="currentView === 'projects'" />
      <PostsView v-else-if="currentView === 'posts'" />
    </main>

    <!-- 提示条 -->
    <div v-if="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 rounded-lg bg-[#333] px-4 py-2 text-sm text-white shadow-lg">
      {{ toast }}
    </div>
  </div>
</template>
