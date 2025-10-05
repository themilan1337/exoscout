<template>
  <div class="space-y-4">
    <!-- Input Section -->
    <div class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <h3 class="text-lg font-medium text-zinc-100 mb-4">Target Name Resolution</h3>
      
      <!-- Mission Selection -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-zinc-300 mb-2">Mission</label>
        <select
          v-model="selectedMission"
          class="w-full bg-zinc-800 border border-zinc-600 rounded-lg px-4 py-2 text-zinc-100 focus:outline-none focus:border-zinc-500"
          :disabled="isLoadingMissions"
        >
          <option value="">{{ isLoadingMissions ? 'Loading missions...' : 'Select a mission' }}</option>
          <option v-for="mission in availableMissions" :key="mission" :value="mission">
            {{ mission }}
          </option>
        </select>
      </div>
      
      <div class="flex gap-3">
        <input
          v-model="inputName"
          type="text"
          placeholder="Enter target name (e.g., TOI-715, HD 209458)"
          class="flex-1 bg-zinc-800 border border-zinc-600 rounded-lg px-4 py-2 text-zinc-100 placeholder-zinc-400 focus:outline-none focus:border-zinc-500"
          @keyup.enter="resolveTarget"
        />
        <button
          @click="resolveTarget"
          :disabled="isLoading || !inputName.trim() || !selectedMission"
          class="bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:text-zinc-500 text-zinc-100 px-6 py-2 rounded-lg transition-colors"
        >
          {{ isLoading ? 'Resolving...' : 'Resolve' }}
        </button>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="resolvedData" class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-lg font-semibold text-zinc-100">Resolution Results</h4>
        <div class="flex items-center gap-2">
          <div 
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              resolvedData.status === 'success' 
                ? 'bg-green-900 text-green-300 border border-green-700' 
                : 'bg-yellow-900 text-yellow-300 border border-yellow-700'
            ]"
          >
            {{ resolvedData.status }}
          </div>
          <div class="text-sm text-zinc-500">
            Primary: {{ resolvedData.primary_mission }}
          </div>
        </div>
      </div>

      <!-- Input Name -->
      <div class="mb-4 p-3 bg-zinc-800 rounded-lg">
        <div class="text-sm text-zinc-400">Input Name</div>
        <div class="text-lg font-medium text-zinc-100">{{ resolvedData.input_name }}</div>
      </div>

      <!-- Resolved Targets -->
      <div v-if="Object.keys(resolvedData.resolved_targets).length > 0">
        <h5 class="text-md font-medium text-zinc-100 mb-3">Available Targets</h5>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="(targetData, mission) in resolvedData.resolved_targets" 
            :key="mission"
            class="bg-zinc-800 p-4 rounded-lg border border-zinc-700 hover:border-zinc-600 transition-colors cursor-pointer"
            @click="selectTarget(mission as string, targetData)"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-zinc-300">{{ mission }}</div>
              <div 
                v-if="mission === resolvedData.primary_mission"
                class="px-2 py-1 bg-zinc-900 text-zinc-300 text-xs rounded"
              >
                Primary
              </div>
            </div>
            
            <div class="space-y-1">
              <div class="text-sm text-zinc-400">Target ID</div>
              <div class="text-lg font-mono text-zinc-100">{{ targetData.target_id || targetData.id || 'N/A' }}</div>
              
              <div v-if="targetData.name" class="text-sm text-zinc-400">Name</div>
              <div v-if="targetData.name" class="text-sm text-zinc-200">{{ targetData.name }}</div>
              
              <div v-if="targetData.coordinates" class="text-sm text-zinc-400">Coordinates</div>
              <div v-if="targetData.coordinates" class="text-xs font-mono text-zinc-300">
                RA: {{ targetData.coordinates.ra?.toFixed(6) || 'N/A' }}, 
                Dec: {{ targetData.coordinates.dec?.toFixed(6) || 'N/A' }}
              </div>
            </div>

            <button
              @click.stop="selectTarget(mission as string, targetData)"
              class="mt-3 w-full px-3 py-1 bg-zinc-600 hover:bg-zinc-700 text-white text-sm rounded transition-colors"
            >
              Use This Target
            </button>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="text-center py-8">
        <svg class="w-12 h-12 text-zinc-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33" />
        </svg>
        <p class="text-zinc-400">No targets found for this name</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-900/20 border border-red-700 p-4 rounded-lg">
      <div class="flex items-center gap-2 text-red-300">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <span class="font-medium">Resolution Error</span>
      </div>
      <p class="text-red-200 mt-2">{{ error }}</p>
    </div>

    <!-- Usage Instructions -->
    <div class="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
      <h5 class="text-sm font-medium text-zinc-300 mb-2">Supported Name Formats</h5>
      <div class="text-sm text-zinc-400 space-y-1">
        <div>• <span class="font-mono text-zinc-300">HD 209458</span> - Henry Draper catalog</div>
        <div>• <span class="font-mono text-zinc-300">Kepler-452b</span> - Kepler planet names</div>
        <div>• <span class="font-mono text-zinc-300">TOI-715</span> - TESS Objects of Interest</div>
        <div>• <span class="font-mono text-zinc-300">TIC 123456789</span> - TESS Input Catalog</div>
        <div>• <span class="font-mono text-zinc-300">KIC 12345678</span> - Kepler Input Catalog</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useExoScoutAPI, type ResolvedTarget, type Mission } from '@/composables/useExoScoutAPI'

const emit = defineEmits<{
  targetSelected: [mission: Mission, targetId: string, targetData: any]
  error: [error: string]
}>()

const { 
  resolveTarget: resolveTargetAPI, 
  getAvailableMissions,
  isLoading, 
  error, 
  clearError 
} = useExoScoutAPI()

const inputName = ref('')
const resolvedData = ref<ResolvedTarget | null>(null)
const selectedMission = ref<string>('')
const availableMissions = ref<string[]>([])
const isLoadingMissions = ref(false)

const loadAvailableMissions = async () => {
  isLoadingMissions.value = true
  try {
    availableMissions.value = await getAvailableMissions()
    // Set default mission to TESS if available
    if (availableMissions.value.includes('TESS')) {
      selectedMission.value = 'TESS'
    } else if (availableMissions.value.length > 0) {
      selectedMission.value = availableMissions.value[0]
    }
  } catch (err: any) {
    emit('error', `Failed to load available missions: ${err.message}`)
  } finally {
    isLoadingMissions.value = false
  }
}

const resolveTarget = async () => {
  if (!inputName.value.trim() || !selectedMission.value) return

  clearError()
  resolvedData.value = null

  try {
    const result = await resolveTargetAPI(inputName.value.trim())
    resolvedData.value = result
  } catch (err: any) {
    emit('error', err.message)
  }
}

const selectTarget = (mission: string, targetData: any) => {
  const targetId = targetData.target_id || targetData.id
  if (targetId && selectedMission.value) {
    // Use the selected mission instead of the detected one
    emit('targetSelected', selectedMission.value as Mission, targetId, targetData)
  }
}

// Load missions on component mount
onMounted(() => {
  loadAvailableMissions()
})

// Expose methods
defineExpose({
  resolveTarget,
  clearResults: () => {
    resolvedData.value = null
    inputName.value = ''
    clearError()
  }
})
</script>