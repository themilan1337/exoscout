<template>
  <div>
    <Header />
    <ScrambleText
      :className="'max-w-3xl text-pretty mx-auto mt-24 leading-tight text-center font-medium text-[clamp(14px,4vw,32px)] text-black'"
      :radius="100" :duration="1.2" :speed="0.5" scrambleChars=".:">
      Discover Exoplanets.<br>
      Your gateway to real data from NASA’s <br> archives—search, filter, and explore <br> worlds beyond our solar <br> system in seconds.
    </ScrambleText>
    <div class="flex mx-auto justify-center items-center mt-8">
      <Input placeholder="Enter ID" variant="secondary" size="sm" class="mr-2" />
      <Button variant="secondary" size="sm">Find some planets</Button>
    </div>
  </div>
</template>
<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import ScrambleText from "@/components/ScrambleText.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
</script>
