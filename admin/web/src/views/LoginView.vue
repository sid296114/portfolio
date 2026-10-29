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
  <div class="flex min-h-screen items-center justify-center px-4">
    <div class="w-full max-w-sm rounded-xl bg-white p-8 shadow-md border border-[#e5e2da]">
      <h1 class="text-center text-xl font-semibold text-[#446688]">Portfolio 内容管理后台</h1>
      <p class="mt-2 text-center text-sm text-[#666]">管理个人简介、项目与博客内容</p>

      <form class="mt-6 space-y-3" @submit.prevent="login">
        <input
          v-model="token"
          type="password"
          placeholder="输入管理口令"
          class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]"
        />
        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full rounded-lg bg-[#446688] py-2 text-sm font-medium text-white hover:bg-[#3a5878] disabled:opacity-60"
        >
          {{ loading ? '验证中…' : '进入后台' }}
        </button>
      </form>

      <p class="mt-4 text-center text-xs text-[#999]">默认口令 admin123（后端可用环境变量 ADMIN_TOKEN 修改）</p>
    </div>
  </div>
</template>
