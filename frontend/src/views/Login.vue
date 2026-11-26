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
          @input="emailError = ''"
        />
        <p v-if="emailError" class="mt-1 text-sm text-[var(--error)]">{{ emailError }}</p>
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-[var(--text-h)] mb-2">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full p-3 border border-[var(--border)] rounded-lg bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="••••••••"
          @input="passwordError = ''"
        />
        <p v-if="passwordError" class="mt-1 text-sm text-[var(--error)]">{{ passwordError }}</p>
      </div>

      <button
        @click="login"
        :disabled="loading || !email || !password"
        class="w-full bg-[var(--accent)] text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity min-h-[44px]"
      >
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>

      <div class="mt-4 text-center">
        <router-link to="/" class="text-sm text-[var(--accent)] hover:underline">
          Back to Home
        </router-link>
      </div>

      <div v-if="error" class="mt-4 p-4 bg-[var(--error-bg)] border border-[var(--error)] rounded-lg text-[var(--error)]">
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
const emailError = ref('')
const passwordError = ref('')
const loading = ref(false)
const error = ref('')

function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function validateForm(): boolean {
  let isValid = true

  if (!email.value) {
    emailError.value = 'Email is required'
    isValid = false
  } else if (!validateEmail(email.value)) {
    emailError.value = 'Please enter a valid email address'
    isValid = false
  }

  if (!password.value) {
    passwordError.value = 'Password is required'
    isValid = false
  } else if (password.value.length < 6) {
    passwordError.value = 'Password must be at least 6 characters'
    isValid = false
  }

  return isValid
}

async function login() {
  if (!validateForm()) return

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
