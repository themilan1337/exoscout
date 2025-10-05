<template>
  <div class="particles-container">
    <Particles
      :particle-count="200"
      :particle-spread="10"
      :speed="0.1"
      :particle-colors="['#fff']"
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
      <ScrambleOld
        trigger="auto"
        :auto-delay="1000"
        :animate-on-mount="true"
        :duration="1.2" 
        :speed="0.5" 
        scramble-chars=".:"
        class="max-w-5xl text-4xl text-pretty mx-auto mt-24 leading-tight text-center font-medium text-zinc-100"
      >
        Discover Exoplanets.<br>
        Your gateway to real data from NASA's <br> archives—search, filter, and explore <br> worlds beyond our solar <br> system in seconds.
      </ScrambleOld>
      <div class="flex flex-col sm:flex-row mx-auto justify-center items-center mt-8 gap-2 px-4">
        <select
          v-model="selectedMission"
          class="bg-zinc-900 border border-zinc-700 rounded-md px-4 py-1 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:border-transparent min-w-[120px] text-sm"
        >
          <option value="">{{ isLoadingMissions ? 'Loading...' : 'Select Mission' }}</option>
          <option v-for="mission in availableMissions" :key="mission" :value="mission">
            {{ mission }}
          </option>
        </select>
        <Input 
          v-model="exoplanetId" 
          placeholder="Enter ID" 
          type="number" 
          variant="secondary" 
          size="sm" 
          class="w-full sm:w-auto sm:mr-2"
          @keyup.enter="searchExoplanet" 
        />
        <Button 
          variant="secondary" 
          size="sm" 
          @click="searchExoplanet"
          :disabled="!exoplanetId || !exoplanetId?.trim() || !selectedMission"
          class="w-full sm:w-auto"
        >
          <ScrambleText 
            trigger="hover" 
            :duration="0.8"
            :speed="0.7"
            scramble-chars="01"
          >
            Find some planets
          </ScrambleText>
        </Button>
      </div>
      
      <!-- Test Examples Section -->
      <div class="max-w-4xl mx-auto mt-12 px-4">
        <div class="text-center mb-6">
          <ScrambleText 
            trigger="hover" 
            :duration="0.8"
            scramble-chars="▓░"
            class="text-zinc-400 text-sm font-medium"
          >
            Try these examples *those are clickable*
          </ScrambleText>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <!-- TESS Examples -->
          <div class="space-y-2">
            <h3 class="text-zinc-500 text-xs font-medium uppercase tracking-wider">TESS</h3>
            <div class="space-y-1">
              <button 
                v-for="example in tessExamples" 
                :key="example.id"
                @click="selectExample('TESS', example.id)"
                class="w-full text-left px-3 py-2 bg-zinc-900/50 border border-zinc-800 rounded-md text-zinc-300 text-sm hover:bg-zinc-800/50 hover:border-zinc-700 transition-all duration-200 hover:text-zinc-100"
              >
                <ScrambleText 
                  trigger="hover" 
                  :duration="0.6"
                  scramble-chars="01"
                >
                  {{ example.id }}
                </ScrambleText>
              </button>
            </div>
          </div>
          
          <!-- KEPLER Examples -->
          <div class="space-y-2">
            <h3 class="text-zinc-500 text-xs font-medium uppercase tracking-wider">KEPLER</h3>
            <div class="space-y-1">
              <button 
                v-for="example in keplerExamples" 
                :key="example.id"
                @click="selectExample('KEPLER', example.id)"
                class="w-full text-left px-3 py-2 bg-zinc-900/50 border border-zinc-800 rounded-md text-zinc-300 text-sm hover:bg-zinc-800/50 hover:border-zinc-700 transition-all duration-200 hover:text-zinc-100"
              >
                <ScrambleText 
                  trigger="hover" 
                  :duration="0.6"
                  scramble-chars="01"
                >
                  {{ example.id }}
                </ScrambleText>
              </button>
            </div>
          </div>
          
          <!-- K2 Examples -->
          <div class="space-y-2">
            <h3 class="text-zinc-500 text-xs font-medium uppercase tracking-wider">K2</h3>
            <div class="space-y-1">
              <button 
                v-for="example in k2Examples" 
                :key="example.id"
                @click="selectExample('K2', example.id)"
                class="w-full text-left px-3 py-2 bg-zinc-900/50 border border-zinc-800 rounded-md text-zinc-300 text-sm hover:bg-zinc-800/50 hover:border-zinc-700 transition-all duration-200 hover:text-zinc-100"
              >
                <ScrambleText 
                  trigger="hover" 
                  :duration="0.6"
                  scramble-chars="01"
                >
                  {{ example.id }}
                </ScrambleText>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="flex mx-auto justify-center gap-x-4 items-center mt-12">
        <NuxtLink to="/team" class="text-zinc-600 text-sm">
          <ScrambleText 
            trigger="hover" 
            :duration="0.6"
            scramble-chars="▓░"
          >
            Our Team<span class="inline-block ml-1">↗</span>
          </ScrambleText>
        </NuxtLink>
        <NuxtLink to="https://github.com/themilan1337/exoscout" class="text-zinc-600 text-sm">
          <ScrambleText 
            trigger="hover" 
            :duration="0.6"
            scramble-chars="▓░"
          >
            GitHub<span class="inline-block ml-1 my-auto">↗</span>
          </ScrambleText>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Header from '@/components/layout/Header.vue'
import ScrambleText from "@/components/ScrambleText.vue";
import ScrambleOld from "@/components/ScrambleOld.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Particles from "@/components/Particles.vue";
import { useExoScoutAPI } from '@/composables/useExoScoutAPI'

const exoplanetId = ref<string>('')
const selectedMission = ref('')
const availableMissions = ref<string[]>([])
const isLoadingMissions = ref(false)

const { getAvailableMissions } = useExoScoutAPI()

// Test examples data
const tessExamples = ref([
  { id: '307210830' },
  { id: '50365310' },
])

const keplerExamples = ref([
  { id: '10666592' },
  { id: '11446443' }
])

const k2Examples = ref([
  { id: '206103150' },
  { id: '201367065' },
])

// Function to select an example and populate the form
const selectExample = (mission: string, id: string) => {
  selectedMission.value = mission
  exoplanetId.value = id
}

// Load available missions on component mount
const loadAvailableMissions = async () => {
  isLoadingMissions.value = true
  try {
    availableMissions.value = await getAvailableMissions()
    // Set default mission to TESS if available
    if (availableMissions.value.includes('TESS')) {
      selectedMission.value = 'TESS'
    } else if (availableMissions.value.length > 0 && availableMissions.value[0]) {
      selectedMission.value = availableMissions.value[0]
    }
  } catch (err: any) {
    console.error('Failed to load available missions:', err.message)
  } finally {
    isLoadingMissions.value = false
  }
}

const searchExoplanet = async () => {
  const trimmedId = exoplanetId.value?.trim()
  if (trimmedId && trimmedId !== '' && selectedMission.value) {
    // Navigate to dashboard with both mission and target ID
    await navigateTo({
      path: '/dashboard',
      query: { 
        id: trimmedId,
        mission: selectedMission.value
      }
    })
  }
}



// Load missions on component mount
onMounted(() => {
  loadAvailableMissions()
})
</script>
<style scoped>
.particles-container {
    width: 100%;
    height: 100vh;
    position: relative;
    overflow: hidden;
  }
</style>