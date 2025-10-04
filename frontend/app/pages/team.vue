<template>
  <div class="particles-container">
    <Particles
      :particle-count="150"
      :particle-spread="8"
      :speed="0.08"
      :particle-colors="['#000']"
      :move-particles-on-hover="false"
      :particle-hover-factor="1"
      :alpha-particles="false"
      :particle-base-size="80"
      :size-randomness="1"
      :camera-distance="25"
      :disable-rotation="false"
      class="w-full h-full"
    />
    <div class="relative z-10">
      <Header />
      
      <div class="max-w-4xl mx-auto px-6 py-16">
        <ScrambleText
          :className="'max-w-3xl text-pretty mx-auto leading-tight text-center font-medium text-[clamp(16px,4vw,36px)] text-black mb-8'"
          :radius="120" 
          :duration="1.4" 
          :speed="0.6" 
          scrambleChars=".:*">
          NASA Space Apps Challenge 2025<br>
          Team ExoScout
        </ScrambleText>
        
        <div class="text-center mb-12">
          <p class="text-lg text-zinc-600 max-w-2xl mx-auto leading-relaxed">
            We are a passionate team of developers, designers, and space enthusiasts 
            participating in NASA's Space Apps Challenge 2025. Our mission: to make 
            exoplanet discovery accessible to everyone.
          </p>
        </div>

        <div class="border border-dashed border-zinc-300 rounded-lg p-6 mb-12 bg-zinc-50/50">
          <div class="flex items-center gap-3 mb-4">
            <img src="/nasa.png" alt="NASA Logo" class="h-6 w-7" />
            <h2 class="text-xl font-medium">Challenge Details</h2>
          </div>
          <div class="grid md:grid-cols-2 gap-6 text-sm">
            <div>
              <h3 class="font-medium mb-2 text-zinc-800">Event</h3>
              <p class="text-zinc-600">NASA Space Apps Challenge 2025</p>
            </div>
            <div>
              <h3 class="font-medium mb-2 text-zinc-800">Project</h3>
              <p class="text-zinc-600">ExoScout - Exoplanet Discovery Platform</p>
            </div>
            <div>
              <h3 class="font-medium mb-2 text-zinc-800">Category</h3>
              <p class="text-zinc-600">Astrophysics & Space Exploration</p>
            </div>
            <div>
              <h3 class="font-medium mb-2 text-zinc-800">Duration</h3>
              <p class="text-zinc-600">48 Hours Hackathon</p>
            </div>
          </div>
        </div>

        <div>
          <h2 class="text-2xl font-medium text-center mb-8">Meet Our Team</h2>
          <div class="grid md:grid-cols-2">
            <div class="border border-dashed border-r-0 border-zinc-300 p-6 hover:bg-zinc-50/50 transition-colors">
              <img 
                src="https://media.licdn.com/dms/image/v2/D4E03AQHTYK4oUJmH6w/profile-displayphoto-shrink_400_400/B4EZeayAzcHgAg-/0/1750648492072?e=1762387200&v=beta&t=WvPtyKZLZ72eBbm_iRc84xq6r9QqVFzvMIXmF8W9ehM" 
                alt="Milan G." 
                class="w-16 h-16 rounded-full mb-4 object-cover"
              />
              <h3 class="font-medium text-lg mb-2">Milan G.</h3>
              <p class="text-zinc-600 text-sm mb-3">Full-Stack Developer, AI & Project Manager</p>
              <p class="text-xs text-zinc-500">Full-stack developer passionate about space exploration and data visualization. Specializes in Vue.js, Node.js, and astronomical data processing.</p>
            </div>

            <div class="border border-dashed border-zinc-300 p-6 hover:bg-zinc-50/50 transition-colors">
              <img 
                src="https://media.licdn.com/dms/image/v2/D4D03AQGsONoaf48xcw/profile-displayphoto-shrink_400_400/B4DZhhQaPSHwAg-/0/1753978350464?e=1762387200&v=beta&t=5ThfLuIv2wT9dIVLFD-5WkqVGIqXUE-ApbDoSBxwlDA" 
                alt="Bizhan A." 
                class="w-16 h-16 rounded-full mb-4 object-cover"
              />
              <h3 class="font-medium text-lg mb-2">Bizhan A.</h3>
              <p class="text-zinc-600 text-sm mb-3">Backend, AI & Machine Learning</p>
              <p class="text-xs text-zinc-500">UI/UX specialist focused on creating intuitive interfaces for complex astronomical data. Expert in modern web technologies and user experience design.</p>
            </div>
          </div>
        </div>

        <div class="border border-dashed border-zinc-300 border-t-0 p-8 mb-12">
          <h2 class="text-2xl font-medium text-center mb-6">Our Mission</h2>
          <div class="max-w-3xl mx-auto text-center">
            <p class="text-zinc-700 leading-relaxed mb-6">
              ExoScout aims to democratize access to exoplanet discovery by creating an intuitive, 
              web-based platform that allows anyone to explore NASA's vast archives of astronomical data. 
              We believe that the wonder of discovering worlds beyond our solar system should be 
              accessible to students, researchers, and space enthusiasts worldwide.
            </p>
            <div class="grid md:grid-cols-3 gap-6 text-sm">
              <div class="text-center">
                <div class="w-12 h-12 bg-zinc-100 rounded-full mx-auto mb-3 flex items-center justify-center">
                  <svg class="w-6 h-6 text-zinc-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                </div>
                <h3 class="font-medium mb-2">Discover</h3>
                <p class="text-zinc-600">Search through thousands of confirmed exoplanets</p>
              </div>
              <div class="text-center">
                <div class="w-12 h-12 bg-zinc-100 rounded-full mx-auto mb-3 flex items-center justify-center">
                  <svg class="w-6 h-6 text-zinc-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
                  </svg>
                </div>
                <h3 class="font-medium mb-2">Filter</h3>
                <p class="text-zinc-600">Advanced filtering by size, distance, and habitability</p>
              </div>
              <div class="text-center">
                <div class="w-12 h-12 bg-zinc-100 rounded-full mx-auto mb-3 flex items-center justify-center">
                  <svg class="w-6 h-6 text-zinc-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                </div>
                <h3 class="font-medium mb-2">Analyze</h3>
                <p class="text-zinc-600">Visualize data and explore planetary characteristics</p>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center">
          <p class="text-zinc-600 mb-6">Ready to explore the cosmos?</p>
          <div class="flex justify-center gap-4">
            <NuxtLink to="/">
              <Button variant="secondary" size="md">Start Exploring</Button>
            </NuxtLink>
            <NuxtLink to="https://github.com/themilan1337/exoscout" target="_blank">
              <Button variant="outline" size="md">View on GitHub</Button>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import ScrambleText from "@/components/ScrambleText.vue"
import Button from "@/components/ui/Button.vue"
import Particles from "@/components/Particles.vue"

useHead({
  title: 'Team - ExoScout | NASA Space Apps Challenge 2025',
  meta: [
    { name: 'description', content: 'Meet the ExoScout team participating in NASA Space Apps Challenge 2025. Passionate developers and space enthusiasts making exoplanet discovery accessible to everyone.' },
    { name: 'keywords', content: 'NASA Space Apps Challenge, ExoScout, team, exoplanets, space exploration, hackathon' }
  ]
})
</script>

<style scoped>
.particles-container {
  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}
</style>