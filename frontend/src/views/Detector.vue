<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-[var(--text-h)] mb-6">AI Detector</h1>

    <div class="border border-[var(--border)] rounded-lg p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-[var(--text-h)]">Input Text</h2>
        <div class="text-sm text-[var(--text)]">
          {{ wordCount }} words · {{ characterCount }} characters
        </div>
      </div>
      <textarea
        v-model="inputText"
        class="w-full h-64 p-4 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] resize-none focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
        placeholder="Paste your text here to check for AI patterns..."
        @input="updateCounts"
      ></textarea>

      <div class="mt-4">
        <label class="block text-sm font-medium text-[var(--text-h)] mb-2">Analysis Mode</label>
        <div class="flex gap-4">
          <label class="flex items-center">
            <input
              v-model="mode"
              type="radio"
              value="quick"
              class="mr-2"
            />
            <span class="text-[var(--text)]">Quick</span>
          </label>
          <label class="flex items-center">
            <input
              v-model="mode"
              type="radio"
              value="deep"
              class="mr-2"
            />
            <span class="text-[var(--text)]">Deep</span>
          </label>
        </div>
      </div>

      <div v-if="wordCount > 0 && wordCount < 100" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-700 text-sm">
        ⚠️ Short texts (under 100 words) may produce less reliable results.
      </div>

      <div class="mt-6 flex gap-3">
        <button
          @click="detect"
          :disabled="!inputText || loading"
          class="flex-1 bg-[var(--accent)] text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
        >
          {{ loading ? 'Scanning...' : 'Analyze' }}
        </button>
        <button
          @click="clearInput"
          class="px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
        >
          Clear
        </button>
      </div>
    </div>

    <!-- Results -->
    <div v-if="result" class="border border-[var(--border)] rounded-lg p-6">
      <h2 class="text-lg font-semibold text-[var(--text-h)] mb-4">Analysis Results</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div class="p-6 bg-[var(--code-bg)] rounded-lg text-center">
          <div class="text-4xl font-bold mb-2" :class="scoreColor">{{ result.overall_score }}%</div>
          <div class="text-lg font-medium text-[var(--text-h)]">{{ result.label }}</div>
          <div class="text-sm text-[var(--text)] mt-2">AI Likelihood Score</div>
        </div>
        <div class="p-6 bg-[var(--code-bg)] rounded-lg">
          <h3 class="font-medium text-[var(--text-h)] mb-3">Understanding the Score</h3>
          <p class="text-sm text-[var(--text)] mb-2">
            This score estimates how similar the text is to AI-generated content. It is <strong>not definitive proof</strong> of authorship.
          </p>
          <p class="text-sm text-[var(--text)]">
            AI detection is probabilistic and can produce false positives and false negatives. Always review content manually.
          </p>
        </div>
      </div>

      <div v-if="result.highlights && result.highlights.length > 0" class="mb-6">
        <h3 class="font-medium text-[var(--text-h)] mb-3">Sentence Analysis</h3>
        <div class="space-y-2">
          <div
            v-for="(highlight, index) in result.highlights"
            :key="index"
            class="p-3 rounded-lg"
            :class="highlightClass(highlight.score)"
          >
            <span class="text-sm">{{ highlight.text }}</span>
            <span class="ml-2 text-xs font-medium">{{ highlight.score }}% AI</span>
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button
          @click="copyToClipboard"
          class="flex-1 px-4 py-3 border border-[var(--border)] rounded-lg text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
        >
          Copy Results
        </button>
        <router-link
          to="/humanizer"
          class="flex-1 px-4 py-3 bg-[var(--accent)] text-white rounded-lg font-medium hover:opacity-90 text-center transition-opacity"
        >
          Humanize This Text
        </router-link>
      </div>
    </div>

    <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { writingApi } from '../api/writing'

const inputText = ref('')
const mode = ref<'quick' | 'deep'>('quick')
const loading = ref(false)
const error = ref('')
const result = ref<any>(null)

const wordCount = computed(() => inputText.value.trim().split(/\s+/).filter(w => w).length)
const characterCount = computed(() => inputText.value.length)

const scoreColor = computed(() => {
  if (!result.value) return 'text-[var(--text)]'
  const score = result.value.overall_score
  if (score < 30) return 'text-green-600'
  if (score < 70) return 'text-yellow-600'
  return 'text-red-600'
})

function updateCounts() {
  // Counts are computed
}

async function detect() {
  if (!inputText.value.trim()) return

  loading.value = true
  error.value = ''
  result.value = null

  try {
    const response = await writingApi.detect({
      text: inputText.value,
      mode: mode.value,
    })
    result.value = response.data
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to analyze text. Please try again.'
  } finally {
    loading.value = false
  }
}

function clearInput() {
  inputText.value = ''
  result.value = null
  error.value = ''
}

function highlightClass(score: number) {
  if (score < 30) return 'bg-green-50 border border-green-200'
  if (score < 70) return 'bg-yellow-50 border border-yellow-200'
  return 'bg-red-50 border border-red-200'
}

async function copyToClipboard() {
  try {
    const text = `AI Detection Results\nScore: ${result.value.overall_score}%\nLabel: ${result.value.label}\n\nSentence Analysis:\n${result.value.highlights.map((h: any) => `${h.text} (${h.score}% AI)`).join('\n')}`
    await navigator.clipboard.writeText(text)
    alert('Results copied to clipboard!')
  } catch (e) {
    alert('Failed to copy')
  }
}
</script>
