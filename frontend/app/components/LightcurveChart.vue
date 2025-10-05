<template>
  <div class="space-y-4">
    <!-- Chart Container -->
    <div class="bg-zinc-900 p-6 rounded-lg border border-zinc-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold text-zinc-100">Lightcurve Data</h3>
        <div class="flex items-center gap-2">
          <button
            v-if="lightcurveData"
            @click="downloadData"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 rounded text-sm transition-colors"
          >
            Download CSV
          </button>
          <div class="text-sm text-zinc-500">
            {{ lightcurveData ? `${lightcurveData.data_points} points` : 'No data' }}
          </div>
        </div>
      </div>

      <!-- Chart -->
      <div v-if="lightcurveData" class="relative">
        <canvas 
          ref="chartCanvas" 
          class="w-full h-80 bg-zinc-800 rounded cursor-crosshair"
        ></canvas>
      </div>

      <!-- Loading State -->
      <div v-else-if="isLoading" class="flex items-center justify-center h-80 bg-zinc-800 rounded">
        <div class="flex items-center space-x-3">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-zinc-400"></div>
          <span class="text-zinc-400">Loading lightcurve data...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex items-center justify-center h-80 bg-zinc-800 rounded">
        <div class="text-center">
          <svg class="w-12 h-12 text-zinc-600 mx-auto mb-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <p class="text-zinc-400">{{ error }}</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="flex items-center justify-center h-80 bg-zinc-800 rounded">
        <div class="text-center">
          <svg class="w-12 h-12 text-zinc-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p class="text-zinc-400">No lightcurve data available</p>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useExoScoutAPI, type LightcurveData, type Mission } from '@/composables/useExoScoutAPI'

interface Props {
  targetId: string
  mission?: Mission
  autoLoad?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoLoad: true
})

const emit = defineEmits<{
  dataLoaded: [data: LightcurveData]
  error: [error: string]
}>()

const { getLightcurve, detectMission, isLoading, error, clearError } = useExoScoutAPI()

const lightcurveData = ref<LightcurveData | null>(null)
const chartCanvas = ref<HTMLCanvasElement | null>(null)

// Computed statistics
const timeRange = computed(() => {
  if (!lightcurveData.value) return 0
  return lightcurveData.value.time_range.end - lightcurveData.value.time_range.start
})

const fluxRange = computed(() => {
  if (!lightcurveData.value?.lightcurve.flux.length) return 0
  const fluxes = lightcurveData.value.lightcurve.flux
  return Math.max(...fluxes) - Math.min(...fluxes)
})

