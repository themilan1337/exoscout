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
    
    // smth similar to earth
    const baseParams = {
      type: 2,
      radius: 20.0,
      amplitude: 1.19,
      sharpness: 2.6,
      offset: -0.016,
      period: 0.6,
      persistence: 0.484,
      lacunarity: 1.8,
      octaves: 10,
      undulation: 0.0,
       ambientIntensity: 0.3, //  more lights 
       diffuseIntensity: 2.5, // difflights increased
       specularIntensity: 1.5, // reduced specular to avoid overbrightness
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
    
    // variations to make each planet unique but still earth like
    return {
      ...baseParams,
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

  // mock data with randomness
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

  // Create animated stars background
  const createStarsBackground = (count: number = 2000): THREE.Points => {
    const starsGeometry = new THREE.BufferGeometry()
    const starPositions = new Float32Array(count * 3)
    const starSizes = new Float32Array(count)
    
    // Generate random star positions and sizes
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      // Create stars in a large sphere around the scene
      starPositions[i3] = (Math.random() - 0.5) * 2000
      starPositions[i3 + 1] = (Math.random() - 0.5) * 2000
      starPositions[i3 + 2] = (Math.random() - 0.5) * 2000
      
      // Vary star sizes for more realistic look
      starSizes[i] = Math.random() * 2 + 0.5
    }
    
    starsGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3))
    starsGeometry.setAttribute('size', new THREE.BufferAttribute(starSizes, 1))
    
    // Create star material with size attenuation
    const starsMaterial = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 2,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.8
    })
    
    return new THREE.Points(starsGeometry, starsMaterial)
  }

  // Setup Three.js scene for planet display - optimized for performance
  const setupPlanetScene = (container: HTMLElement, planet: THREE.Mesh) => {
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x000000) // Very dark blue instead of pure black
    
    // Add animated stars background
    const stars = createStarsBackground(1500)
    scene.add(stars)

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

    // Add additional lighting to the scene
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4) // Soft ambient light
    scene.add(ambientLight)
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2)
    directionalLight.position.set(1, 1, 1)
    scene.add(directionalLight)
    
    // Add a second light from the opposite side for better illumination
    const backLight = new THREE.DirectionalLight(0xffffff, 0.6)
    backLight.position.set(-1, -1, -1)
    scene.add(backLight)

    scene.add(planet)

    // Mouse interaction variables
    let isMouseDown = false
    let mouseX = 0
    let mouseY = 0
    let targetRotationX = 0
    let targetRotationY = 0
    let currentRotationX = 0
    let currentRotationY = 0

    // Raycaster for detecting planet hover
    const raycaster = new THREE.Raycaster()
    const mouse = new THREE.Vector2()

    // Mouse event handlers for planet interaction
    const handleMouseDown = (event: MouseEvent) => {
      isMouseDown = true
      mouseX = event.clientX
      mouseY = event.clientY
      renderer.domElement.style.cursor = 'grabbing'
    }

    const handleMouseMove = (event: MouseEvent) => {
      // Update mouse position for raycasting
      const rect = renderer.domElement.getBoundingClientRect()
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

      // Check if hovering over planet when not dragging
      if (!isMouseDown) {
        raycaster.setFromCamera(mouse, camera)
        const intersects = raycaster.intersectObject(planet)
        
        if (intersects.length > 0) {
          renderer.domElement.style.cursor = 'grab'
        } else {
          renderer.domElement.style.cursor = 'default'
        }
        return
      }
      
      const deltaX = event.clientX - mouseX
      const deltaY = event.clientY - mouseY
      
      targetRotationY += deltaX * 0.01
      targetRotationX += deltaY * 0.01
      
      // Clamp vertical rotation to prevent flipping
      targetRotationX = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, targetRotationX))
      
      mouseX = event.clientX
      mouseY = event.clientY
    }

    const handleMouseUp = () => {
      isMouseDown = false
      // Check if still hovering over planet after mouse up
      raycaster.setFromCamera(mouse, camera)
      const intersects = raycaster.intersectObject(planet)
      renderer.domElement.style.cursor = intersects.length > 0 ? 'grab' : 'default'
    }

    const handleWheel = (event: WheelEvent) => {
      event.preventDefault()
      camera.position.z += event.deltaY * 0.01
      camera.position.z = Math.max(25, Math.min(100, camera.position.z)) // Clamp zoom
    }

    // Add event listeners
    renderer.domElement.addEventListener('mousedown', handleMouseDown)
    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('mouseup', handleMouseUp)
    renderer.domElement.addEventListener('wheel', handleWheel)

    // Performance optimized animation loop
    let animationId: number
    let lastTime = 0
    const targetFPS = 60
    const frameInterval = 1000 / targetFPS

    const animate = (currentTime: number) => {
      animationId = requestAnimationFrame(animate)
      
      // Throttle to target FPS for consistent performance
      if (currentTime - lastTime >= frameInterval) {
        // Smooth rotation interpolation
        currentRotationX += (targetRotationX - currentRotationX) * 0.1
        currentRotationY += (targetRotationY - currentRotationY) * 0.1
        
        planet.rotation.x = currentRotationX
        planet.rotation.y = currentRotationY
        
        // Auto-rotate when not interacting
        if (!isMouseDown) {
          targetRotationY += 0.002
        }
        
        // Animate stars - slow rotation for depth effect
        stars.rotation.x += 0.0001
        stars.rotation.y += 0.0002
        
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
      
      // Remove mouse event listeners
      renderer.domElement.removeEventListener('mousedown', handleMouseDown)
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseup', handleMouseUp)
      renderer.domElement.removeEventListener('wheel', handleWheel)
      
      // Proper cleanup to prevent memory leaks
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement)
      }
      
      // Dispose of geometries and materials
      planet.geometry.dispose()
      if (planet.material instanceof THREE.Material) {
        planet.material.dispose()
      }
      
      // Dispose stars
      stars.geometry.dispose()
      if (stars.material instanceof THREE.Material) {
        stars.material.dispose()
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