<template>
  <div class="max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold text-[var(--text-h)] mb-6">AI Humanizer</h1>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Input Section -->
      <div class="border border-[var(--border)] rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-[var(--text-h)]">Original Text</h2>
          <div class="text-sm text-[var(--text)]">
            {{ wordCount }} words · {{ characterCount }} characters
          </div>
        </div>
        <textarea
          v-model="inputText"
          class="w-full h-48 md:h-64 p-4 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] resize-none focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="Paste your text here..."
          @input="updateCounts"
        ></textarea>

        <!-- Settings -->
        <div class="mt-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-[var(--text-h)] mb-2">
              Intensity: {{ intensity }}
            </label>
            <input
              v-model.number="intensity"
              type="range"
              min="1"
              max="10"
              class="w-full h-2 bg-[var(--border)] rounded-lg appearance-none cursor-pointer"
            />
            <div class="flex justify-between text-xs text-[var(--text)] mt-1">
              <span>Light</span>
              <span>Medium</span>
              <span>Strong</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-[var(--text-h)] mb-2">Profile</label>
            <select
              v-model="profile"
              class="w-full p-2 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
            >
              <option value="swift">Swift - Fast, direct rewrite</option>
              <option value="studio">Studio - Balanced coherence</option>
              <option value="careful">Careful - Preserves structure</option>
              <option value="plain">Plain - Simple language</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-[var(--text-h)] mb-2">Language</label>
            <select
              v-model="language"
              class="w-full p-2 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="it">Italian</option>
              <option value="pt">Portuguese</option>
            </select>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <button
            @click="humanize"
            :disabled="!inputText || loading"
            class="flex-1 bg-[var(--accent)] text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
          >
            {{ loading ? 'Processing...' : 'Humanize' }}
          </button>
          <button
            @click="clearInput"
            class="px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Clear
          </button>
        </div>
      </div>

      <!-- Output Section -->
      <div class="border border-[var(--border)] rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-[var(--text-h)]">Humanized Text</h2>
          <div v-if="outputText" class="text-sm text-[var(--text)]">
            {{ outputWordCount }} words · {{ outputCharacterCount }} characters
          </div>
        </div>
        <div
          class="w-full h-48 md:h-64 p-4 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] overflow-y-auto"
        >
          <div v-if="loading" class="flex items-center justify-center h-full">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)]"></div>
          </div>
          <div v-else-if="outputText" class="whitespace-pre-wrap">{{ outputText }}</div>
          <div v-else class="text-[var(--text)] opacity-50">Result will appear here...</div>
        </div>

        <div v-if="outputText" class="mt-6 flex flex-wrap gap-3">
          <button
            @click="copyToClipboard"
            class="flex-1 min-w-[100px] px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Copy
          </button>
          <button
            @click="downloadTxt"
            class="flex-1 min-w-[100px] px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Download TXT
          </button>
          <button
            @click="downloadDocx"
            class="flex-1 min-w-[100px] px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Download DOCX
          </button>
          <button
            v-if="authStore.token"
            @click="saveDocument"
            class="flex-1 min-w-[100px] px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Save
          </button>
        </div>

        <div v-if="error" class="mt-4 p-4 bg-[var(--error-bg)] border border-[var(--error)] rounded-lg text-[var(--error)]">
          {{ error }}
        </div>
      </div>
    </div>

    <!-- Comparison View -->
    <div v-if="showComparison && inputText && outputText" class="mt-6 border border-[var(--border)] rounded-lg p-6">
      <h2 class="text-lg font-semibold text-[var(--text-h)] mb-4">Side-by-Side Comparison</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 bg-[var(--code-bg)] rounded-lg">
          <h3 class="text-sm font-medium text-[var(--text-h)] mb-2">Original</h3>
          <p class="text-sm text-[var(--text)] whitespace-pre-wrap">{{ inputText }}</p>
        </div>
        <div class="p-4 bg-[var(--code-bg)] rounded-lg">
          <h3 class="text-sm font-medium text-[var(--text-h)] mb-2">Humanized</h3>
          <p class="text-sm text-[var(--text)] whitespace-pre-wrap">{{ outputText }}</p>
        </div>
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
const intensity = ref(5)
const profile = ref<'swift' | 'studio' | 'careful' | 'plain'>('studio')
const language = ref('en')
const loading = ref(false)
const error = ref('')
const showComparison = ref(false)

const wordCount = computed(() => inputText.value.trim().split(/\s+/).filter(w => w).length)
const characterCount = computed(() => inputText.value.length)
const outputWordCount = computed(() => outputText.value.trim().split(/\s+/).filter(w => w).length)
const outputCharacterCount = computed(() => outputText.value.length)

function updateCounts() {
  // Counts are computed
}

async function humanize() {
  if (!inputText.value.trim()) return

  loading.value = true
  error.value = ''

  try {
    const response = await writingApi.rewrite({
      text: inputText.value,
      intensity: intensity.value,
      profile: profile.value,
      language: language.value,
    })
    outputText.value = response.data.rewritten
    showComparison.value = true
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to humanize text. Please try again.'
  } finally {
    loading.value = false
  }
}

function clearInput() {
  inputText.value = ''
  outputText.value = ''
  showComparison.value = false
  error.value = ''
}

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(outputText.value)
    alert('Copied to clipboard!')
  } catch (e) {
    alert('Failed to copy')
  }
}

function downloadTxt() {
  const blob = new Blob([outputText.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'humanized-text.txt'
  a.click()
  URL.revokeObjectURL(url)
}

async function downloadDocx() {
  try {
    const response = await writingApi.downloadDocx({
      text: inputText.value,
      intensity: intensity.value,
      profile: profile.value,
      language: language.value,
    })
    const url = URL.createObjectURL(new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' }))
    const a = document.createElement('a')
    a.href = url
    a.download = 'humanized-text.docx'
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    alert('Failed to download DOCX')
  }
}

async function saveDocument() {
  try {
    await documentsApi.save({
      title: `Humanized - ${new Date().toLocaleDateString()}`,
      content: outputText.value,
      tool: 'humanizer',
    })
    alert('Document saved!')
  } catch (e) {
    alert('Failed to save document')
  }
}
</script>
