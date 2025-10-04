<template>
  <div class="particles-container">
    <Particles
      :particle-count="200"
      :particle-spread="10"
      :speed="0.1"
      :particle-colors="['#000']"
      :move-particles-on-hover="false"
      :particle-hover-factor="1"
      :alpha-particles="false"
      :particle-base-size="100"
      :size-randomness="1"
      :camera-distance="20"
      :disable-rotation="false"
      class="w-full h-full"
    />
    <div class="relative z-10">
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
  </div>
</template>
<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import ScrambleText from "@/components/ScrambleText.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Particles from "@/components/Particles.vue";
</script>
<style scoped>
.particles-container {
    width: 100%;
    height: 100vh;
    position: relative;
    overflow: hidden;
  }
</style>