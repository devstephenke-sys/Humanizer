<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-[var(--text-h)] mb-6">Content Improvement</h1>
    <p class="text-[var(--text)] mb-6">Improve clarity, directness, and readability of your text.</p>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="border border-[var(--border)] rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-[var(--text-h)]">Original Text</h2>
          <div class="text-sm text-[var(--text)]">{{ wordCount }} words</div>
        </div>
        <textarea
          v-model="inputText"
          class="w-full h-64 p-4 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] resize-none focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="Paste your text here..."
          @input="updateCounts"
        ></textarea>

        <div class="mt-6 flex gap-3">
          <button
            @click="improve"
            :disabled="!inputText || loading"
            class="flex-1 bg-[var(--accent)] text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
          >
            {{ loading ? 'Processing...' : 'Improve' }}
          </button>
          <button @click="clearInput" class="px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors">Clear</button>
        </div>
      </div>

      <div class="border border-[var(--border)] rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-[var(--text-h)]">Improved Text</h2>
        </div>
        <div class="w-full h-64 p-4 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] overflow-y-auto">
          <div v-if="loading" class="flex items-center justify-center h-full">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)]"></div>
          </div>
          <div v-else-if="outputText" class="whitespace-pre-wrap">{{ outputText }}</div>
          <div v-else class="text-[var(--text)] opacity-50">Result will appear here...</div>
        </div>

        <div v-if="outputText" class="mt-6 flex gap-3">
          <button @click="copyToClipboard" class="flex-1 px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors">Copy</button>
          <button @click="downloadTxt" class="flex-1 px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors">Download TXT</button>
          <button v-if="authStore.token" @click="saveDocument" class="flex-1 px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors">Save</button>
        </div>

        <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { writingApi } from '../api/writing'
import { documentsApi } from '../api/documents'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const inputText = ref('')
const outputText = ref('')
const loading = ref(false)
const error = ref('')

const wordCount = computed(() => inputText.value.trim().split(/\s+/).filter(w => w).length)

function updateCounts() {}

async function improve() {
  if (!inputText.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    const response = await writingApi.contentImprove({ text: inputText.value })
    outputText.value = response.data.rewritten
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to improve text.'
  } finally {
    loading.value = false
  }
}

function clearInput() {
  inputText.value = ''
  outputText.value = ''
  error.value = ''
}

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(outputText.value)
    alert('Copied!')
  } catch (e) {
    alert('Failed to copy')
  }
}

function downloadTxt() {
  const blob = new Blob([outputText.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'improved-text.txt'
  a.click()
  URL.revokeObjectURL(url)
}

async function saveDocument() {
  try {
    await documentsApi.save({ title: `Improved - ${new Date().toLocaleDateString()}`, content: outputText.value, tool: 'content-improvement' })
    alert('Saved!')
  } catch (e) {
    alert('Failed to save')
  }
}
</script>
