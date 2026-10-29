<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'

const posts = ref([])
const loading = ref(true)
const error = ref('')
const editing = ref(false)
const form = ref(emptyForm())
const tagsText = ref('')
const syncMsg = ref('')

function emptyForm() {
  return { slug: '', title: '', date: '', tags: [], summary: '', content: '' }
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    posts.value = await api.getPosts()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function openCreate() {
  const today = new Date().toISOString().slice(0, 10)
  form.value = emptyForm()
  form.value.date = today
  tagsText.value = ''
  editing.value = true
}
function openEdit(p) {
  form.value = { ...p }
  tagsText.value = (p.tags || []).join(', ')
  editing.value = true
}
async function save() {
  error.value = ''
  syncMsg.value = ''
  try {
    form.value.tags = tagsText.value.split(/[,，、\s]+/).filter(Boolean)
    let res
    if (form.value.slug) {
      res = await api.updatePost(form.value.slug, form.value)
    } else {
      res = await api.createPost(form.value)
    }
    editing.value = false
    if (res && res.sync && !res.sync.ok) {
      syncMsg.value = `已保存，但 GitHub 同步失败：${res.sync.message}`
    }
    await load()
  } catch (e) {
    error.value = e.message
  }
}
async function remove(p) {
  if (!confirm(`确定删除文章「${p.title}」？`)) return
  try {
    await api.deletePost(p.slug)
    await load()
  } catch (e) {
    error.value = e.message
  }
}
function fmtDate(d) {
  return d || '—'
}
onMounted(load)
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
      <button class="ml-auto rounded-lg bg-[#446688] px-4 py-2 text-sm font-medium text-white hover:bg-[#3a5878]" @click="openCreate">+ 写新文章</button>
    </div>

    <div v-if="loading" class="py-16 text-center text-sm text-[#666]">加载中…</div>

    <div v-else class="space-y-3">
      <div v-for="p in posts" :key="p.slug" class="rounded-xl border border-[#e5e2da] bg-white p-4 shadow-sm">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-sm font-semibold text-[#446688]">{{ p.title }}</span>
              <span class="rounded bg-[#f0ede5] px-1.5 py-0.5 text-xs text-[#666]">{{ p.slug }}</span>
            </div>
            <div class="mt-1 text-xs text-[#999]">发布于 {{ fmtDate(p.date) }}</div>
            <p class="mt-2 line-clamp-2 text-sm text-[#555]">{{ p.summary }}</p>
            <div class="mt-2 flex flex-wrap gap-1">
              <span v-for="t in p.tags" :key="t" class="rounded-full bg-[#eef4f8] px-2 py-0.5 text-xs text-[#446688]">{{ t }}</span>
            </div>
          </div>
          <div class="flex shrink-0 gap-2">
            <button class="rounded-lg border border-[#446688] px-3 py-1.5 text-sm text-[#446688] hover:bg-[#eef4f8]" @click="openEdit(p)">编辑</button>
            <button class="rounded-lg border border-red-200 px-3 py-1.5 text-sm text-red-500 hover:bg-red-50" @click="remove(p)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <div v-if="editing" class="fixed inset-0 z-20 flex items-center justify-center bg-black/30 px-4" @click.self="editing = false">
      <div class="max-h-[88vh] w-full max-w-2xl overflow-y-auto rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-4 text-base font-semibold text-[#446688]">{{ form.slug ? `编辑文章（${form.slug}）` : '写新文章' }}</h2>
        <div class="space-y-3">
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">标题</span>
            <input v-model="form.title" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
          </label>
          <div class="grid grid-cols-2 gap-3">
            <label class="block">
              <span class="mb-1 block text-sm text-[#666]">发布日期</span>
              <input v-model="form.date" type="date" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
            </label>
            <label class="block">
              <span class="mb-1 block text-sm text-[#666]">标签（逗号分隔）</span>
              <input v-model="tagsText" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" placeholder="STM32, 踩坑" />
            </label>
          </div>
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">摘要（列表页展示）</span>
            <input v-model="form.summary" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
          </label>
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">正文（Markdown，支持代码块）</span>
            <textarea v-model="form.content" rows="14" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 font-mono text-sm outline-none focus:border-[#446688]"></textarea>
          </label>
          <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
          <p v-if="syncMsg" class="text-sm text-amber-600">{{ syncMsg }}</p>
        </div>
        <div class="mt-5 flex justify-end gap-2">
          <button class="rounded-lg border border-[#d8d4ca] px-4 py-2 text-sm text-[#555] hover:bg-[#fbfaf7]" @click="editing = false">取消</button>
          <button class="rounded-lg bg-[#446688] px-4 py-2 text-sm font-medium text-white hover:bg-[#3a5878]" @click="save">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>
