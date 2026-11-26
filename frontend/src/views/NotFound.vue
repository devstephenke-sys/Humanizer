<template>
  <div class="min-h-[60vh] flex items-center justify-center text-center">
    <div class="max-w-md">
      <h1 class="text-6xl font-bold text-[var(--accent)] mb-4">404</h1>
      <h2 class="text-2xl font-semibold text-[var(--text-h)] mb-4">Page Not Found</h2>
      <p class="text-[var(--text)] mb-8">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <router-link
        to="/"
        class="inline-block bg-[var(--accent)] text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 transition-opacity"
      >
        Go Home
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// No script needed for this simple page
</script>
