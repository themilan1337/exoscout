// @ts-ignore - Three.js types not available
import * as THREE from 'three'
import { noiseFunctions, planetVertexShader, planetFragmentShader } from './shaders'

export interface PlanetParams {
  type: number
  radius: number
  amplitude: number
  sharpness: number
  offset: number
  period: number
  persistence: number
  lacunarity: number
  octaves: number
  undulation: number
  ambientIntensity: number
  diffuseIntensity: number
  specularIntensity: number
  shininess: number
  lightDirection: THREE.Vector3
  lightColor: THREE.Color
  bumpStrength: number
  bumpOffset: number
  color1: THREE.Color
  color2: THREE.Color
  color3: THREE.Color
  color4: THREE.Color
  color5: THREE.Color
  transition2: number
  transition3: number
  transition4: number
  transition5: number
  blend12: number
  blend23: number
  blend34: number
  blend45: number
}

export interface ExoplanetData {
  id: string
  name: string
  type: string
  mass: string
  radius: string
  temperature: string
  distance: string
  discoveryYear: number
  hostStar: string
}

export function usePlanetGenerator() {
  // Generate planet parameters with seeded randomness - Earth-like and realistic
  const generatePlanetParams = (id: string): PlanetParams => {
    const seed = hashCode(id)
    const random = seededRandom(seed)
    
    // Base Earth-like parameters with small variations
    const baseParams = {
      type: 2, // Use type 2 which looks most Earth-like
      radius: 20.0,
      amplitude: 1.19,
      sharpness: 2.6,
      offset: -0.016,
      period: 0.6,
      persistence: 0.484,
      lacunarity: 1.8,
      octaves: 10,
      undulation: 0.0,
      ambientIntensity: 0.02,
      diffuseIntensity: 1.0,
      specularIntensity: 2.0,
      shininess: 10.0,
      lightDirection: new THREE.Vector3(1, 1, 1).normalize(),
      lightColor: new THREE.Color(0xffffff),
      bumpStrength: 1.0,
      bumpOffset: 0.001,
      // Earth-like colors with slight variations
      color1: new THREE.Color(0.014, 0.117, 0.279), // Deep ocean blue
      color2: new THREE.Color(0.080, 0.527, 0.351), // Shallow water/coastal
      color3: new THREE.Color(0.620, 0.516, 0.372), // Beach/desert
      color4: new THREE.Color(0.149, 0.254, 0.084), // Forest/vegetation
      color5: new THREE.Color(0.150, 0.150, 0.150), // Mountains/rocks
      transition2: 0.071,
      transition3: 0.215,
      transition4: 0.372,
      transition5: 1.2,
      blend12: 0.152,
      blend23: 0.152,
      blend34: 0.104,
      blend45: 0.168
    }
    
    // Add small variations to make each planet unique but still Earth-like
    return {
      ...baseParams,
      // Slight variations in terrain
      amplitude: baseParams.amplitude + (random() - 0.5) * 0.3, // ±0.15 variation
      sharpness: baseParams.sharpness + (random() - 0.5) * 0.4, // ±0.2 variation
      period: baseParams.period + (random() - 0.5) * 0.2, // ±0.1 variation
      persistence: baseParams.persistence + (random() - 0.5) * 0.1, // ±0.05 variation
      
      // Slight color variations for different planet types
      color1: new THREE.Color(
        Math.max(0, baseParams.color1.r + (random() - 0.5) * 0.02),
        Math.max(0, baseParams.color1.g + (random() - 0.5) * 0.05),
        Math.max(0, baseParams.color1.b + (random() - 0.5) * 0.1)
      ),
      color2: new THREE.Color(
        Math.max(0, baseParams.color2.r + (random() - 0.5) * 0.1),
        Math.max(0, baseParams.color2.g + (random() - 0.5) * 0.1),
        Math.max(0, baseParams.color2.b + (random() - 0.5) * 0.05)
      ),
      color4: new THREE.Color(
        Math.max(0, baseParams.color4.r + (random() - 0.5) * 0.05),
        Math.max(0, baseParams.color4.g + (random() - 0.5) * 0.1),
        Math.max(0, baseParams.color4.b + (random() - 0.5) * 0.02)
      )
    }
  }

  // Generate mock exoplanet data
  const generateExoplanetData = (id: string): ExoplanetData => {
    const seed = hashCode(id)
    const random = seededRandom(seed)
    
    const planetTypes = ['Super Earth', 'Gas Giant', 'Rocky Planet', 'Ice Giant', 'Hot Jupiter']
    const starNames = ['Kepler', 'TRAPPIST', 'HD', 'WASP', 'TOI', 'K2', 'EPIC']
    
    return {
      id,
      name: `${starNames[Math.floor(random() * starNames.length)] || 'Kepler'}-${id}b`,
      type: planetTypes[Math.floor(random() * planetTypes.length)] || 'Rocky Planet',
      mass: `${(0.1 + random() * 10).toFixed(2)} Earth masses`,
      radius: `${(0.5 + random() * 3).toFixed(2)} Earth radii`,
      temperature: `${Math.floor(200 + random() * 800)}K`,
      distance: `${(10 + random() * 1000).toFixed(1)} light-years`,
      discoveryYear: 2009 + Math.floor(random() * 15),
      hostStar: `${starNames[Math.floor(random() * starNames.length)] || 'Kepler'}-${id}`
    }
  }

  // Create planet mesh with generated parameters
  const createPlanet = (params: PlanetParams): THREE.Mesh => {
    // Convert parameters to uniforms format
    const uniforms = {
      type: { value: params.type },
      radius: { value: params.radius },
      amplitude: { value: params.amplitude },
      sharpness: { value: params.sharpness },
      offset: { value: params.offset },
      period: { value: params.period },
      persistence: { value: params.persistence },
      lacunarity: { value: params.lacunarity },
      octaves: { value: params.octaves },
      undulation: { value: params.undulation },
      ambientIntensity: { value: params.ambientIntensity },
      diffuseIntensity: { value: params.diffuseIntensity },
      specularIntensity: { value: params.specularIntensity },
      shininess: { value: params.shininess },
      lightDirection: { value: params.lightDirection },
      lightColor: { value: params.lightColor },
      bumpStrength: { value: params.bumpStrength },
      bumpOffset: { value: params.bumpOffset },
      color1: { value: params.color1 },
      color2: { value: params.color2 },
      color3: { value: params.color3 },
      color4: { value: params.color4 },
      color5: { value: params.color5 },
      transition2: { value: params.transition2 },
      transition3: { value: params.transition3 },
      transition4: { value: params.transition4 },
      transition5: { value: params.transition5 },
      blend12: { value: params.blend12 },
      blend23: { value: params.blend23 },
      blend34: { value: params.blend34 },
      blend45: { value: params.blend45 }
    }

    const material = new THREE.ShaderMaterial({
      uniforms,
      vertexShader: noiseFunctions + '\n' + planetVertexShader,
      fragmentShader: noiseFunctions + '\n' + planetFragmentShader,
    })

    // Use lower resolution for better performance - still looks good at distance
    const geometry = new THREE.SphereGeometry(1, 64, 64)
    geometry.computeTangents()
    
    return new THREE.Mesh(geometry, material)
  }

  // Setup Three.js scene for planet display - optimized for performance
  const setupPlanetScene = (container: HTMLElement, planet: THREE.Mesh) => {
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x000000)

    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000)
    camera.position.z = 50

    // Optimize renderer settings for performance
    const renderer = new THREE.WebGLRenderer({ 
      antialias: false, // Disable antialiasing for better performance
      powerPreference: "high-performance",
      stencil: false,
      depth: true
    })
    renderer.setSize(container.clientWidth, container.clientHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)) // Cap pixel ratio for performance
    renderer.outputColorSpace = THREE.SRGBColorSpace
    container.appendChild(renderer.domElement)

    scene.add(planet)

    // Performance optimized animation loop
    let animationId: number
    let lastTime = 0
    const targetFPS = 60
    const frameInterval = 1000 / targetFPS

    const animate = (currentTime: number) => {
      animationId = requestAnimationFrame(animate)
      
      // Throttle to target FPS for consistent performance
      if (currentTime - lastTime >= frameInterval) {
        planet.rotation.y += 0.002 // Slower rotation for smoother performance
        renderer.render(scene, camera)
        lastTime = currentTime
      }
    }

    // Handle resize with debouncing for performance
     let resizeTimeout: ReturnType<typeof setTimeout>
    const handleResize = () => {
      clearTimeout(resizeTimeout)
      resizeTimeout = setTimeout(() => {
        camera.aspect = container.clientWidth / container.clientHeight
        camera.updateProjectionMatrix()
        renderer.setSize(container.clientWidth, container.clientHeight)
      }, 100)
    }

    window.addEventListener('resize', handleResize)

    animate(0)

    // Enhanced cleanup function
    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', handleResize)
      clearTimeout(resizeTimeout)
      
      // Proper cleanup to prevent memory leaks
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement)
      }
      
      // Dispose of geometries and materials
      planet.geometry.dispose()
      if (planet.material instanceof THREE.Material) {
        planet.material.dispose()
      }
      
      renderer.dispose()
      renderer.forceContextLoss()
    }
  }

  return {
    generatePlanetParams,
    generateExoplanetData,
    createPlanet,
    setupPlanetScene
  }
}

// Utility functions for seeded randomization
function hashCode(str: string): number {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  return Math.abs(hash)
}

function seededRandom(seed: number) {
  let x = Math.sin(seed) * 10000
  return function() {
    x = Math.sin(x) * 10000
    return x - Math.floor(x)
  }
}