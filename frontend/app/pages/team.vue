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
        <ScrambleOld
          trigger="auto"
          :auto-delay="800"
          :animate-on-mount="true"
          :duration="1.4" 
          :speed="0.6" 
          scramble-chars=".:*"
          class="max-w-3xl text-pretty mx-auto leading-tight text-center font-medium text-[clamp(16px,4vw,36px)] text-zinc-100 mb-8"
        >
          NASA Space Apps Challenge 2025<br>
          Project ExoScout by Synapse team
        </ScrambleOld>
        
        <div class="text-center mb-12">
          <ScrambleText
            trigger="auto"
            :auto-delay="2000"
            :animate-on-mount="true"
            tag="p"
            class="text-lg text-zinc-600 max-w-2xl mx-auto leading-relaxed"
          >
            We are a passionate team of developers, designers, and space enthusiasts 
            participating in NASA's Space Apps Challenge 2025. Our mission: to make 
            exoplanet discovery accessible to everyone.
          </ScrambleText>
        </div>

        <div class="border border-dashed border-zinc-300 p-6 mb-6">
          <div class="flex items-center gap-3 mb-4">
            <img src="/nasa.png" alt="NASA Logo" class="h-6 w-7" />
            <ScrambleText
              trigger="hover"
              tag="h2"
              class="text-xl font-medium text-zinc-100"
            >
              Challenge Details
            </ScrambleText>
          </div>
          <div class="grid md:grid-cols-2 gap-6 text-sm">
            <div>
              <h3 class="font-medium mb-2 text-zinc-100">Event</h3>
              <p class="text-zinc-600">NASA Space Apps Challenge 2025</p>
            </div>
            <div>
              <h3 class="font-medium mb-2 text-zinc-100">Project</h3>
              <p class="text-zinc-600">ExoScout - Exoplanet Discovery Platform by Synapse</p>
            </div>
            <div>
              <h3 class="font-medium mb-2 text-zinc-100">Category</h3>
              <p class="text-zinc-600">Hunting for Exoplanets with AI</p>
            </div>
            <div>
              <h3 class="font-medium mb-2 text-zinc-100">Duration</h3>
              <p class="text-zinc-600">48 Hours Hackathon</p>
            </div>
          </div>
        </div>

        <div>
          <ScrambleText
            trigger="auto"
            :auto-delay="3000"
            :animate-on-mount="true"
            tag="h2"
            class="text-3xl font-bold text-zinc-100 mb-8"
          >
            Meet Our Team
          </ScrambleText>
          <div class="grid md:grid-cols-2">
            <div class="border border-dashed border-r-0 border-zinc-300 p-6 hover:bg-zinc-900 transition-colors">
              <img 
                src="https://media.licdn.com/dms/image/v2/D4E03AQHTYK4oUJmH6w/profile-displayphoto-shrink_400_400/B4EZeayAzcHgAg-/0/1750648492072?e=1762387200&v=beta&t=WvPtyKZLZ72eBbm_iRc84xq6r9QqVFzvMIXmF8W9ehM" 
                alt="Milan G." 
                class="w-16 h-16 rounded-full mb-4 object-cover"
              />
              <ScrambleText
                trigger="hover"
                tag="h3"
                class="font-medium text-lg mb-2 text-zinc-100"
              >
                Milan G.
              </ScrambleText>
              <p class="text-zinc-600 text-sm mb-3">Full-Stack Developer, AI & Project Manager</p>
              <p class="text-xs text-zinc-500">Full-stack developer passionate about space exploration and data visualization. Specializes in Vue.js, Node.js, and astronomical data processing.</p>
            </div>

            <div class="border border-dashed border-zinc-300 p-6 hover:bg-zinc-900 transition-colors">
              <img 
                src="https://media.licdn.com/dms/image/v2/D4D03AQGsONoaf48xcw/profile-displayphoto-shrink_400_400/B4DZhhQaPSHwAg-/0/1753978350464?e=1762387200&v=beta&t=5ThfLuIv2wT9dIVLFD-5WkqVGIqXUE-ApbDoSBxwlDA" 
                alt="Bizhan A." 
                class="w-16 h-16 rounded-full mb-4 object-cover"
              />
              <ScrambleText
                trigger="hover"
                tag="h3"
                class="font-medium text-lg mb-2 text-zinc-100"
              >
                Bizhan A.
              </ScrambleText>
              <p class="text-zinc-600 text-sm mb-3">Backend, AI & Machine Learning</p>
              <p class="text-xs text-zinc-500">UI/UX specialist focused on creating intuitive interfaces for complex astronomical data. Expert in modern web technologies and user experience design.</p>
            </div>
          </div>
        </div>

        <div class="border border-dashed border-zinc-300 border-t-0 p-8 mb-12">
          <ScrambleText
            trigger="auto"
            :auto-delay="4000"
            :animate-on-mount="true"
            tag="h2"
            class="text-2xl font-medium text-zinc-100 text-center mb-6"
          >
            Our Mission
          </ScrambleText>
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
                  <svg class="w-6 h-6 text-zinc-600" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M24.38 19.81h-1.53v3.05h-3.04v1.52h-3.05v1.52h4.57v1.53h1.52v1.52h1.53v1.53h1.52V32h1.53v-1.52h1.52v-1.53h1.52v-1.52H32V25.9h-1.53v-1.52h-1.52v-1.52h-1.52v-1.53H25.9v-4.57h-1.52zm1.52-9.14h1.53v6.09H25.9Zm-1.52-3.05h1.52v3.05h-1.52Zm-1.53-3.05h1.53v3.05h-1.53Zm-1.52 7.62h1.52v3.05h-1.52Zm-1.52-3.05h1.52v3.05h-1.52Zm0-6.09h3.04v1.52h-3.04Zm-3.05 4.57h3.05v1.52h-3.05Zm0-6.1h3.05v1.53h-3.05ZM13.71 6.1h3.05v1.52h-3.05Zm-3.05 19.8h6.1v1.53h-6.1Zm0-25.9h6.1v1.52h-6.1ZM7.62 24.38h3.04v1.52H7.62Zm0-22.86h3.04v1.53H7.62ZM4.57 22.86h3.05v1.52H4.57Zm0-19.81h3.05v1.52H4.57ZM3.05 19.81h1.52v3.05H3.05Zm0-15.24h1.52v3.05H3.05ZM1.52 16.76h1.53v3.05H1.52Zm0-9.14h1.53v3.05H1.52ZM0 10.67h1.52v6.09H0Z"/></svg>
                </div>
                <ScrambleText
                  trigger="hover"
                  tag="h3"
                  class="font-medium mb-2 text-zinc-100"
                >
                  Discover
                </ScrambleText>
                <p class="text-zinc-600">Search through thousands of confirmed exoplanets</p>
              </div>
              <div class="text-center">
                <div class="w-12 h-12 bg-zinc-100 rounded-full mx-auto mb-3 flex items-center justify-center">
                  <svg class="w-6 h-6 text-zinc-600" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M30.48 16.005H32v7.62h-1.52Zm0-9.15H32v4.58h-1.52Zm-1.53 16.77h1.53v1.52h-1.53Zm0-13.72h-1.52v1.53h-1.52v1.52h-1.53v1.52h-1.52v1.53h-1.52v1.52h1.52v1.52h1.52v-1.52h1.53v-1.52h1.52v-1.53h1.52v-1.52h1.53v-1.52h-1.53zm-3.04-4.57h4.57v1.52h-4.57ZM3.05 25.145h25.9v1.52H3.05Zm18.29-19.81h3.04v1.52h-3.04Zm-3.05 13.71v-4.57h-1.53v6.1h6.1v-1.53z"/><path fill="currentColor" d="M19.81 16.005h1.53v-1.53h1.52v-1.52h1.52v-1.52h1.53v-1.53h1.52v-1.52h-1.52v-1.53h-1.53v1.53h-1.52v1.52h-1.52v1.53h-1.53v1.52h-1.52v1.52h1.52zm0-9.15h1.53v1.53h-1.53Zm-1.52 1.53h1.52v1.52h-1.52Zm-3.05 12.19h1.52v1.52h-1.52Zm-4.57 0h1.52v1.52h-1.52Zm-4.57 0h1.52v1.52H6.1Zm-3.05-9.14h13.71v1.52H3.05Zm-1.52 12.19h1.52v1.52H1.53Zm0-10.67h1.52v1.52H1.53ZM0 14.475h1.53v9.15H0Z"/></svg>
                </div>
                <ScrambleText
                  trigger="hover"
                  tag="h3"
                  class="font-medium mb-2 text-zinc-100"
                >
                  Filter
                </ScrambleText>
                <p class="text-zinc-600">Advanced filtering by size, distance, and habitability</p>
              </div>
              <div class="text-center">
                <div class="w-12 h-12 bg-zinc-100 rounded-full mx-auto mb-3 flex items-center justify-center">
                  <svg class="w-6 h-6 text-zinc-600" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M27.43 6.09h-4.57V1.52h1.52V0H3.05v32h25.9V4.57h-1.52Zm0 24.39H4.57V1.52h16.76v6.1h6.1Z"/><path fill="currentColor" d="M25.91 3.05h1.52v1.52h-1.52Zm-1.53-1.53h1.53v1.53h-1.53Zm-3.05 21.34h-1.52v-9.15h-3.05v9.15h-1.52v-6.1h-3.05v6.1H7.62v-3.05h1.52v-1.52H7.62v-3.05h1.52v-1.53H7.62v-3.04H6.1v13.71h19.81v-1.52h-1.53v-7.62h-3.05z"/></svg>
                </div>
                <ScrambleText
                  trigger="hover"
                  tag="h3"
                  class="font-medium mb-2 text-zinc-100"
                >
                  Analyze
                </ScrambleText>
                <p class="text-zinc-600">Visualize data and explore planetary characteristics</p>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center">
          <ScrambleText
            trigger="auto"
            :auto-delay="5000"
            :animate-on-mount="true"
            tag="p"
            class="text-zinc-600 mb-6"
          >
            Ready to explore the cosmos?
          </ScrambleText>
          <div class="flex justify-center gap-4">
            <NuxtLink to="/">
              <Button variant="secondary" size="md">
                <ScrambleText 
                  trigger="hover" 
                  :duration="0.8"
                  scramble-chars="★☆"
                >
                  Start Exploring
                </ScrambleText>
              </Button>
            </NuxtLink>
            <NuxtLink to="https://github.com/themilan1337/exoscout" target="_blank">
              <Button variant="outline" size="md">
                <ScrambleText 
                  trigger="hover" 
                  :duration="0.8"
                  scramble-chars="<>/"
                >
                  View on GitHub
                </ScrambleText>
              </Button>
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
import ScrambleOld from "@/components/ScrambleOld.vue"
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