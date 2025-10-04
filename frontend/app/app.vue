<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
      <Analytics/>
    </NuxtLayout>
  </div>
</template>
<script lang="ts">
import { Analytics } from '@vercel/analytics/nuxt'
</script>