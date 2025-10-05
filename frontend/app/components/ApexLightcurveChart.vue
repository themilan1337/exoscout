<template>
  <div class="space-y-4">
    <!-- Chart Container -->
    <div class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold text-zinc-100 flex">
          <svg class="mr-4 my-auto" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
            <!-- Icon from Pixel free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ -->
            <path fill="currentColor" d="M27.43 6.09h-4.57V1.52h1.52V0H3.05v32h25.9V4.57h-1.52Zm0 24.39H4.57V1.52h16.76v6.1h6.1Z"/>
            <path fill="currentColor" d="M25.91 3.05h1.52v1.52h-1.52Zm-1.53-1.53h1.53v1.53h-1.53Zm-3.05 21.34h-1.52v-9.15h-3.05v9.15h-1.52v-6.1h-3.05v6.1H7.62v-3.05h1.52v-1.52H7.62v-3.05h1.52v-1.53H7.62v-3.04H6.1v13.71h19.81v-1.52h-1.53v-7.62h-3.05z"/>
          </svg>
          <span class="my-auto">Lightcurve Data</span>
        </h3>
        <div class="flex items-center gap-2">
          <button
            v-if="lightcurveData"
            @click="downloadData"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 rounded text-sm transition-colors"
          >
            Download CSV
          </button>
          <button
            v-if="lightcurveData"
            @click="toggleNormalizedFlux"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 rounded text-sm transition-colors"
          >
            {{ showNormalizedFlux ? 'Hide' : 'Show' }} Normalized Flux
          </button>
          <div class="text-sm text-zinc-500">
            {{ lightcurveData ? `${lightcurveData.data_points.toLocaleString()} points` : 'No data' }}
          </div>
        </div>
      </div>

      <!-- Chart -->
      <div v-if="lightcurveData" class="relative">
        <ClientOnly>
          <VueApexCharts
            ref="chartRef"
            type="line"
            height="400"
            :options="chartOptions"
            :series="chartSeries"
            class="apex-lightcurve-chart"
          />
          <template #fallback>
            <div class="flex items-center justify-center h-96 bg-zinc-800 rounded">
              <div class="text-zinc-400">Loading chart...</div>
            </div>
          </template>
        </ClientOnly>
      </div>

      <!-- Loading State -->
      <div v-else-if="isLoading" class="flex items-center justify-center h-96 bg-zinc-800 rounded">
        <div class="flex items-center space-x-3">
          <svg class="animate-spin text-zinc-500" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
            <path fill="currentColor" d="M30.47 16.76h-3.05v-3.05h3.05v-1.52H25.9v1.52h-1.52v4.58h1.52v1.52h4.57v-1.52H32v-4.58h-1.53zm-3.05 6.1h1.53v4.57h-1.53Zm-4.57-1.53v1.53h-1.52v4.57h1.52v1.52h4.57v-1.52h-3.04v-4.57h3.04v-1.53zm4.57-10.66V9.14h1.53V4.57h-1.53v3.05H25.9V6.09h-1.52V4.57h3.04V3.05h-4.57v1.52h-1.52v4.57h1.52v1.53zM18.28 25.9h1.52v4.58h-1.52ZM19.8 1.52h-1.52V0h-4.57v1.52h-1.52v4.57h1.52v1.53h4.57V6.09h1.52zm-6.09 28.96h4.57V32h-4.57Zm0-6.1h4.57v1.52h-4.57Zm-1.52 1.52h1.52v4.58h-1.52Zm-3.05 3.05v-1.52h1.52v-4.57H9.14v-1.53H4.57v1.53h3.04v4.57H4.57v1.52zm1.52-24.38H9.14V3.05H4.57v1.52h3.04v1.52H6.09v1.53H4.57V4.57H3.04v4.57h1.53v1.53h4.57V9.14h1.52zM3.04 22.86h1.53v4.57H3.04Zm-1.52-3.05h4.57v-1.52h1.52v-4.58H6.09v-1.52H1.52v1.52h3.05v3.05H1.52v-3.05H0v4.58h1.52z"/>
          </svg>
          <span class="text-zinc-400">Loading lightcurve data...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex items-center justify-center h-96 bg-zinc-800 rounded">
        <div class="text-center">
          <svg class="text-zinc-600 mx-auto mb-4 size-16" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
            <path fill="currentColor" d="M30.48 9.14h-1.53V6.09h-1.52V4.57H25.9V3.05h-3.04V1.52h-3.05V0h-7.62v1.52H9.14v1.53H6.09v1.52H4.57v1.52H3.05v3.05H1.52v3.05H0v7.62h1.52v3.05h1.53v3.04h1.52v1.53h1.52v1.52h3.05v1.53h3.05V32h7.62v-1.52h3.05v-1.53h3.04v-1.52h1.53V25.9h1.52v-3.04h1.53v-3.05H32v-7.62h-1.52ZM19.81 25.9h-1.52v1.53h-4.58V25.9h-1.52v-4.57h1.52v-1.52h4.58v1.52h1.52Zm1.52-12.19h-1.52v3.05h-1.52v1.53h-4.58v-1.53h-1.52v-3.05h-1.52V6.09h1.52V4.57h7.62v1.52h1.52Z"/>
            <path fill="currentColor" d="M18.29 7.62h1.52v4.57h-1.52Zm-1.53-1.53h1.53v1.53h-1.53Z"/>
          </svg>
          <p class="text-zinc-400">{{ error }}</p>
          <button
            @click="retryLoad"
            class="mt-4 px-4 py-2 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 rounded transition-colors"
          >
            Retry
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="flex items-center justify-center h-96 bg-zinc-800 rounded">
        <div class="text-center">
          <svg class="w-12 h-12 text-zinc-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p class="text-zinc-400">No lightcurve data available</p>
          <p class="text-sm text-zinc-500 mt-2">Enter a target ID to load lightcurve data</p>
        </div>
      </div>
    </div>

    <!-- Data Statistics -->
    <div v-if="lightcurveData" class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
        <div class="text-sm text-zinc-400">Data Points</div>
        <div class="text-lg font-medium text-zinc-100">{{ lightcurveData.data_points.toLocaleString() }}</div>
      </div>
      <div class="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
        <div class="text-sm text-zinc-400">Time Range</div>
        <div class="text-lg font-medium text-zinc-100">{{ timeRange.toFixed(2) }} days</div>
      </div>
      <div class="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
        <div class="text-sm text-zinc-400">Flux Range</div>
        <div class="text-lg font-medium text-zinc-100">{{ fluxRange.toFixed(6) }}</div>
      </div>
      <div class="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
        <div class="text-sm text-zinc-400">Mission</div>
        <div class="text-lg font-medium text-zinc-100">{{ lightcurveData.mission }}</div>
      </div>
    </div>

    <!-- Metadata -->
    <div v-if="lightcurveData?.metadata" class="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
      <h4 class="text-lg font-medium text-zinc-100 mb-3">Metadata</h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div>
          <span class="text-zinc-400">Cadence:</span>
          <span class="text-zinc-200 ml-2">{{ lightcurveData.metadata.cadence }}</span>
        </div>
        <div>
          <span class="text-zinc-400">Pipeline:</span>
          <span class="text-zinc-200 ml-2">{{ lightcurveData.metadata.pipeline }}</span>
        </div>
        <div>
          <span class="text-zinc-400">Quality Flags:</span>
          <span class="text-zinc-200 ml-2">{{ lightcurveData.metadata.quality_flags }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useExoScoutAPI, type LightcurveData, type Mission } from '@/composables/useExoScoutAPI'
