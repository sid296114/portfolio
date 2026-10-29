<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'

const projects = ref([])
const loading = ref(true)
const error = ref('')
const editing = ref(false)
const form = ref(emptyForm())
const tagsText = ref('')
const syncMsg = ref('')

function emptyForm() {
  return { id: '', name: '', description: '', thumbnail: '', tags: [], detail: '' }
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    projects.value = await api.getProjects()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.value = emptyForm()
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
    if (form.value.id) {
      res = await api.updateProject(form.value.id, form.value)
    } else {
      res = await api.createProject(form.value)
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
  if (!confirm(`确定删除项目「${p.name}」？`)) return
  try {
    await api.deleteProject(p.id)
    await load()
  } catch (e) {
    error.value = e.message
  }
}
function toggleTag(t) {
  const i = form.value.tags.indexOf(t)
  if (i >= 0) form.value.tags.splice(i, 1)
  else form.value.tags.push(t)
}
const TAG_SUGGESTIONS = ['STM32', '传感器', '物联网', 'LoRA', '微调', '数据集', '嵌入式', '前端']
onMounted(load)
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
      <button class="ml-auto rounded-lg bg-[#446688] px-4 py-2 text-sm font-medium text-white hover:bg-[#3a5878]" @click="openCreate">+ 新增项目</button>
    </div>

    <div v-if="loading" class="py-16 text-center text-sm text-[#666]">加载中…</div>

    <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="p in projects" :key="p.id" class="rounded-xl border border-[#e5e2da] bg-white p-4 shadow-sm">
        <div class="flex items-center gap-3">
          <img :src="p.thumbnail" alt="" class="h-12 w-12 rounded-lg bg-[#eef2f6] object-cover" />
          <div class="min-w-0 flex-1">
            <div class="truncate text-sm font-semibold text-[#446688]">{{ p.name }}</div>
            <div class="text-xs text-[#999]">{{ p.id }}</div>
          </div>
        </div>
        <p class="mt-2 line-clamp-2 text-sm text-[#555]">{{ p.description }}</p>
        <div class="mt-2 flex flex-wrap gap-1">
          <span v-for="t in p.tags" :key="t" class="rounded-full bg-[#eef4f8] px-2 py-0.5 text-xs text-[#446688]">{{ t }}</span>
        </div>
        <div class="mt-3 flex gap-2">
          <button class="flex-1 rounded-lg border border-[#446688] py-1.5 text-sm text-[#446688] hover:bg-[#eef4f8]" @click="openEdit(p)">编辑</button>
          <button class="flex-1 rounded-lg border border-red-200 py-1.5 text-sm text-red-500 hover:bg-red-50" @click="remove(p)">删除</button>
        </div>
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <div v-if="editing" class="fixed inset-0 z-20 flex items-center justify-center bg-black/30 px-4" @click.self="editing = false">
      <div class="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-4 text-base font-semibold text-[#446688]">{{ form.id ? '编辑项目' : '新增项目' }}</h2>
        <div class="space-y-3">
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">项目名称</span>
            <input v-model="form.name" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
          </label>
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">简介（列表展示）</span>
            <textarea v-model="form.description" rows="2" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]"></textarea>
          </label>
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">缩略图路径（public/assets/projects/ 下）</span>
            <input v-model="form.thumbnail" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" placeholder="/assets/projects/xxx.png" />
          </label>
          <div>
            <span class="mb-1 block text-sm text-[#666]">技术标签</span>
            <div class="flex flex-wrap gap-1.5">
              <button
                v-for="t in TAG_SUGGESTIONS" :key="t" type="button"
                :class="form.tags.includes(t) ? 'bg-[#446688] text-white' : 'bg-[#eef4f8] text-[#446688]'"
                class="rounded-full px-2.5 py-1 text-xs"
                @click="toggleTag(t)"
              >{{ t }}</button>
            </div>
            <input v-model="tagsText" class="mt-2 w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" placeholder="或直接输入：标签1, 标签2" />
          </div>
          <label class="block">
            <span class="mb-1 block text-sm text-[#666]">详情（弹窗展示）</span>
            <textarea v-model="form.detail" rows="5" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]"></textarea>
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
