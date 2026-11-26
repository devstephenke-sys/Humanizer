<template>
  <nav class="border-b border-[var(--border)] bg-[var(--bg)]">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-bold text-[var(--text-h)]">
            Draftwell
          </router-link>
          <div class="ml-10 flex space-x-4">
            <router-link
              to="/humanizer"
              class="rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-[var(--accent-bg)]"
              :class="isActive('/humanizer') ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            >
              Humanizer
            </router-link>
            <router-link
              to="/detector"
              class="rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-[var(--accent-bg)]"
              :class="isActive('/detector') ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            >
              AI Detector
            </router-link>
            <div class="relative group">
              <button
                class="rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-[var(--accent-bg)] text-[var(--text)]"
              >
                More Tools
              </button>
              <div class="absolute left-0 mt-2 w-48 rounded-md bg-[var(--bg)] shadow-lg border border-[var(--border)] opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                <div class="py-1">
                  <router-link
                    to="/rewriter"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Rewriter
                  </router-link>
                  <router-link
                    to="/paraphraser"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Paraphraser
                  </router-link>
                  <router-link
                    to="/essay-rewriter"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Essay Rewriter
                  </router-link>
                  <router-link
                    to="/article-rewriter"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Article Rewriter
                  </router-link>
                  <router-link
                    to="/sentence-rewriter"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Sentence Rewriter
                  </router-link>
                  <router-link
                    to="/paragraph-rewriter"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Paragraph Rewriter
                  </router-link>
                  <router-link
                    to="/content-improvement"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Content Improvement
                  </router-link>
                  <router-link
                    to="/grammar"
                    class="block px-4 py-2 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)]"
                  >
                    Grammar Check
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <button
            @click="themeStore.toggleTheme"
            class="rounded-md p-2 text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
            title="Toggle theme"
          >
            <svg v-if="themeStore.isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          <router-link
            v-if="authStore.token"
            to="/workspace"
            class="rounded-md px-3 py-2 text-sm font-medium text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Workspace
          </router-link>
          <router-link
            v-else
            to="/login"
            class="rounded-md px-3 py-2 text-sm font-medium text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Sign In
          </router-link>
          <button
            v-if="authStore.token"
            @click="authStore.logout"
            class="rounded-md px-3 py-2 text-sm font-medium text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'

const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

function isActive(path: string) {
  return route.path === path
}
</script>
