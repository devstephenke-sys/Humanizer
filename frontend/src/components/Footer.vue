<template>
  <footer class="border-t border-[var(--border)] bg-[var(--bg)] mt-auto">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 class="text-lg font-semibold text-[var(--text-h)] mb-4">Humanizer</h3>
          <p class="text-sm text-[var(--text)]">
            A free AI writing workspace for rewriting drafts and estimating AI-like patterns.
          </p>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-[var(--text-h)] mb-4">Tools</h3>
          <ul class="space-y-2 text-sm text-[var(--text)]">
            <li><router-link to="/humanizer" class="hover:text-[var(--accent)] transition-colors">Humanizer</router-link></li>
            <li><router-link to="/detector" class="hover:text-[var(--accent)] transition-colors">AI Detector</router-link></li>
            <li><router-link to="/rewriter" class="hover:text-[var(--accent)] transition-colors">Rewriter</router-link></li>
            <li><router-link to="/paraphraser" class="hover:text-[var(--accent)] transition-colors">Paraphraser</router-link></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-[var(--text-h)] mb-4">About</h3>
          <p class="text-sm text-[var(--text)] mb-2">
            AI detection is probabilistic and can produce false positives and false negatives.
          </p>
          <p class="text-sm text-[var(--text)]">
            Always review content manually for accuracy.
          </p>
        </div>
      </div>
      <div class="mt-8 pt-8 border-t border-[var(--border)] text-center text-sm text-[var(--text)]">
        <p>&copy; {{ new Date().getFullYear() }} Humanizer. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// No script needed for this simple footer
</script>
