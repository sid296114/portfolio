<script setup>
import { ref } from 'vue'
import { api, setToken } from '../api'

const emit = defineEmits(['ok'])
const token = ref('')
const error = ref('')
const loading = ref(false)

async function login() {
  if (!token.value.trim()) {
    error.value = '请输入口令'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await api.login(token.value.trim())
    setToken(token.value.trim())
    emit('ok')
  } catch (e) {
    error.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="relative flex min-h-screen items-center justify-center overflow-hidden px-4">
    <!-- 星夜背景（梵高《星月夜》，公有领域画作） -->
    <img
      src="https://aka.doubaocdn.com/s/Im8VOBJV30"
      alt=""
      aria-hidden="true"
      class="absolute inset-0 h-full w-full object-cover"
    />
    <div class="absolute inset-0 bg-[#0a1830]/70"></div>

    <div class="relative w-full max-w-sm rounded-2xl border border-white/15 bg-[#0e2140]/80 p-8 shadow-2xl backdrop-blur-md">
      <div class="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-[#2b5397] to-[#12305e] text-2xl font-bold text-white ring-2 ring-white/30">
        李
      </div>
      <h1 class="text-xl font-semibold text-white">Portfolio 内容管理后台</h1>
      <p class="mt-2 text-sm text-white/70">管理个人简介、项目与博客内容</p>

      <form class="mt-6 space-y-3" @submit.prevent="login">
        <input
          v-model="token"
          type="password"
          placeholder="输入管理口令"
          class="w-full rounded-lg border border-white/25 bg-white/10 px-3 py-2 text-sm text-white placeholder-white/50 outline-none backdrop-blur focus:border-[#9fd8e8]"
        />
        <p v-if="error" class="text-sm text-red-300">{{ error }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full rounded-lg bg-[#f0d488] py-2 text-sm font-semibold text-[#12305e] transition hover:bg-[#f6e3a0] disabled:opacity-60"
        >
          {{ loading ? '验证中…' : '进入后台' }}
        </button>
      </form>

      <p class="mt-4 text-center text-xs text-white/50">默认口令 admin123（后端可用环境变量 ADMIN_TOKEN 修改）</p>
    </div>
  </div>
</template>