import VueApexCharts from 'vue3-apexcharts'

interface Props {
  targetId: string
  mission?: Mission
  autoLoad?: boolean
  showErrorBars?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoLoad: true,
  showErrorBars: false
})

const emit = defineEmits<{
  dataLoaded: [data: LightcurveData]
  error: [error: string]
}>()

// Composables
const { getLightcurve, detectMission, isLoading, error, clearError } = useExoScoutAPI()

// Reactive state
const lightcurveData = ref<LightcurveData | null>(null)
const chartRef = ref()
const showNormalizedFlux = ref(props.showErrorBars)

// Computed statistics
const timeRange = computed(() => {
  if (!lightcurveData.value) return 0
  return lightcurveData.value.time_range.end - lightcurveData.value.time_range.start
})

const fluxRange = computed(() => {
  if (!lightcurveData.value?.time_series.flux.length) return 0
  const fluxes = lightcurveData.value.time_series.flux
  return Math.max(...fluxes) - Math.min(...fluxes)
})

// Chart configuration
const chartOptions = computed(() => ({
  chart: {
    id: 'lightcurve-chart',
    type: 'line',
    background: 'transparent',
    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: true,
        reset: true
      }
    },
    zoom: {
      enabled: true,
      type: 'x'
    },
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 800
    }
  },
  theme: {
    mode: 'dark'
  },
  colors: ['#3b82f6', '#ef4444'],
  stroke: {
    curve: 'straight',
    width: [1, 1]
  },
  markers: {
    size: (lightcurveData.value?.data_points ?? 0) > 1000 ? 0 : 2,
    hover: {
      size: 4
    }
  },
  xaxis: {
    type: 'numeric',
    title: {
      text: 'Time (days)',
      style: {
        color: '#a1a1aa',
        fontSize: '14px'
      }
    },
    labels: {
      style: {
        colors: '#a1a1aa'
      },
      formatter: (value: number) => value.toFixed(2)
    },
    axisBorder: {
      color: '#52525b'
    },
    axisTicks: {
      color: '#52525b'
    }
  },
  yaxis: {
    title: {
      text: 'Relative Flux',
      style: {
        color: '#a1a1aa',
        fontSize: '14px'
      }
    },
    labels: {
      style: {
        colors: '#a1a1aa'
      },
      formatter: (value: number) => value.toFixed(6)
    },
    axisBorder: {
      color: '#52525b'
    }
  },
  grid: {
    borderColor: '#374151',
    strokeDashArray: 3
  },
  tooltip: {
    theme: 'dark',
    x: {
      formatter: (value: number) => `Time: ${value.toFixed(4)} days`
    },
    y: {
      formatter: (value: number) => `Flux: ${value.toFixed(8)}`
    }
  },
  legend: {
    show: showNormalizedFlux.value,
    position: 'top',
    labels: {
      colors: '#a1a1aa'
    }
  },
  dataLabels: {
    enabled: false
  }
}))

