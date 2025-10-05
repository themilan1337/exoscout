<template>
  <div class="space-y-6">
    <!-- Prediction Results Card -->
    <div v-if="predictionData" class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold text-zinc-100">AI Prediction Results</h3>
        <div class="flex items-center gap-2">
          <div 
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              predictionData.classification === 'CONFIRMED' 
                ? 'bg-green-900 text-green-300 border border-green-700' 
                : 'bg-red-900 text-red-300 border border-red-700'
            ]"
          >
            {{ predictionData.classification }}
          </div>
          <div class="text-sm text-zinc-500">
            {{ Math.round(predictionData.probability * 100) }}% confidence
          </div>
        </div>
      </div>

      <!-- Confidence Meter -->
      <div class="mb-6">
        <div class="flex justify-between text-sm text-zinc-400 mb-2">
          <span>Confidence Level</span>
          <span>{{ Math.round(predictionData.probability * 100) }}%</span>
        </div>
        <div class="w-full bg-zinc-800 rounded-full h-3">
          <div 
            :class="[
              'h-3 rounded-full transition-all duration-500',
              predictionData.probability >= predictionData.threshold 
                ? 'bg-gradient-to-r from-green-600 to-green-400' 
                : 'bg-gradient-to-r from-red-600 to-red-400'
            ]"
            :style="{ width: `${predictionData.probability * 100}%` }"
          ></div>
        </div>
        <div class="flex justify-between text-xs text-zinc-500 mt-1">
          <span>0%</span>
          <span 
            class="text-zinc-300"
            :style="{ marginLeft: `${predictionData.threshold * 100 - 5}%` }"
          >
            Threshold: {{ Math.round(predictionData.threshold * 100) }}%
          </span>
          <span>100%</span>
        </div>
      </div>

      <!-- Mission Info -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-zinc-800 p-4 rounded-lg">
          <div class="text-sm text-zinc-400">Mission</div>
          <div class="text-lg font-medium text-zinc-100">{{ predictionData.mission }}</div>
        </div>
        <div class="bg-zinc-800 p-4 rounded-lg">
          <div class="text-sm text-zinc-400">Target ID</div>
          <div class="text-lg font-medium text-zinc-100">{{ predictionData.target_id }}</div>
        </div>
        <div class="bg-zinc-800 p-4 rounded-lg">
          <div class="text-sm text-zinc-400">Model Threshold</div>
          <div class="text-lg font-medium text-zinc-100">{{ Math.round(predictionData.threshold * 100) }}%</div>
        </div>
      </div>

      <!-- Features Used -->
      <div>
        <h4 class="text-lg font-medium text-zinc-100 mb-3">Features Used in Prediction</h4>
        
        <!-- Available Features -->
        <div v-if="Object.keys(availableFeatures).length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mb-4">
          <div 
            v-for="(value, key) in availableFeatures" 
            :key="key"
            class="bg-zinc-800 p-3 rounded-lg"
          >
            <div class="text-xs text-zinc-400 uppercase tracking-wide">{{ formatFeatureName(key) }}</div>
            <div class="text-sm font-medium text-zinc-100">{{ formatFeatureValue(key, value) }}</div>
          </div>
        </div>
        
        <!-- No Features Available Message -->
        <div v-else class="bg-zinc-800 p-4 rounded-lg border border-zinc-600">
          <div class="flex items-center gap-2 text-amber-400 mb-2">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span class="font-medium">Limited Feature Data</span>
          </div>
          <p class="text-zinc-300 text-sm">
            No specific feature values were available for this target. The AI model made its prediction based on internal feature extraction and processing.
          </p>
          <p class="text-zinc-400 text-xs mt-2">
            This is common for targets where detailed astronomical parameters haven't been catalogued yet.
          </p>
        </div>
      </div>
    </div>

    <!-- Additional Features Card -->
    <div v-if="featuresData" class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <h3 class="text-xl font-semibold text-zinc-100 mb-4">Complete Feature Set</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <div 
          v-for="(value, key) in featuresData.features" 
          :key="key"
          class="bg-zinc-800 p-3 rounded-lg"
        >
          <div class="text-xs text-zinc-400 uppercase tracking-wide">{{ formatFeatureName(key) }}</div>
          <div class="text-sm font-medium text-zinc-100">{{ formatFeatureValue(key, value) }}</div>
        </div>
      </div>
      <div class="mt-4 text-sm text-zinc-500">
        Source: {{ featuresData.source }}
        <span v-if="featuresData.last_updated"> • Updated: {{ formatDate(featuresData.last_updated) }}</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-900/20 border border-red-700 p-4 rounded-lg">
      <div class="flex items-center gap-2 text-red-300">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <span class="font-medium">Prediction Error</span>
      </div>
      <p class="text-red-200 mt-2">{{ error }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <div class="flex items-center justify-center space-x-3">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-zinc-400"></div>
        <span class="text-zinc-400">Analyzing exoplanet data...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useExoScoutAPI, type PredictionResult, type FeatureData, type Mission } from '@/composables/useExoScoutAPI'

