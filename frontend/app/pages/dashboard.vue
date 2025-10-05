<template>
  <div>
    <Header />
    <div class="min-h-screen bg-black">
      <!-- Main Content -->
      <div class="flex flex-col xl:flex-row">
        <!-- Planet Visualization -->
        <div class="w-full xl:w-1/3 h-64 xl:h-screen border-r border-gray-600 border-dashed relative">
          <div ref="planetContainer" class="w-full h-full"></div>
          <div class="absolute top-4 left-4 text-white">
            <h2 class="text-lg xl:text-xl font-semibold mb-2 text-zinc-100">
              {{ currentTargetId ? `Target: ${currentTargetId}` : (exoplanetData?.name || 'ExoScout Dashboard') }}
            </h2>
            <p class="text-xs xl:text-sm text-zinc-600">{{ exoplanetData?.type || 'AI-Powered Exoplanet Analysis' }}</p>
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
                    class="bg-zinc-800 border border-zinc-600 rounded-md px-4 py-3 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-w-[120px]"
                  >
                    <option value="TESS">TESS</option>
                    <option value="KEPLER">KEPLER</option>
                    <option value="K2">K2</option>
                  </select>
                  <input
                    v-model="targetInput"
                    @keyup.enter="analyzeTarget"
                    type="text"
                    placeholder="Enter Target ID (e.g., 123456789) or use Target Resolver below"
                    class="flex-1 px-4 py-3 bg-zinc-800 border border-zinc-600 rounded-md text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              <Button
                @click="analyzeTarget"
                :disabled="!targetInput.trim() || isAnalyzing"
              >
                <span v-if="isAnalyzing" class="flex items-center gap-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Analyzing...
                </span>
                <span v-else>Analyze Target</span>
              </Button>
            </div>
          </div>

          <!-- Tabs for different sections -->
          <div class="mb-6">
            <div class="flex flex-wrap gap-2 border-b border-zinc-700">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'px-4 py-2 text-sm font-medium transition-colors',
                  activeTab === tab.id
                    ? 'text-blue-400 border-b-2 border-blue-400'
                    : 'text-zinc-400 hover:text-zinc-200'
                ]"
              >
                {{ tab.label }}
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
                <p class="text-zinc-400">Enter a target ID above to start AI analysis</p>
              </div>
            </div>

            <!-- Lightcurve Tab -->
            <div v-if="activeTab === 'lightcurve'">
              <LightcurveChart
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
                <p class="text-zinc-400">Enter a target ID above to view lightcurve data</p>
              </div>
            </div>

            <!-- Target Resolver Tab -->
            <div v-if="activeTab === 'resolver'">
              <TargetResolver
                @target-selected="onTargetSelected"
                @error="onError"
              />
            </div>

            <!-- Legacy Planet Info Tab -->
            <div v-if="activeTab === 'info' && exoplanetData" class="space-y-6">
              <div>
                <h1 class="text-3xl font-bold text-white mb-2">{{ exoplanetData.name }}</h1>
                <p class="text-lg text-zinc-600">{{ exoplanetData.type }}</p>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-4">
                  <div class="bg-zinc-900 p-4 rounded-lg">
                    <h3 class="font-semibold text-zinc-100 mb-2">Physical Properties</h3>
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
                    <h3 class="font-semibold text-zinc-100 mb-2">Discovery Info</h3>
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
                    <h3 class="font-semibold text-zinc-100 mb-2">Search Details</h3>
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
                    <h3 class="font-semibold text-zinc-100 mb-2">About This Visualization</h3>
                    <p class="text-sm text-zinc-500">
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
            
            <div v-else-if="activeTab === 'info'" class="flex items-center justify-center h-64">
              <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-zinc-900 mx-auto mb-4"></div>
                <p class="text-zinc-600">Generating exoplanet...</p>
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
import LightcurveChart from '@/components/LightcurveChart.vue'
import TargetResolver from '@/components/TargetResolver.vue'
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

// Tab configuration
const tabs = [
  { id: 'prediction', label: 'AI Prediction' },
  { id: 'lightcurve', label: 'Lightcurve Data' },
  { id: 'resolver', label: 'Target Resolver' },
  { id: 'info', label: 'Planet Info' }
]

let cleanupPlanet: (() => void) | null = null

const { generatePlanetParams, generateExoplanetData, createPlanet, setupPlanetScene } = usePlanetGenerator()
const { detectMission } = useExoScoutAPI()

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

const onTargetSelected = (mission: Mission, targetId: string, targetData: any) => {
  currentTargetId.value = targetId
  currentMission.value = mission
  targetInput.value = targetId
  activeTab.value = 'prediction'
}

const onPredictionComplete = (prediction: any) => {
  console.log('Prediction completed:', prediction)
  // You can add additional logic here if needed
}

const onLightcurveLoaded = (data: any) => {
  console.log('Lightcurve data loaded:', data)
  // You can add additional logic here if needed
}

const onError = (message: string) => {
  console.error('Error:', message)
  // Error is logged to console - consider implementing a proper notification system
}

onMounted(() => {
  // Initialize planet with delay
  setTimeout(initializePlanet, 100)
  
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