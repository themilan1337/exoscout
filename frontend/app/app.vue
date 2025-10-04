<script setup lang="ts">
import { Analytics } from '@vercel/analytics/nuxt'
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
      <Analytics/>
    </NuxtLayout>
  </div>
</template>