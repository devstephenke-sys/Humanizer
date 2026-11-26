<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-[var(--text-h)] mb-6">Workspace</h1>
    <p class="text-[var(--text)] mb-6">Manage your saved documents.</p>

    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)]"></div>
    </div>

    <div v-else-if="documents.length === 0" class="text-center py-12 border border-[var(--border)] rounded-lg">
      <p class="text-[var(--text)]">No saved documents yet.</p>
      <router-link to="/humanizer" class="inline-block mt-4 bg-[var(--accent)] text-white px-6 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity">
        Start Writing
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="doc in documents"
        :key="doc.id"
        class="border border-[var(--border)] rounded-lg p-4 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start mb-2">
          <h3 class="font-semibold text-[var(--text-h)] truncate flex-1">{{ doc.title }}</h3>
          <button
            @click="deleteDocument(doc.id)"
            class="ml-2 text-red-500 hover:text-red-700 transition-colors"
            title="Delete"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        <p class="text-xs text-[var(--text)] mb-2">{{ doc.tool }}</p>
        <p class="text-sm text-[var(--text)] mb-3 line-clamp-3">{{ doc.content.substring(0, 150) }}...</p>
        <div class="flex justify-between items-center">
          <span class="text-xs text-[var(--text)]">{{ formatDate(doc.created_at) }}</span>
          <button
            @click="openDocument(doc)"
            class="text-sm text-[var(--accent)] hover:underline"
          >
            Open
          </button>
        </div>
      </div>
    </div>

    <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { documentsApi } from '../api/documents'
import type { Document } from '../api/writing'

const router = useRouter()
const documents = ref<Document[]>([])
const loading = ref(false)
const error = ref('')

async function loadDocuments() {
  loading.value = true
  error.value = ''
  try {
    const response = await documentsApi.list()
    documents.value = response.data
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to load documents.'
  } finally {
    loading.value = false
  }
}

async function deleteDocument(id: number) {
  if (!confirm('Are you sure you want to delete this document?')) return
  try {
    await documentsApi.delete(id)
    documents.value = documents.value.filter(d => d.id !== id)
  } catch (e) {
    alert('Failed to delete document')
  }
}

function openDocument(doc: Document) {
  // For now, just copy content to clipboard
  navigator.clipboard.writeText(doc.content)
  alert('Content copied to clipboard!')
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadDocuments()
})
</script>
