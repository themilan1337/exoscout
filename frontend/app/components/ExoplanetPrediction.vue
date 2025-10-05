<template>
  <div class="space-y-6">
    <div v-if="predictionData" class="p-6 rounded-lg border border-dashed border-zinc-600">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold text-zinc-100 flex">
          <svg class="mr-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M28.95 15.24h1.53v7.62h-1.53Zm-1.52 9.15h1.52v-1.53h-1.52v-7.62h1.52v-1.52h-1.52v-3.05H25.9v3.05H6.1v-3.05H4.57v3.05H3.05v1.52h1.52v7.62H3.05v1.53h1.52v1.52H6.1V15.24h19.8v10.67h1.53zM25.9 0h1.53v1.53H25.9Zm-1.52 25.91h1.52v1.52h-1.52Z"/><path fill="currentColor" d="M24.38 7.62h1.52v3.05h-1.52Zm0-6.09h1.52v1.52h-1.52ZM22.86 6.1h1.52v1.52h-1.52Zm0-3.05h1.52v1.53h-1.52Zm-1.53 27.43h1.53v-1.52h1.52v-1.53h-3.05zm-1.52-25.9h3.05V6.1h-3.05Zm-1.52 25.9h3.04V32h-3.04Zm-4.58-3.05v3.05h1.53v-1.52h1.52v1.52h1.53v-3.05zM12.19 3.05h7.62v1.53h-7.62Zm-1.52 27.43h3.04V32h-3.04Zm12.19-18.29V9.15h-1.53V7.62H10.67v1.53H9.14v3.04Zm-4.57-3.04h1.52v1.52h-1.52Zm-6.1 0h1.52v1.52h-1.52ZM9.14 4.58h3.05V6.1H9.14ZM7.62 27.43v1.53h1.52v1.52h1.53v-3.05zm0-21.33h1.52v1.52H7.62Zm0-3.05h1.52v1.53H7.62ZM6.1 25.91h1.52v1.52H6.1Zm0-18.29h1.52v3.05H6.1Zm0-6.09h1.52v1.52H6.1ZM4.57 0H6.1v1.53H4.57ZM1.52 15.24h1.53v7.62H1.52Z"/></svg>
          <span class="my-auto">AI Prediction Results</span>
        </h3>
        <div class="flex items-center gap-2">
          <div 
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium flex items-center gap-2',
              predictionData.classification === 'CONFIRMED' 
                ? 'bg-green-900 text-green-300 border border-green-700' 
                : 'bg-red-900 text-red-300 border border-red-700'
            ]"
          >
            <!-- Confirmed state icon -->
            <svg v-if="predictionData.classification === 'CONFIRMED'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 32 32" class="flex-shrink-0">
              <!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ -->
              <path fill="currentColor" d="M28.955 15.245h1.52v1.52h-1.52Zm-1.53 1.52h1.53v1.52h-1.53Zm0-3.05h1.53v1.53h-1.53Zm-1.52 4.57h1.52v1.53h-1.52Zm0-6.09h1.52v1.52h-1.52Zm-1.52 12.19h-4.58v1.52h6.1v-6.09h-1.52zm-9.15-7.62h-1.52v-1.52h-1.53v-1.53h-1.52v1.53h-1.52v1.52h1.52v1.52h1.52v1.53h1.53v1.52h1.52v-1.52h1.53v-1.53h1.52v-1.52h1.52v-1.52h1.53v-1.53h1.52v-1.52h-1.52v-1.53h-1.53v1.53h-1.52v1.52h-1.52v1.53h-1.53zm9.15-9.14v4.57h1.52v-6.1h-6.1v1.53zm-6.1 18.28h1.52v1.53h-1.52Zm0-21.33h1.52v1.52h-1.52Zm-1.52 22.86h1.52v1.52h-1.52Zm0-24.38h1.52v1.52h-1.52Zm-1.53 25.9h1.53v1.52h-1.53Zm0-27.43h1.53v1.53h-1.53Zm-1.52 25.91h1.52v1.52h-1.52Zm0-24.38h1.52v1.52h-1.52Zm-1.53 22.85h1.53v1.53h-1.53Zm0-21.33h1.53v1.52h-1.53Zm-4.57 19.81v-4.57h-1.52v6.09h6.09v-1.52z"/>
              <path fill="currentColor" d="M7.615 7.625h4.57v-1.53h-6.09v6.1h1.52zm-3.04 10.66h1.52v1.53h-1.52Zm0-6.09h1.52v1.52h-1.52Zm-1.53 4.57h1.53v1.52h-1.53Zm0-3.05h1.53v1.53h-1.53Zm-1.52 1.53h1.52v1.52h-1.52Z"/>
            </svg>
            <!-- Not confirmed state icon -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 32 32" class="flex-shrink-0">
              <!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ -->
              <path fill="currentColor" d="M30.48 9.14h-1.53V6.09h-1.52V4.57H25.9V3.05h-3.04V1.52h-3.05V0h-7.62v1.52H9.14v1.53H6.09v1.52H4.57v1.52H3.05v3.05H1.52v3.05H0v7.62h1.52v3.05h1.53v3.04h1.52v1.53h1.52v1.52h3.05v1.53h3.05V32h7.62v-1.52h3.05v-1.53h3.04v-1.52h1.53V25.9h1.52v-3.04h1.53v-3.05H32v-7.62h-1.52ZM19.81 25.9h-1.52v1.53h-4.58V25.9h-1.52v-4.57h1.52v-1.52h4.58v1.52h1.52Zm1.52-12.19h-1.52v3.05h-1.52v1.53h-4.58v-1.53h-1.52v-3.05h-1.52V6.09h1.52V4.57h7.62v1.52h1.52Z"/>
              <path fill="currentColor" d="M18.29 7.62h1.52v4.57h-1.52Zm-1.53-1.53h1.53v1.53h-1.53Z"/>
            </svg>
            {{ predictionData.classification }}
          </div>
          <div class="text-sm text-zinc-500">
            {{ Math.round(predictionData.probability * 100) }}% confidence
          </div>
        </div>
      </div>

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

      <div>
        <h4 class="text-lg font-medium text-zinc-100 mb-3 flex">
          <svg class="mr-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M30.48 10.66h-9.15v1.53h-1.52v1.52h-1.52v1.52h-1.53V4.57h1.53V1.52h-1.53V0h-1.52v1.52h-1.53v3.05h-1.52v3.05h-1.52v3.04H1.52v1.53H0v1.52h1.52v1.52h1.53v1.53H6.1v1.52h1.52v3.05h1.52v-1.52h3.05v-1.53h3.05v1.53h-1.53v1.52h-1.52v1.52h-1.52v1.53H9.14v1.52H7.62v1.53H6.1v1.52H4.57v-1.52H3.05v3.04h1.52V32h3.05v-1.53h1.52v-1.52h3.05v-1.52h1.52V25.9h1.53v-1.52h1.52v-4.57h1.53v1.52h1.52v1.52h1.52v1.53h1.53v1.52h1.52v1.53h1.52v3.04h-1.52V32h3.05v-1.53h1.52v-3.04h-1.52v-3.05H25.9v-3.05h-1.52v-3.05h1.52v-1.52h-3.04v1.52h-6.1v-1.52h4.57v-1.53h1.53v-1.52h6.09v1.52h1.53v-1.52H32v-1.52h-1.52Zm-16.77 6.1h-3.04v-1.53H7.62v-1.52H4.57v-1.52h7.62v1.52h1.52Z"/><path fill="currentColor" d="M25.9 15.23h3.05v1.53H25.9Zm-3.04 13.72h1.52v1.52h-1.52Zm-3.05-1.52h3.05v1.52h-3.05Zm0-19.81h1.52v3.04h-1.52ZM18.29 25.9h1.52v1.53h-1.52Zm0-21.33h1.52v3.05h-1.52Zm-1.53 19.81h1.53v1.52h-1.53ZM6.1 21.33h1.52v3.05H6.1Zm-1.53 3.05H6.1v3.05H4.57Z"/></svg>
          <span class="my-auto">Features Used in Prediction</span>
        </h4>
        
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

    <div v-if="error" class="bg-red-900/20 border border-red-700 p-4 rounded-lg">
      <div class="flex items-center gap-2 text-red-300">
        <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ --><path fill="currentColor" d="M30.48 24.38h-1.53v-3.05h-1.52v-3.04H25.9v-3.05h-1.52v-3.05h-1.52V9.14h-1.53V6.09h-1.52V3.05h-1.52V1.52h-1.53V0h-1.52v1.52h-1.53v1.53h-1.52v3.04h-1.52v3.05H9.14v3.05H7.62v3.05H6.09v3.05H4.57v3.04H3.05v3.05H1.52v3.05H0v3.05h1.52V32h28.96v-1.52H32v-3.05h-1.52Zm-10.67 3.05h-1.52v1.52h-4.58v-1.52h-1.52v-4.57h1.52v-1.53h4.58v1.53h1.52Zm0-10.67h-1.52v3.05h-4.58v-3.05h-1.52v-6.09h1.52V9.14h4.58v1.53h1.52Z"/><path fill="currentColor" d="M16.76 12.19h1.53v3.05h-1.53Zm-1.52-1.52h1.52v1.52h-1.52Z"/></svg>
        <span class="font-medium">Prediction Error</span>
      </div>
      <p class="text-red-200 mt-2">{{ error }}</p>
    </div>

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

const runPrediction = async () => {
  if (!props.targetId) return

  clearError()
  predictionData.value = null
  featuresData.value = null

  try {
    let result: PredictionResult
    let detectedMission: Mission

    if (props.mission) {
      result = await predictExoplanet(props.mission, props.targetId)
      detectedMission = props.mission
    } else {
      const smartResult = await smartPredict(props.targetId)
      result = smartResult.result
      detectedMission = smartResult.detectedMission
    }

    predictionData.value = result
    emit('predictionComplete', result)

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

watch([() => props.targetId, () => props.mission], () => {
  if (props.autoPredict && props.targetId) {
    runPrediction()
  }
}, { immediate: true })

defineExpose({
  runPrediction,
  clearResults: () => {
    predictionData.value = null
    featuresData.value = null
    clearError()
  }
})
</script>