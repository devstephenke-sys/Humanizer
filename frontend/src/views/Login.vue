<template>
  <div class="max-w-md mx-auto">
    <h1 class="text-3xl font-bold text-[var(--text-h)] mb-6 text-center">Sign In</h1>
    <p class="text-[var(--text)] mb-6 text-center">Sign in to save your documents.</p>

    <div class="border border-[var(--border)] rounded-lg p-6">
      <div class="mb-4">
        <label class="block text-sm font-medium text-[var(--text-h)] mb-2">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full p-3 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="your@email.com"
        />
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-[var(--text-h)] mb-2">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full p-3 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="••••••••"
        />
      </div>

      <button
        @click="login"
        :disabled="loading || !email || !password"
        class="w-full bg-[var(--accent)] text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
      >
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>

      <div class="mt-4 text-center">
        <router-link to="/" class="text-sm text-[var(--accent)] hover:underline">
          Back to Home
        </router-link>
      </div>

      <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
        {{ error }}
      </div>
    </div>

    <div class="mt-6 p-4 bg-[var(--code-bg)] rounded-lg">
      <p class="text-sm text-[var(--text)]">
        <strong>Note:</strong> All writing tools are free and work without an account. Sign in only if you want to save documents.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/auth'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function login() {
  loading.value = true
  error.value = ''

  try {
    const response = await authApi.login({
      email: email.value,
      password: password.value,
    })

    authStore.setToken(response.data.access_token)
    authStore.setUser(response.data.user)

    router.push('/workspace')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to sign in. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>
