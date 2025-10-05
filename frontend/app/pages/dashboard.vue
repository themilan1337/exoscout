<template>
  <div>
    <Header />
    <div class="min-h-screen bg-black">
      <!-- Main Content -->
      <div class="flex flex-col xl:flex-row">
        <!-- Planet Visualization -->
        <div class="w-full xl:w-1/3 h-64 xl:h-screen border-r border-b border-gray-600 border-dashed relative">
          <!-- Show planet only if we have successful data from backend -->
          <div v-if="hasSuccessfulBackendData" ref="planetContainer" class="w-full h-full"></div>
          
          <!-- Zoom Controls -->
          <div v-if="hasSuccessfulBackendData" class="absolute top-4 right-4 flex flex-col gap-2 z-10">
            <button 
              @click="zoomIn"
              class="bg-zinc-800/90 hover:bg-zinc-700/90 active:bg-zinc-600/90 border border-zinc-600 hover:border-zinc-500 rounded-lg p-3 text-zinc-300 hover:text-white transition-all duration-200 backdrop-blur-sm shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/50 cursor-pointer"
              title="Zoom In"
              aria-label="Zoom in on planet"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32" class="w-5 h-5">
                <path fill="currentColor" d="M23.62 20.57H22.1v1.52h-1.53v1.53h-3.04v1.52h3.04v1.52h1.53v1.53h1.52v1.52h1.52v1.53h4.58v-1.53h1.52v-4.57h-1.52v-1.52h-1.53v-1.53h-1.52v-1.52h-1.53v-3.05h-1.52Zm1.52 3.05h1.53v1.52h1.52v1.52h1.53v1.53h-1.53v-1.53h-1.52v-1.52h-1.53Zm0-13.72h1.53v7.62h-1.53Zm-1.52-3.05h1.52V9.9h-1.52ZM22.1 5.33h1.52v1.52H22.1Zm-1.53-1.52h1.53v1.52h-1.53Zm-9.14 16.76H16V16h4.57v-4.57H16V6.85h-4.57v4.58H6.86V16h4.57zm6.1-18.29h3.04v1.53h-3.04ZM9.91 25.14h7.62v1.52H9.91Zm0-24.38h7.62v1.52H9.91ZM6.86 23.62h3.05v1.52H6.86Zm0-21.34h3.05v1.53H6.86ZM5.34 22.09h1.52v1.53H5.34Zm0-18.28h1.52v1.52H5.34ZM3.81 20.57h1.53v1.52H3.81Zm0-15.24h1.53v1.52H3.81ZM2.29 17.52h1.52v3.05H2.29Zm0-10.67h1.52V9.9H2.29ZM.76 9.9h1.53v7.62H.76Z"/>
              </svg>
            </button>
            <button 
              @click="zoomOut"
              class="bg-zinc-800/90 hover:bg-zinc-700/90 active:bg-zinc-600/90 border border-zinc-600 hover:border-zinc-500 rounded-lg p-3 text-zinc-300 hover:text-white transition-all duration-200 backdrop-blur-sm shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/50 cursor-pointer"
              title="Zoom Out"
              aria-label="Zoom out on planet"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32" class="w-5 h-5">
                <path fill="currentColor" d="M23.62 20.57H22.1v1.52h-1.53v1.53h-3.04v1.52h3.04v1.52h1.53v1.53h1.52v1.52h1.52v1.53h4.58v-1.53h1.52v-4.57h-1.52v-1.52h-1.53v-1.53h-1.52v-1.52h-1.53v-3.05h-1.52Zm1.52 3.05h1.53v1.52h1.52v1.52h1.53v1.53h-1.53v-1.53h-1.52v-1.52h-1.53Zm0-13.72h1.53v7.62h-1.53Zm-1.52-3.05h1.52V9.9h-1.52ZM22.1 5.33h1.52v1.52H22.1Zm-1.53-1.52h1.53v1.52h-1.53ZM6.86 11.43h13.71V16H6.86Zm10.67-9.15h3.04v1.53h-3.04ZM9.91 25.14h7.62v1.52H9.91Zm0-24.38h7.62v1.52H9.91ZM6.86 23.62h3.05v1.52H6.86Zm0-21.34h3.05v1.53H6.86ZM5.34 22.09h1.52v1.53H5.34Zm0-18.28h1.52v1.52H5.34ZM3.81 20.57h1.53v1.52H3.81Zm0-15.24h1.53v1.52H3.81ZM2.29 17.52h1.52v3.05H2.29Zm0-10.67h1.52V9.9H2.29ZM.76 9.9h1.53v7.62H.76Z"/>
              </svg>
            </button>
          </div>
          
          <!-- Placeholder when no backend data -->
          <div v-else class="w-full h-full flex items-center justify-center">
            <div class="text-center px-8">
              <svg class="w-20 h-20 text-zinc-600 mx-auto mb-6" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M24.38 19.81h-1.53v3.05h-3.04v1.52h-3.05v1.52h4.57v1.53h1.52v1.52h1.53v1.53h1.52V32h1.53v-1.52h1.52v-1.53h1.52v-1.52H32V25.9h-1.53v-1.52h-1.52v-1.52h-1.52v-1.53H25.9v-4.57h-1.52zm1.52-9.14h1.53v6.09H25.9Zm-1.52-3.05h1.52v3.05h-1.52Zm-1.53-3.05h1.53v3.05h-1.53Zm-1.52 7.62h1.52v3.05h-1.52Zm-1.52-3.05h1.52v3.05h-1.52Zm0-6.09h3.04v1.52h-3.04Zm-3.05 4.57h3.05v1.52h-3.05Zm0-6.1h3.05v1.53h-3.05ZM13.71 6.1h3.05v1.52h-3.05Zm-3.05 19.8h6.1v1.53h-6.1Zm0-25.9h6.1v1.52h-6.1ZM7.62 24.38h3.04v1.52H7.62Zm0-22.86h3.04v1.53H7.62ZM4.57 22.86h3.05v1.52H4.57Zm0-19.81h3.05v1.52H4.57ZM3.05 19.81h1.52v3.05H3.05Zm0-15.24h1.52v3.05H3.05ZM1.52 16.76h1.53v3.05H1.52Zm0-9.14h1.53v3.05H1.52ZM0 10.67h1.52v6.09H0Z"/></svg>
              <ScrambleText 
                tag="h3" 
                trigger="auto" 
                :auto-delay="3000" 
                :animate-on-mount="true"
                class="text-xl font-semibold text-zinc-100 mb-2"
              >
                Discover Exoplanets
              </ScrambleText>
              <ScrambleText 
                trigger="hover" 
                class="text-zinc-400 text-sm mb-4"
              >
                Enter a planet ID above to start exploring
              </ScrambleText>
              <ScrambleText 
                trigger="hover" 
                class="text-zinc-600 text-xs"
              >
                3D planet visualization will appear after successful discovery
              </ScrambleText>
            </div>
          </div>
          
          <div class="absolute top-4 left-4 text-white">
            <ScrambleText 
              tag="h2" 
              trigger="hover" 
              class="text-lg xl:text-xl font-semibold mb-2 text-zinc-100 flex"
            >
              <svg class="mr-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M22.85 7.62v3.05h-1.52v4.57h1.52v1.52h1.53v1.53h-4.57v1.52h-1.53v1.52h4.57v3.05h-1.52v3.05h1.52v1.52h3.05v-1.52h1.53V25.9h1.52v-3.04h1.52v-3.05H32v-7.62h-1.53V9.14h-1.52V6.1h-1.52v1.52zm3.05-3.05h1.53V6.1H25.9Zm-3.05-1.52h3.05v1.52h-3.05Z"/><path fill="currentColor" d="M19.81 28.95h3.04v1.53h-3.04Zm0-27.43h3.04v1.53h-3.04Z"/><path fill="currentColor" d="M16.76 28.95h-1.52v-1.52h-4.58v1.52H9.14v1.53h3.05V32h7.62v-1.52h-3.05zM12.19 0h7.62v1.52h-7.62Zm-1.53 16.76h1.53v1.53h1.52v-4.58h-3.05zM6.09 27.43h3.05v1.52H6.09ZM4.57 25.9h1.52v1.53H4.57Z"/><path fill="currentColor" d="M3.05 22.86v3.04h1.52v-1.52h1.52v-1.52h1.53v-4.57H6.09v-1.53H4.57v-1.52H3.05v-1.53h1.52v-1.52h4.57v-1.52h1.52V9.14h1.53v1.53h1.52V9.14h1.53V6.1h-1.53V4.57h-3.05V3.05h1.53V1.52H9.14v1.53H6.09v1.52H4.57V6.1H3.05v3.04H1.52v3.05H0v7.62h1.52v3.05z"/></svg>
              <span class="my-auto">{{ currentTargetId ? `Target: ${currentTargetId}` : (exoplanetData?.name || 'ExoScout Dashboard') }}</span>
            </ScrambleText>
            <ScrambleText 
              trigger="hover" 
              class="text-xs xl:text-sm text-zinc-600"
            >
              {{ exoplanetData?.type || 'AI-Powered Exoplanet Analysis' }}
            </ScrambleText>
          </div>
        </div>
        
        <!-- Analysis Panel -->
        <div class="w-full xl:w-2/3 p-4 xl:p-8 overflow-y-auto">
          <!-- Target Input Section -->
          <div class="mb-8">
            <div class="flex flex-col sm:flex-row gap-4 mb-4">
              <div class="flex-1">
                <div class="flex gap-3">
                  <select
                    v-model="currentMission"
                    class="bg-zinc-800 border border-zinc-600 rounded-md px-4 py-3 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:border-transparent min-w-[120px]"
                  >
                    <option value="TESS">TESS</option>
                    <option value="KEPLER">KEPLER</option>
                    <option value="K2">K2</option>
                  </select>
                  <input
                    v-model="targetInput"
                    @keyup.enter="analyzeTarget"
                    type="text"
                    placeholder="Enter Target ID (e.g., 123456789)"
                    class="flex-1 px-4 py-3 bg-zinc-800 border border-zinc-600 rounded-md text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  />
                </div>
              </div>
              <Button
                @click="analyzeTarget"
                :disabled="!targetInput.trim() || isAnalyzing"
              >
                <span v-if="isAnalyzing" class="flex items-center gap-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <ScrambleText trigger="auto" :auto-delay="1000">Analyzing...</ScrambleText>
                </span>
                <ScrambleText v-else trigger="hover">Analyze Target</ScrambleText>
              </Button>
            </div>
          </div>

          <!-- Tabs for different sections - only show relevant tabs based on data availability -->
          <div class="mb-6">
            <div class="flex flex-wrap gap-2 border-b border-zinc-700">
              <button
                v-for="tab in availableTabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'px-4 py-2 text-sm font-medium transition-colors',
                  activeTab === tab.id
                    ? 'text-zinc-400 border-b-2 border-zinc-400'
                    : 'text-zinc-400 hover:text-zinc-200'
                ]"
              >
                <ScrambleText 
                  trigger="hover" 
                  :duration="0.8"
                >
                  {{ tab.label }}
                </ScrambleText>
              </button>
            </div>
          </div>

          <!-- Tab Content -->
          <div class="space-y-6">
            <!-- AI Prediction Tab -->
            <div v-if="activeTab === 'prediction'">
              <ExoplanetPrediction
                v-if="currentTargetId"
                :target-id="currentTargetId"
                :mission="currentMission"
                @prediction-complete="onPredictionComplete"
                @error="onError"
              />
              <div v-else class="text-center py-12">
                <svg class="w-16 h-16 text-zinc-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <ScrambleText 
                  trigger="auto" 
                  :auto-delay="4000" 
                  :animate-on-mount="true"
                  class="text-zinc-400"
                >
                  Enter a target ID above to start AI analysis
                </ScrambleText>
              </div>
            </div>

            <!-- Lightcurve Tab -->
            <div v-if="activeTab === 'lightcurve'">
              <ApexLightcurveChart
                v-if="currentTargetId"
                :target-id="currentTargetId"
                :mission="currentMission"
                @data-loaded="onLightcurveLoaded"
                @error="onError"
              />
              <div v-else class="text-center py-12">
                <svg class="w-16 h-16 text-zinc-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <ScrambleText 
                  trigger="auto" 
                  :auto-delay="5000" 
                  :animate-on-mount="true"
                  class="text-zinc-400"
                >
                  Enter a target ID above to view lightcurve data
                </ScrambleText>
              </div>
            </div>



            <!-- Legacy Planet Info Tab - only show when we have backend data -->
            <div v-if="activeTab === 'info' && hasSuccessfulBackendData && exoplanetData" class="space-y-6">
              <div>
                <ScrambleText 
                  trigger="auto" 
                  :auto-delay="1000" 
                  :animate-on-mount="true"
                  tag="h1"
                  class="text-3xl font-bold text-white mb-2"
                >
                  {{ exoplanetData.name }}
                </ScrambleText>
                <ScrambleText 
                  trigger="hover" 
                  tag="p"
                  class="text-lg text-zinc-600"
                >
                  {{ exoplanetData.type }}
                </ScrambleText>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-4">
                  <div class="bg-zinc-900 p-4 rounded-lg">
                    <ScrambleText 
                      trigger="hover" 
                      tag="h3"
                      class="font-semibold text-zinc-100 mb-2"
                    >
                      Physical Properties
                    </ScrambleText>
                    <div class="space-y-2 text-sm">
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Mass:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.mass }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Radius:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.radius }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Temperature:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.temperature }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="bg-zinc-900 p-4 rounded-lg">
                    <ScrambleText 
                      trigger="hover" 
                      tag="h3"
                      class="font-semibold text-zinc-100 mb-2"
                    >
                      Discovery Info
                    </ScrambleText>
                    <div class="space-y-2 text-sm">
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Discovery Year:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.discoveryYear }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Host Star:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.hostStar }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Distance:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.distance }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="space-y-4">
                  <div class="bg-zinc-900 p-4 rounded-lg">
                    <ScrambleText 
                      trigger="hover" 
                      tag="h3"
                      class="font-semibold text-zinc-100 mb-2"
                    >
                      Search Details
                    </ScrambleText>
                    <div class="space-y-2 text-sm">
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Search ID:</span>
                        <span class="font-medium text-zinc-100">{{ exoplanetData.id }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-zinc-600">Status:</span>
                        <span class="font-medium text-green-600">Found</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="bg-zinc-900 p-4 rounded-lg">
                    <ScrambleText 
                      trigger="hover" 
                      tag="h3"
                      class="font-semibold text-zinc-100 mb-2"
                    >
                      About This Visualization
                    </ScrambleText>
                    <ScrambleText 
                      trigger="auto" 
                      :auto-delay="6000" 
                      tag="p"
                      class="text-sm text-zinc-500"
                    >
                      This 3D planet is procedurally generated based on your search ID. 
                      The terrain, colors, and atmospheric conditions are simulated to 
                      represent what this exoplanet might look like.
                    </ScrambleText>
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import Header from '@/components/layout/Header.vue'
import Button from '@/components/ui/Button.vue'
import ExoplanetPrediction from '@/components/ExoplanetPrediction.vue'
import ApexLightcurveChart from '@/components/ApexLightcurveChart.vue'
import ScrambleText from '@/components/ScrambleText.vue'

import { usePlanetGenerator, type ExoplanetData } from '@/composables/usePlanetGenerator'
import { useExoScoutAPI, type Mission } from '@/composables/useExoScoutAPI'

const route = useRoute()
const planetContainer = ref<HTMLElement>()
const exoplanetData = ref<ExoplanetData | null>(null)

// Backend integration state
const targetInput = ref('')
const currentTargetId = ref<string>('')
const currentMission = ref<Mission>('TESS')
const isAnalyzing = ref(false)
const activeTab = ref('prediction')

// Track if we have successful backend data
const hasSuccessfulBackendData = ref(false)
const hasSuccessfulPrediction = ref(false)
const hasSuccessfulLightcurve = ref(false)

// Store prediction data for planet visualization
const predictionData = ref<any>(null)

// Tab configuration - computed to show only relevant tabs
const allTabs = [
  { id: 'prediction', label: 'AI Prediction' },
  { id: 'lightcurve', label: 'Lightcurve Data' },
  { id: 'info', label: 'Planet Info' }
]

const availableTabs = computed(() => {
  // Always show prediction and lightcurve tabs
  const baseTabs = allTabs.filter(tab => ['prediction', 'lightcurve'].includes(tab.id))
  
  // Only show info tab if we have successful backend data
  if (hasSuccessfulBackendData.value) {
    baseTabs.push(allTabs.find(tab => tab.id === 'info')!)
  }
  
  return baseTabs
})

let cleanupPlanet: (() => void) | null = null
let planetZoomControls: { zoomIn: () => void; zoomOut: () => void } | null = null

const { generatePlanetParams, generateExoplanetData, createPlanet, setupPlanetScene } = usePlanetGenerator()
const { detectMission } = useExoScoutAPI()

const initializePlanet = () => {
  if (!hasSuccessfulBackendData.value) return
  
  const searchId = route.query.id as string || currentTargetId.value || '12345'
  
  exoplanetData.value = generateExoplanetData(searchId)
  
  if (planetContainer.value) {
    // Pass prediction data to generate appropriate planet type
    const planetParams = generatePlanetParams(searchId, predictionData.value)
    const planet = createPlanet(planetParams)
    const sceneResult = setupPlanetScene(planetContainer.value, planet)
    cleanupPlanet = sceneResult.cleanup
    planetZoomControls = sceneResult.zoomControls
  }
}

// Zoom control functions
const zoomIn = () => {
  if (planetZoomControls) {
    planetZoomControls.zoomIn()
  }
}

const zoomOut = () => {
  if (planetZoomControls) {
    planetZoomControls.zoomOut()
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
    const sceneResult = setupPlanetScene(planetContainer.value, planet)
    cleanupPlanet = sceneResult.cleanup
    planetZoomControls = sceneResult.zoomControls
  }
}

// Backend integration methods
const analyzeTarget = async () => {
  if (!targetInput.value.trim()) return
  
  isAnalyzing.value = true
  try {
    currentTargetId.value = targetInput.value.trim()
    
    // Use the selected mission instead of auto-detecting
    // currentMission.value is already set by the dropdown
    
    // Switch to prediction tab to show results
    activeTab.value = 'prediction'
  } catch (error) {
    console.error('Error analyzing target:', error)
    onError('Failed to analyze target. Please check the target ID and try again.')
  } finally {
    isAnalyzing.value = false
  }
}



const onPredictionComplete = (prediction: any) => {
  console.log('Prediction completed:', prediction)
  predictionData.value = prediction
  hasSuccessfulPrediction.value = true
  
  // Mark as having successful backend data when we get a prediction
  if (!hasSuccessfulBackendData.value) {
    hasSuccessfulBackendData.value = true
    // Initialize planet after successful data fetch
    setTimeout(() => {
      initializePlanet()
    }, 100)
  } else {
    // If planet already exists, reinitialize it with new prediction data
    setTimeout(() => {
      if (cleanupPlanet) {
        cleanupPlanet()
        cleanupPlanet = null
      }
      initializePlanet()
    }, 100)
  }
}

const onLightcurveLoaded = (data: any) => {
  console.log('Lightcurve data loaded:', data)
  hasSuccessfulLightcurve.value = true
  
  // Mark as having successful backend data when we get lightcurve data
  if (!hasSuccessfulBackendData.value) {
    hasSuccessfulBackendData.value = true
    // Initialize planet after successful data fetch
    setTimeout(() => {
      initializePlanet()
    }, 100)
  }
}

const onError = (message: string) => {
  console.error('Error:', message)
  // Reset backend data states when error occurs
  hasSuccessfulBackendData.value = false
  hasSuccessfulPrediction.value = false
  hasSuccessfulLightcurve.value = false
  predictionData.value = null
  
  // Cleanup planet visualization if it exists
  if (cleanupPlanet) {
    cleanupPlanet()
    cleanupPlanet = null
  }
}

onMounted(() => {
  // Don't initialize planet immediately - wait for backend data
  
  // Check if there's a target ID in the route query (support both 'id' and 'target' parameters)
  const routeTargetId = (route.query.id as string) || (route.query.target as string)
  const routeMission = route.query.mission as string
  
  if (routeTargetId) {
    targetInput.value = routeTargetId
    
    // Set mission if provided in query
    if (routeMission && ['TESS', 'KEPLER', 'K2'].includes(routeMission)) {
      currentMission.value = routeMission as any
    }
    
    analyzeTarget()
  }
})

onUnmounted(() => {
  if (cleanupPlanet) {
    cleanupPlanet()
  }
})
</script>