// Chart series data
const chartSeries = computed(() => {
  if (!lightcurveData.value) return []

  const { time, flux, flux_normalized } = lightcurveData.value.time_series
  
  const mainSeries = {
    name: 'Flux',
    data: time.map((t, i) => [t, flux[i]]).filter(([t, f]) => t != null && f != null)
  }

  const series = [mainSeries]

  // Add normalized flux if enabled and data is available
  if (showNormalizedFlux.value && flux_normalized && flux_normalized.length > 0) {
    const normalizedSeries = {
      name: 'Normalized Flux',
      data: time.map((t, i) => [t, flux_normalized[i]]).filter(([t, f]) => t != null && f != null)
    }
    
    series.push(normalizedSeries)
  }

  return series
})

// Methods
const toggleNormalizedFlux = () => {
  showNormalizedFlux.value = !showNormalizedFlux.value
}

const downloadData = () => {
  if (!lightcurveData.value) return

  const { time, flux, flux_normalized } = lightcurveData.value.time_series

  const csv = [
    'time,flux,flux_normalized',
    ...time.map((t: number, i: number) => 
      `${t},${flux[i]},${flux_normalized[i] || ''}`
    )
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `lightcurve_${props.targetId}_${lightcurveData.value?.mission || 'unknown'}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

const loadLightcurve = async () => {
  if (!props.targetId) return

  clearError()
  lightcurveData.value = null

  try {
    let mission: Mission = props.mission || 'TESS'
    if (!props.mission) {
      const detectedMission = await detectMission(props.targetId)
      if (detectedMission) {
        mission = detectedMission
      }
    }

    const data = await getLightcurve(mission, props.targetId)
    lightcurveData.value = data
    emit('dataLoaded', data)
  } catch (err: any) {
    emit('error', err.message)
  }
}

const retryLoad = () => {
  loadLightcurve()
}

// Watch for changes
watch([() => props.targetId, () => props.mission], () => {
  if (props.autoLoad && props.targetId) {
    loadLightcurve()
  }
}, { immediate: true })

// Expose methods
defineExpose({
  loadLightcurve,
  clearData: () => {
    lightcurveData.value = null
    clearError()
  },
  toggleNormalizedFlux,
  downloadData
})
</script>

<style scoped>
@reference "~/assets/css/main.css";

.apex-lightcurve-chart {
  @apply bg-zinc-800 rounded-lg;
}

/* Custom ApexCharts dark theme overrides */
:deep(.apexcharts-canvas) {
  background: transparent !important;
}

:deep(.apexcharts-tooltip) {
  background: #27272a !important;
  border: 1px solid #52525b !important;
  color: #f4f4f5 !important;
}

:deep(.apexcharts-tooltip-title) {
  background: #18181b !important;
  border-bottom: 1px solid #52525b !important;
  color: #f4f4f5 !important;
}

:deep(.apexcharts-toolbar) {
  background: rgba(39, 39, 42, 0.8) !important;
  border-radius: 6px !important;
}

:deep(.apexcharts-zoom-icon),
:deep(.apexcharts-pan-icon),
:deep(.apexcharts-reset-icon),
:deep(.apexcharts-download-icon) {
  fill: #a1a1aa !important;
}

:deep(.apexcharts-zoom-icon:hover),
:deep(.apexcharts-pan-icon:hover),
:deep(.apexcharts-reset-icon:hover),
:deep(.apexcharts-download-icon:hover) {
  fill: #f4f4f5 !important;
}
</style>