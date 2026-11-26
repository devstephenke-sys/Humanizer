<template>
  <div class="text-center">
    <h1 class="text-5xl font-bold text-[var(--text-h)] mb-6">
      Your Free AI Writing Workspace
    </h1>
    <p class="text-xl text-[var(--text)] mb-12 max-w-2xl mx-auto">
      Transform AI-generated text into natural language, detect AI patterns, and improve your writing with powerful tools—all completely free.
    </p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
      <div
        v-for="tool in tools"
        :key="tool.name"
        class="border border-[var(--border)] rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
        @click="$router.push(tool.path)"
      >
        <div class="text-[var(--accent)] mb-3">
          <component :is="tool.icon" class="w-8 h-8" />
        </div>
        <h3 class="text-lg font-semibold text-[var(--text-h)] mb-2">{{ tool.name }}</h3>
        <p class="text-[var(--text)] text-sm">{{ tool.description }}</p>
      </div>
    </div>

    <div class="border-t border-[var(--border)] pt-8">
      <h2 class="text-2xl font-semibold text-[var(--text-h)] mb-4">Why Draftwell?</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
        <div>
          <h3 class="font-semibold text-[var(--text-h)] mb-2">100% Free</h3>
          <p class="text-[var(--text)] text-sm">No subscriptions, no payments, no word limits. All features are accessible to everyone.</p>
        </div>
        <div>
          <h3 class="font-semibold text-[var(--text-h)] mb-2">Privacy First</h3>
          <p class="text-[var(--text)] text-sm">Your documents are stored securely with user isolation. Unsaved text is never stored.</p>
        </div>
        <div>
          <h3 class="font-semibold text-[var(--text-h)] mb-2">Multiple Tools</h3>
          <p class="text-[var(--text)] text-sm">Humanizer, detector, rewriter, paraphraser, and more—all in one workspace.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'

const tools = [
  {
    name: 'AI Humanizer',
    description: 'Rewrite AI-generated text into natural, human-like language with adjustable intensity.',
    path: '/humanizer',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' })
    ])
  },
  {
    name: 'AI Detector',
    description: 'Estimate how AI-like your text reads with quick and deep analysis modes.',
    path: '/detector',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
    ])
  },
  {
    name: 'Rewriter',
    description: 'General-purpose text rewriting with multiple intensity levels.',
    path: '/rewriter',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' })
    ])
  },
  {
    name: 'Paraphraser',
    description: 'Rephrase text while keeping the same meaning.',
    path: '/paraphraser',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' })
    ])
  },
  {
    name: 'Essay Rewriter',
    description: 'Rewrite essays with academic tone and structure.',
    path: '/essay-rewriter',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
    ])
  },
  {
    name: 'Grammar Check',
    description: 'Improve grammar and readability with explanations.',
    path: '/grammar',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9' })
    ])
  }
]
</script>