interface Props {
  targetId: string
  mission?: Mission
  autoPredict?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoPredict: true
})

const emit = defineEmits<{
  predictionComplete: [result: PredictionResult]
  error: [error: string]
}>()

const { 
  predictExoplanet, 
  getFeatures, 
  smartPredict, 
  detectMission,
  isLoading, 
  error,
  clearError 
} = useExoScoutAPI()

const predictionData = ref<PredictionResult | null>(null)
const featuresData = ref<FeatureData | null>(null)

// Computed property to get available features (non-null values)
const availableFeatures = computed(() => {
  if (!predictionData.value?.used_features) return {}
  
  const features: Record<string, number> = {}
  Object.entries(predictionData.value.used_features).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      features[key] = value
    }
  })
  return features
})

// Feature name formatting
const featureNameMap: Record<string, string> = {
  'pl_orbper': 'Orbital Period',
  'pl_trandurh': 'Transit Duration',
  'pl_trandep': 'Transit Depth',
  'pl_rade': 'Planet Radius',
  'pl_insol': 'Insolation Flux',
  'pl_eqt': 'Equilibrium Temperature',
  'st_teff': 'Stellar Temperature',
  'st_logg': 'Stellar Surface Gravity',
  'st_rad': 'Stellar Radius',
  'st_tmag': 'TESS Magnitude',
  'st_kmag': 'Kepler Magnitude'
}

const formatFeatureName = (key: string): string => {
  return featureNameMap[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const formatFeatureValue = (key: string, value: number | null): string => {
  if (value === null || value === undefined) {
    return 'N/A'
  }
  
  if (key.includes('temp') || key.includes('teff')) {
    return `${value.toFixed(0)} K`
  }
  if (key.includes('per') || key.includes('dur')) {
    return `${value.toFixed(2)} days`
  }
  if (key.includes('rad')) {
    return `${value.toFixed(2)} R⊕`
  }
  if (key.includes('mag')) {
    return `${value.toFixed(2)} mag`
  }
  if (key.includes('dep')) {
    return `${value.toFixed(0)} ppm`
  }
  return value.toFixed(3)
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString()
}

// Main prediction function
const runPrediction = async () => {
  if (!props.targetId) return

  clearError()
  predictionData.value = null
  featuresData.value = null

  try {
    let result: PredictionResult
    let detectedMission: Mission

    if (props.mission) {
      // Use specified mission
      result = await predictExoplanet(props.mission, props.targetId)
      detectedMission = props.mission
    } else {
      // Auto-detect mission
      const smartResult = await smartPredict(props.targetId)
      result = smartResult.result
      detectedMission = smartResult.detectedMission
    }

    predictionData.value = result
    emit('predictionComplete', result)

    // Also fetch complete features
    try {
      const features = await getFeatures(detectedMission, props.targetId)
      featuresData.value = features
    } catch (featuresError) {
      console.warn('Could not fetch additional features:', featuresError)
    }

  } catch (err: any) {
    emit('error', err.message)
  }
}

// Watch for changes in targetId or mission
watch([() => props.targetId, () => props.mission], () => {
  if (props.autoPredict && props.targetId) {
    runPrediction()
  }
}, { immediate: true })

// Expose methods for manual control
defineExpose({
  runPrediction,
  clearResults: () => {
    predictionData.value = null
    featuresData.value = null
    clearError()
  }
})
</script>