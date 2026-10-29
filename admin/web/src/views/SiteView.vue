<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'

const site = ref(null)
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const saved = ref(false)
const ICONS = [
  { value: 'chip', label: '芯片（嵌入式）' },
  { value: 'ai', label: 'AI（大模型）' },
  { value: 'tools', label: '工具' },
  { value: 'web', label: '网页' },
]

async function load() {
  loading.value = true
  error.value = ''
  try {
    site.value = await api.getSite()
    if (!site.value.skillGroups) site.value.skillGroups = []
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function autoObfuscated() {
  if (!site.value) return
  const email = site.value.email || ''
  const at = email.indexOf('@')
  if (at > 0) {
    site.value.emailObfuscated = `${email.slice(0, at)} [at] ${email.slice(at + 1)}`
  }
}

function addGroup() {
  site.value.skillGroups.push({ title: '新技能组', icon: 'chip', skills: [] })
}
function removeGroup(i) {
  site.value.skillGroups.splice(i, 1)
}
function addSkill(g) {
  g.skills.push({ name: '', level: '熟悉' })
}
function removeSkill(g, i) {
  g.skills.splice(i, 1)
}

async function save() {
  saving.value = true
  saved.value = false
  error.value = ''
  try {
    await api.saveSite(site.value)
    saved.value = true
    setTimeout(() => (saved.value = false), 2500)
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-if="loading" class="py-16 text-center text-sm text-[#666]">加载中…</div>

  <div v-else-if="site" class="space-y-5">
    <p v-if="error" class="rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{{ error }}</p>

    <!-- 基础信息 -->
    <section class="rounded-xl border border-[#e5e2da] bg-white p-5 shadow-sm">
      <h2 class="mb-4 text-base font-semibold text-[#446688]">基础信息</h2>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
        <label class="block">
          <span class="mb-1 block text-sm text-[#666]">姓名</span>
          <input v-model="site.name" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
        </label>
        <label class="block">
          <span class="mb-1 block text-sm text-[#666]">角色 / 头衔</span>
          <input v-model="site.role" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
        </label>
      </div>
      <label class="mt-4 block">
        <span class="mb-1 block text-sm text-[#666]">Slogan</span>
        <input v-model="site.slogan" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
      </label>
      <label class="mt-4 block">
        <span class="mb-1 block text-sm text-[#666]">首屏导语（lead）</span>
        <input v-model="site.lead" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
      </label>
      <label class="mt-4 block">
        <span class="mb-1 block text-sm text-[#666]">关于我（about）</span>
        <textarea v-model="site.about" rows="4" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]"></textarea>
      </label>
      <div class="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
        <label class="block">
          <span class="mb-1 block text-sm text-[#666]">邮箱</span>
          <input v-model="site.email" @change="autoObfuscated" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
        </label>
        <label class="block">
          <span class="mb-1 flex items-center justify-between text-sm text-[#666]">
            邮箱（混淆展示）
            <button type="button" class="text-xs text-[#446688] underline" @click="autoObfuscated">自动生成</button>
          </span>
          <input v-model="site.emailObfuscated" class="w-full rounded-lg border border-[#d8d4ca] bg-[#fbfaf7] px-3 py-2 text-sm outline-none focus:border-[#446688]" />
        </label>
      </div>
    </section>

    <!-- 技能组 -->
    <section class="rounded-xl border border-[#e5e2da] bg-white p-5 shadow-sm">
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-base font-semibold text-[#446688]">技能栈（{{ site.skillGroups.length }} 组）</h2>
        <button class="rounded-lg bg-[#446688] px-3 py-1.5 text-sm text-white hover:bg-[#3a5878]" @click="addGroup">+ 添加技能组</button>
      </div>

      <div class="space-y-4">
        <div v-for="(g, gi) in site.skillGroups" :key="gi" class="rounded-lg border border-[#e5e2da] bg-[#fbfaf7] p-4">
          <div class="flex flex-wrap items-center gap-3">
            <input v-model="g.title" class="w-44 rounded-lg border border-[#d8d4ca] bg-white px-3 py-1.5 text-sm outline-none focus:border-[#446688]" placeholder="组名" />
            <select v-model="g.icon" class="rounded-lg border border-[#d8d4ca] bg-white px-3 py-1.5 text-sm outline-none focus:border-[#446688]">
              <option v-for="ic in ICONS" :key="ic.value" :value="ic.value">{{ ic.label }}</option>
            </select>
            <span class="text-xs text-[#999]">{{ g.skills.length }} 项技能</span>
            <button class="ml-auto text-sm text-red-500 hover:underline" @click="removeGroup(gi)">删除组</button>
          </div>
          <div class="mt-3 space-y-2">
            <div v-for="(s, si) in g.skills" :key="si" class="flex items-center gap-2">
              <input v-model="s.name" class="w-56 rounded-lg border border-[#d8d4ca] bg-white px-3 py-1.5 text-sm outline-none focus:border-[#446688]" placeholder="技能名" />
              <input v-model="s.level" class="w-36 rounded-lg border border-[#d8d4ca] bg-white px-3 py-1.5 text-sm outline-none focus:border-[#446688]" placeholder="能力标签，如 熟练/熟悉/了解" />
              <button class="text-sm text-red-400 hover:underline" @click="removeSkill(g, si)">移除</button>
            </div>
            <button class="text-sm text-[#446688] hover:underline" @click="addSkill(g)">+ 添加技能</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 保存 -->
    <div class="sticky bottom-4 flex items-center gap-3 rounded-xl border border-[#e5e2da] bg-white/95 p-4 shadow-md backdrop-blur">
      <button
        :disabled="saving"
        class="rounded-lg bg-[#446688] px-6 py-2 text-sm font-medium text-white hover:bg-[#3a5878] disabled:opacity-60"
        @click="save"
      >{{ saving ? '保存中…' : '保存全部修改' }}</button>
      <span v-if="saved" class="text-sm text-green-600">已保存，Astro 热更新会自动生效 ✓</span>
      <span v-if="error" class="text-sm text-red-600">{{ error }}</span>
    </div>
  </div>
</template>
