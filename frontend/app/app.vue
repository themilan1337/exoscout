<script setup lang="ts">
import { Analytics } from '@vercel/analytics/nuxt'
</script>

<template>
  <div class="bg-zinc-950">
    <NuxtLayout>
      <NuxtPage />
      <Analytics/>
    </NuxtLayout>
  </div>
</template>