// Chart drawing
const drawChart = () => {
  if (!chartCanvas.value || !lightcurveData.value) return

  const canvas = chartCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // Set canvas size
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * window.devicePixelRatio
  canvas.height = rect.height * window.devicePixelRatio
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio)

  const width = rect.width
  const height = rect.height
  const padding = 60

  // Clear canvas
  ctx.fillStyle = '#27272a' // zinc-800
  ctx.fillRect(0, 0, width, height)

  const times = lightcurveData.value.lightcurve.time
  const fluxes = lightcurveData.value.lightcurve.flux
  
  if (times.length === 0) return

  // Calculate scales
  const timeMin = Math.min(...times)
  const timeMax = Math.max(...times)
  const fluxMin = Math.min(...fluxes)
  const fluxMax = Math.max(...fluxes)

  const timeScale = (width - 2 * padding) / (timeMax - timeMin)
  const fluxScale = (height - 2 * padding) / (fluxMax - fluxMin)

  // Draw axes
  ctx.strokeStyle = '#52525b' // zinc-600
  ctx.lineWidth = 1
  
  // X-axis
  ctx.beginPath()
  ctx.moveTo(padding, height - padding)
  ctx.lineTo(width - padding, height - padding)
  ctx.stroke()

  // Y-axis
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, height - padding)
  ctx.stroke()

  // Draw axis labels
  ctx.fillStyle = '#a1a1aa' // zinc-400
  ctx.font = '12px system-ui'
  ctx.textAlign = 'center'
  ctx.fillText('Time (days)', width / 2, height - 10)
  
  ctx.save()
  ctx.translate(15, height / 2)
  ctx.rotate(-Math.PI / 2)
  ctx.fillText('Relative Flux', 0, 0)
  ctx.restore()

  // Draw tick marks and labels
  const numTicks = 5
  
  // X-axis ticks
  for (let i = 0; i <= numTicks; i++) {
    const x = padding + (i / numTicks) * (width - 2 * padding)
    const time = timeMin + (i / numTicks) * (timeMax - timeMin)
    
    ctx.strokeStyle = '#52525b'
    ctx.beginPath()
    ctx.moveTo(x, height - padding)
    ctx.lineTo(x, height - padding + 5)
    ctx.stroke()
    
    ctx.fillStyle = '#a1a1aa'
    ctx.textAlign = 'center'
    ctx.fillText(time.toFixed(2), x, height - padding + 20)
  }

  // Y-axis ticks
  for (let i = 0; i <= numTicks; i++) {
    const y = height - padding - (i / numTicks) * (height - 2 * padding)
    const flux = fluxMin + (i / numTicks) * (fluxMax - fluxMin)
    
    ctx.strokeStyle = '#52525b'
    ctx.beginPath()
    ctx.moveTo(padding - 5, y)
    ctx.lineTo(padding, y)
    ctx.stroke()
    
    ctx.fillStyle = '#a1a1aa'
    ctx.textAlign = 'right'
    ctx.fillText(flux.toFixed(6), padding - 10, y + 4)
  }

  // Draw data points
  ctx.fillStyle = '#3b82f6' // blue-500
  ctx.strokeStyle = '#1d4ed8' // blue-700
  
  if (times.length > 1000) {
    // For large datasets, draw as a line
    ctx.beginPath()
    times.forEach((time, i) => {
      const flux = fluxes[i]
      if (flux !== undefined) {
        const x = padding + (time - timeMin) * timeScale
        const y = height - padding - (flux - fluxMin) * fluxScale
        
        if (i === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      }
    })
    ctx.lineWidth = 1
    ctx.stroke()
  } else {
    // For smaller datasets, draw individual points
    times.forEach((time, i) => {
      const flux = fluxes[i]
      if (flux !== undefined) {
        const x = padding + (time - timeMin) * timeScale
        const y = height - padding - (flux - fluxMin) * fluxScale
        
        ctx.beginPath()
        ctx.arc(x, y, 2, 0, 2 * Math.PI)
        ctx.fill()
      }
    })
  }
}

// Data download
const downloadData = () => {
  if (!lightcurveData.value) return

  const times = lightcurveData.value.lightcurve.time
  const fluxes = lightcurveData.value.lightcurve.flux
  const fluxErrors = lightcurveData.value.lightcurve.flux_err

  const csv = [
    'time,flux,flux_err',
    ...times.map((time, i) => 
      `${time},${fluxes[i]},${fluxErrors[i] || ''}`
    )
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `lightcurve_${props.targetId}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// Load lightcurve data
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

    await nextTick()
    drawChart()
  } catch (err: any) {
    emit('error', err.message)
  }
}

// Watch for changes
watch([() => props.targetId, () => props.mission], () => {
  if (props.autoLoad && props.targetId) {
    loadLightcurve()
  }
}, { immediate: true })

// Redraw chart on resize
onMounted(() => {
  const resizeObserver = new ResizeObserver(() => {
    if (lightcurveData.value) {
      nextTick(() => drawChart())
    }
  })
  
  if (chartCanvas.value) {
    resizeObserver.observe(chartCanvas.value)
  }
})

// Expose methods
defineExpose({
  loadLightcurve,
  clearData: () => {
    lightcurveData.value = null
    clearError()
  }
})
</script>