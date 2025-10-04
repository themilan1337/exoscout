<template>
    <div>
        <Header />
        <ScrambleText
    :className="'max-w-3xl mx-auto mt-24 leading-tight text-center font-medium text-[clamp(14px,4vw,32px)] text-black'"
    :radius="100"
    :duration="1.2"
    :speed="0.5"
    scrambleChars=".:"
  >
    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Similique pariatur dignissimos porro eius quam doloremque 
    et enim velit nobis maxime.
  </ScrambleText>
    </div>
</template>
<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import ScrambleText from "@/components/ScrambleText.vue";
</script>
