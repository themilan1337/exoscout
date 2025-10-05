/**
 * ExoScout API Composable
 * NASA Space Apps Challenge - A World Away: Hunting for Exoplanets with AI
 */

import { ref, computed } from 'vue'

// Types for API responses
export interface PredictionResult {
  mission: string
  target_id: string
  probability: number
  threshold: number
  classification: 'CONFIRMED' | 'FALSE_POSITIVE'
  used_features: Record<string, number>
}

export interface FeatureData {
  mission: string
  target_id: string
  features: Record<string, number>
  source: string
  last_updated?: string
  feature_count?: number
  available_features?: number
}

export interface LightcurveData {
  mission: string
  target_id: string
  sector?: number
  quarter?: number
  campaign?: number
  data_points: number
  time_range: {
    start: number
    end: number
  }
  lightcurve: {
    time: number[]
    flux: number[]
    flux_err: number[]
  }
  metadata: {
    cadence: string
    pipeline: string
    quality_flags: string
  }
}

export interface ResolvedTarget {
  mission: string
  target: string
  original_target: string
  numeric_id: string
  ra?: number
  dec?: number
  metadata: {
    // TESS/TOI metadata
    toi?: string
    tid?: number
    tfopwg_disp?: string  // Disposition: PC (Planet Candidate), CP (Confirmed Planet), FP (False Positive)
    pl_orbper?: number
    pl_rade?: number
    st_tmag?: number
    st_teff?: number
    st_rad?: number
    // Kepler/KOI metadata
    kepoi_name?: string
    kepid?: number
    koi_disposition?: string  // Disposition: CONFIRMED, CANDIDATE, FALSE POSITIVE
    koi_period?: number
    koi_prad?: number
    koi_kepmag?: number
    koi_steff?: number
    koi_srad?: number
    [key: string]: any
  }
}

export interface ModelStatus {
  available_missions: string[]
  models: Record<string, any>
  total_available: number
}

export interface APIError {
  detail: string
  status_code: number
}

export type Mission = 'TESS' | 'KEPLER' | 'K2'

