<script setup lang="ts">
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen bg-[var(--bg)]">
    <Navbar />
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6 md:py-8">
      <router-view />
    </main>
  </div>
</template>
