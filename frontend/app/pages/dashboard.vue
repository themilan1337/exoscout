<template>
  <div>
    <Header />
    <div class="flex flex-col lg:flex-row h-[calc(100vh-1.8rem)]">
      <div class="w-full lg:w-1/2 h-64 lg:h-full border-b lg:border-b-0 lg:border-r border-zinc-300 border-dashed relative bg-white">
        <div ref="planetContainer" class="w-full h-full"></div>
        <div class="absolute top-4 left-4 text-black">
          <h2 class="text-lg lg:text-xl font-semibold mb-2">{{ exoplanetData?.name || 'Loading...' }}</h2>
          <p class="text-xs lg:text-sm text-zinc-600">{{ exoplanetData?.type || '' }}</p>
        </div>
      </div>
      
      <div class="w-full lg:w-1/2 p-4 lg:p-8 overflow-y-auto flex-1">
        <div v-if="exoplanetData" class="space-y-6">
          <div>
            <h1 class="text-3xl font-bold text-zinc-900 mb-2">{{ exoplanetData.name }}</h1>
            <p class="text-lg text-zinc-600">{{ exoplanetData.type }}</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <div class="bg-zinc-50 p-4 rounded-lg">
                <h3 class="font-semibold text-zinc-900 mb-2">Physical Properties</h3>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Mass:</span>
                    <span class="font-medium">{{ exoplanetData.mass }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Radius:</span>
                    <span class="font-medium">{{ exoplanetData.radius }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Temperature:</span>
                    <span class="font-medium">{{ exoplanetData.temperature }}</span>
                  </div>
                </div>
              </div>
              
              <div class="bg-zinc-50 p-4 rounded-lg">
                <h3 class="font-semibold text-zinc-900 mb-2">Discovery Info</h3>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Discovery Year:</span>
                    <span class="font-medium">{{ exoplanetData.discoveryYear }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Host Star:</span>
                    <span class="font-medium">{{ exoplanetData.hostStar }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Distance:</span>
                    <span class="font-medium">{{ exoplanetData.distance }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="space-y-4">
              <div class="bg-zinc-50 p-4 rounded-lg">
                <h3 class="font-semibold text-zinc-900 mb-2">Search Details</h3>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Search ID:</span>
                    <span class="font-medium">{{ exoplanetData.id }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-zinc-600">Status:</span>
                    <span class="font-medium text-green-600">Found</span>
                  </div>
                </div>
              </div>
              
              <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h3 class="font-semibold text-blue-900 mb-2">About This Visualization</h3>
                <p class="text-sm text-blue-700">
                  This 3D planet is procedurally generated based on your search ID. 
                  The terrain, colors, and atmospheric conditions are simulated to 
                  represent what this exoplanet might look like.
                </p>
              </div>
            </div>
          </div>
          
          <div class="flex gap-4 pt-4">
            <Button @click="regeneratePlanet" variant="primary">
              Regenerate Planet
            </Button>
            <Button 
              variant="secondary"
              @click="$router.push('/')"
            >
              Search Another
            </Button>
          </div>
        </div>
        
        <div v-else class="flex items-center justify-center h-full">
          <div class="text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-zinc-900 mx-auto mb-4"></div>
            <p class="text-zinc-600">Generating exoplanet...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Header from '@/components/layout/Header.vue'
import Button from '@/components/ui/Button.vue'
import { usePlanetGenerator, type ExoplanetData } from '@/composables/usePlanetGenerator'

const route = useRoute()
const planetContainer = ref<HTMLElement>()
const exoplanetData = ref<ExoplanetData | null>(null)

let cleanupPlanet: (() => void) | null = null

const { generatePlanetParams, generateExoplanetData, createPlanet, setupPlanetScene } = usePlanetGenerator()

const initializePlanet = () => {
  const searchId = route.query.id as string || '12345'
  
  exoplanetData.value = generateExoplanetData(searchId)
  
  if (planetContainer.value) {
    const planetParams = generatePlanetParams(searchId)
    const planet = createPlanet(planetParams)
    cleanupPlanet = setupPlanetScene(planetContainer.value, planet)
  }
}

const regeneratePlanet = () => {
  if (cleanupPlanet) {
    cleanupPlanet()
  }
  
  const randomId = Math.floor(Math.random() * 999999).toString()
  exoplanetData.value = generateExoplanetData(randomId)
  
  if (planetContainer.value) {
    const planetParams = generatePlanetParams(randomId)
    const planet = createPlanet(planetParams)
    cleanupPlanet = setupPlanetScene(planetContainer.value, planet)
  }
}

onMounted(() => {
  //delay1s
  setTimeout(initializePlanet, 100)
})

onUnmounted(() => {
  if (cleanupPlanet) {
    cleanupPlanet()
  }
})
</script>