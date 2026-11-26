<template>
  <nav class="border-b border-[var(--border)] bg-[var(--bg)] sticky top-0 z-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-bold text-[var(--text-h)]">
            Humanizer
          </router-link>
          <div class="ml-8 hidden md:flex gap-2">
            <router-link
              to="/humanizer"
              class="rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
              :class="isActive('/humanizer') ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            >
              Humanizer
            </router-link>
            <router-link
              to="/detector"
              class="rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
              :class="isActive('/detector') ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            >
              AI Detector
            </router-link>
            <div class="relative group">
              <button
                class="rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-[var(--accent-bg)] text-[var(--text)] flex items-center gap-1 min-h-[44px]"
                aria-label="More tools dropdown"
              >
                More Tools
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="absolute left-0 mt-2 w-56 rounded-lg bg-[var(--bg)] shadow-xl border border-[var(--border)] opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div class="py-2">
                  <router-link
                    to="/rewriter"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Rewriter
                  </router-link>
                  <router-link
                    to="/paraphraser"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Paraphraser
                  </router-link>
                  <router-link
                    to="/essay-rewriter"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Essay Rewriter
                  </router-link>
                  <router-link
                    to="/article-rewriter"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Article Rewriter
                  </router-link>
                  <router-link
                    to="/sentence-rewriter"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Sentence Rewriter
                  </router-link>
                  <router-link
                    to="/paragraph-rewriter"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Paragraph Rewriter
                  </router-link>
                  <router-link
                    to="/content-improvement"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Content Improvement
                  </router-link>
                  <router-link
                    to="/grammar"
                    class="block px-4 py-3 text-sm text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
                  >
                    Grammar Check
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="themeStore.toggleTheme"
            class="rounded-md p-3 text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
            :aria-label="themeStore.isDark ? 'Switch to light mode' : 'Switch to dark mode'"
            title="Toggle theme"
          >
            <svg v-if="themeStore.isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          <div class="hidden md:flex items-center gap-2">
            <router-link
              v-if="authStore.token"
              to="/workspace"
              class="rounded-md px-4 py-3 text-sm font-medium text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
            >
              Workspace
            </router-link>
            <router-link
              v-else
              to="/login"
              class="rounded-md px-4 py-3 text-sm font-medium text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
            >
              Sign In
            </router-link>
            <button
              v-if="authStore.token"
              @click="authStore.logout"
              class="rounded-md px-4 py-3 text-sm font-medium text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] flex items-center"
            >
              Sign Out
            </button>
          </div>
          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden rounded-md p-3 text-[var(--text)] hover:bg-[var(--accent-bg)] transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
            :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
            :aria-expanded="mobileMenuOpen"
          >
            <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    <!-- Mobile menu -->
    <div v-if="mobileMenuOpen" class="md:hidden border-t border-[var(--border)] bg-[var(--bg)]">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          to="/humanizer"
          class="block rounded-md px-4 py-3 text-base font-medium transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          :class="isActive('/humanizer') ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
          @click="mobileMenuOpen = false"
        >
          Humanizer
        </router-link>
        <router-link
          to="/detector"
          class="block rounded-md px-4 py-3 text-base font-medium transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          :class="isActive('/detector') ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
          @click="mobileMenuOpen = false"
        >
          AI Detector
        </router-link>
        <router-link
          to="/rewriter"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Rewriter
        </router-link>
        <router-link
          to="/paraphraser"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Paraphraser
        </router-link>
        <router-link
          to="/essay-rewriter"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Essay Rewriter
        </router-link>
        <router-link
          to="/article-rewriter"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Article Rewriter
        </router-link>
        <router-link
          to="/sentence-rewriter"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Sentence Rewriter
        </router-link>
        <router-link
          to="/paragraph-rewriter"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Paragraph Rewriter
        </router-link>
        <router-link
          to="/content-improvement"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Content Improvement
        </router-link>
        <router-link
          to="/grammar"
          class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          @click="mobileMenuOpen = false"
        >
          Grammar Check
        </router-link>
        <div class="border-t border-[var(--border)] pt-2 mt-2">
          <router-link
            v-if="authStore.token"
            to="/workspace"
            class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
            @click="mobileMenuOpen = false"
          >
            Workspace
          </router-link>
          <router-link
            v-else
            to="/login"
            class="block rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
            @click="mobileMenuOpen = false"
          >
            Sign In
          </router-link>
          <button
            v-if="authStore.token"
            @click="authStore.logout(); mobileMenuOpen = false"
            class="block w-full text-left rounded-md px-4 py-3 text-base font-medium text-[var(--text)] transition-colors hover:bg-[var(--accent-bg)] min-h-[44px] flex items-center"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'

const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const mobileMenuOpen = ref(false)

function isActive(path: string) {
  return route.path === path
}
</script>