export const useExoScoutAPI = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseUrl || 'http://localhost:8000'
  const apiVersion = config.public.apiVersion || 'v1'
  const timeout = config.public.apiTimeout || 30000
  const debug = config.public.apiDebug || false

  // Reactive state
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const lastResponse = ref<any>(null)

  // Computed API URL
  const apiURL = computed(() => `${baseURL}/api/${apiVersion}`)

  // Generic API request handler using fetch
  const apiRequest = async <T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> => {
    isLoading.value = true
    error.value = null

    try {
      const url = endpoint.startsWith('http') ? endpoint : `${baseURL}${endpoint}`
      
      if (debug) {
        console.log(`[ExoScout API] ${options.method || 'GET'} ${url}`)
      }

      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        const errorMessage = errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        throw new Error(errorMessage)
      }

      const data = await response.json()
      lastResponse.value = data
      
      if (debug) {
        console.log(`[ExoScout API] Response:`, data)
      }

      return data
    } catch (err: any) {
      const errorMessage = err.message || 'An unexpected error occurred'
      error.value = errorMessage
      
      if (debug) {
        console.error(`[ExoScout API] Error:`, err)
      }
      
      throw new Error(errorMessage)
    } finally {
      isLoading.value = false
    }
  }

  // Health check
  const healthCheck = async (): Promise<{ status: string }> => {
    return apiRequest('/health')
  }

  // Prediction endpoints
  const predictExoplanet = async (
    mission: Mission,
    targetId: string
  ): Promise<PredictionResult> => {
    return apiRequest(`/api/${apiVersion}/predict/${mission}/${targetId}`)
  }

  const getPredictionFeatures = async (
    mission: Mission,
    targetId: string
  ): Promise<FeatureData> => {
    return apiRequest(`/api/${apiVersion}/predict/${mission}/${targetId}/features`)
  }

  const predictWithCustomFeatures = async (
    mission: Mission,
    targetId: string,
    customFeatures?: Record<string, number>
  ): Promise<PredictionResult> => {
    const endpoint = `/api/${apiVersion}/predict/${mission}/${targetId}/custom`
    
    if (customFeatures) {
      return apiRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify(customFeatures)
      })
    } else {
      return apiRequest(endpoint)
    }
  }

  const getModelsStatus = async (): Promise<ModelStatus> => {
    return apiRequest(`/api/${apiVersion}/predict/models/status`)
  }

  const getAvailableMissions = async (): Promise<string[]> => {
    const status = await getModelsStatus()
    return status.available_missions
  }

  // Feature endpoints
  const getFeatures = async (
    mission: Mission,
    targetId: string
  ): Promise<FeatureData> => {
    return apiRequest(`/api/${apiVersion}/features/${mission}/${targetId}`)
  }

  // Lightcurve endpoints
  const getLightcurve = async (
    mission: Mission,
    targetId: string,
    options: {
      sector?: number
      quarter?: number
      campaign?: number
    } = {}
  ): Promise<LightcurveData> => {
    const params = new URLSearchParams()
    
    if (options.sector) params.append('sector', options.sector.toString())
    if (options.quarter) params.append('quarter', options.quarter.toString())
    if (options.campaign) params.append('campaign', options.campaign.toString())
    
    const queryString = params.toString()
    const endpoint = `/api/${apiVersion}/lightcurve/${mission}/${targetId}${queryString ? `?${queryString}` : ''}`
    
    return apiRequest(endpoint)
  }

  // Resolution endpoints
  const resolveTarget = async (targetName: string): Promise<ResolvedTarget> => {
    return apiRequest(`/api/${apiVersion}/resolve/${encodeURIComponent(targetName)}`)
  }

  const bulkResolveTargets = async (
    targets: string[],
    includeCoordinates: boolean = true
  ): Promise<{
    resolved_count: number
    failed_count: number
    results: Record<string, ResolvedTarget>
  }> => {
    return apiRequest(`/api/${apiVersion}/resolve/bulk`, {
      method: 'POST',
      body: JSON.stringify({
        targets,
        include_coordinates: includeCoordinates
      })
    })
  }

  // Utility functions
  const clearError = () => {
    error.value = null
  }

  const reset = () => {
    isLoading.value = false
    error.value = null
    lastResponse.value = null
  }

  // Auto-detect mission from target ID
  const detectMission = (targetId: string): Mission | null => {
    const id = targetId.toString()
    
    // TESS TIC IDs are typically 8-10 digits
    if (/^\d{8,10}$/.test(id)) {
      return 'TESS'
    }
    
    // Kepler KepIDs are typically 8-9 digits
    if (/^\d{8,9}$/.test(id)) {
      return 'KEPLER'
    }
    
    // K2 EPIC IDs are typically 9 digits starting with 2
    if (/^2\d{8}$/.test(id)) {
      return 'K2'
    }
    
    return null
  }

  // Smart prediction that tries to auto-detect mission
  const smartPredict = async (targetId: string): Promise<{
    result: PredictionResult
    detectedMission: Mission
  }> => {
    const detectedMission = detectMission(targetId)
    
    if (!detectedMission) {
      throw new Error('Could not auto-detect mission from target ID. Please specify mission manually.')
    }
    
    const result = await predictExoplanet(detectedMission, targetId)
    
    return {
      result,
      detectedMission
    }
  }

  // Comprehensive exoplanet analysis
  const analyzeExoplanet = async (
    mission: Mission,
    targetId: string,
    options: {
      includeLightcurve?: boolean
      lightcurveOptions?: {
        sector?: number
        quarter?: number
        campaign?: number
      }
    } = {}
  ): Promise<{
    prediction?: PredictionResult
    features?: FeatureData
    lightcurve?: LightcurveData
  }> => {
    const results: any = {}

    try {
      results.prediction = await predictExoplanet(mission, targetId)
    } catch (err) {
      console.warn('Prediction failed:', err)
    }

    try {
      results.features = await getFeatures(mission, targetId)
    } catch (err) {
      console.warn('Features failed:', err)
    }

    if (options.includeLightcurve) {
      try {
        results.lightcurve = await getLightcurve(mission, targetId, options.lightcurveOptions || {})
      } catch (err) {
        console.warn('Lightcurve failed:', err)
      }
    }

    return results
  }

  return {
    // State
    isLoading: readonly(isLoading),
    error: readonly(error),
    lastResponse: readonly(lastResponse),
    
    // Configuration
    baseURL,
    apiURL,
    
    // Core API methods
    healthCheck,
    predictExoplanet,
    getPredictionFeatures,
    predictWithCustomFeatures,
    getModelsStatus,
    getAvailableMissions,
    getFeatures,
    getLightcurve,
    resolveTarget,
    bulkResolveTargets,
    
    // Utility methods
    clearError,
    reset,
    detectMission,
    smartPredict,
    analyzeExoplanet,
    
    // Raw API request method for custom endpoints
    apiRequest
  }
}