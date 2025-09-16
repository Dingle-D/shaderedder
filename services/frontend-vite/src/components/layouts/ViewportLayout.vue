<template>
  <div id="scene-container" class="w-full h-full" ref="CONTAINER"></div>
</template>

<script setup lang="ts">
  import * as THREE from 'three'
  import { nextTick, onMounted, onUnmounted, ref } from 'vue'
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

  const minFov = 20;
  const maxFov = 70;
  const minDistance = 0.6;
  const maxDistance = 4;

  enum Mode {
    _2d_,
    _3d_,
    _ns_
  }

  interface CameraOptions {
    fov: number;
    distance: number;
  }

  function isCameraOptionsValid(arg: any): arg is CameraOptions {
    let isValid = arg && arg.fov && arg.distance;
    isValid &= (arg.fov >= minFov) && (arg.fov <= maxFov);
    isValid &= (arg.Distance >= minDistance) && (arg.Distance <= maxDistance);
    return isValid;
  }

  interface LightOptions {
    color: integer;
    intencivity: float;
  }

  function isLightOptionsValid(arg: any): arg is LightOptions {
    let isValid = arg && arg.color && arg.intencivity;
    isValid &= (arg.color >= 0) && (arg.color <= 0xffffff);
    isValid &= (arg.intencivity >= 0) && (arg.intencivity <= 1);
  }

  type UniformType = 
    | number

  // common
  const CONTAINER = ref<HTMLDivElement | null>(null)
  const SCENE = new THREE.Scene()
  const RENDERER = new THREE.WebGLRenderer({antialias: true})
  let CONTROLS: OrbitControls
  let MODE: Mode = Mode._ns_
  let CURRENT_CAMERA

  let CONTAINER_WIDTH: number 
  let CONTAINER_HEIGHT: number

  let VERTEX_SHADER: string
  let FRAGMENT_SHADER: string
  let UNIFORMS: object

  //const DEFAULT_VERTEX_SHADER = `void main() {gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);}`
  const DEFAULT_VERTEX_SHADER2 = `
  uniform vec4 modelViewMatrix;
    varying vec3 vNormal;
    varying vec3 vViewDir;
    void main() {
      // нормаль в мировом пространстве
      vNormal = normalize(normalMatrix * normal);
      // направление камеры
      vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
      vViewDir = normalize(-mvPosition.xyz);
      gl_Position = projectionMatrix * mvPosition;
    }
  `
  const DEFAULT_FRAGMENT_SHADER2 = `
    uniform vec3 uColor;
    uniform vec3 uOutlineColor;
    uniform float uOutlineStrength;
    varying vec3 vNormal;
    varying vec3 vViewDir;

    void main() {
      // cos угла между нормалью и направлением на камеру
      float edge = 1.0 - abs(dot(vNormal, vViewDir));
      
      if (edge > uOutlineStrength) {
        gl_FragColor = vec4(uOutlineColor, 1.0); // контур
      } else {
        gl_FragColor = vec4(uColor, 1.0);        // основной цвет
      }
    }
  `
  const DEFAULT_VERTEX_SHADER = `#version 300 es
    in vec3 position;
    in vec3 normal;
    in vec2 uv;

    uniform mat4 modelViewMatrix;
    uniform mat4 projectionMatrix;

    out vec2 vUv;
    out vec3 vNormal;

    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `
  const DEFAULT_FRAGMENT_SHADER = `#version 300 es
    precision highp float;
    precision highp int;
    #define EPSILON 0.05

    in vec2 vUv;
    in vec3 vNormal;

    out vec4 outColor;

    void main() {
        if ((fract(vUv.x * 8.0) < EPSILON)
            || (fract(vUv.y * 8.0) < EPSILON)) {
            outColor = vec4(vec3(0.0), 1.0);
        } else {
            outColor = vec4(1.0);
        }
    }
  `
  const DEFAULT_UNIFORMS = {}

  const DEFAULT_SHADER_MATERIAL =  new THREE.RawShaderMaterial({
    uniforms: DEFAULT_UNIFORMS,
    vertexShader: DEFAULT_VERTEX_SHADER,
    fragmentShader: DEFAULT_FRAGMENT_SHADER,
    glslVersion: THREE.GLSL3
  })

  const DEFAULT_MATERIAL = new THREE.MeshStandardMaterial({color: 0xff0f0f})

  let LAST_USED_SHADER: THREE.RawShaderMaterial

  // ortographic scene
  let CAMERA_2D: THREE.OrthographicCamera
  let QUAD: THREE.Mesh

  // perspective scene
  let CAMERA_3D: THREE.PerspectiveCamera
  let MESH: thee.Mesh 
  let CAMERA_OPTIONS: CameraOptions
  let AMBIENT_OPTIONS: LightOptions
  let DIRECTIONAL_OPTIONS: LightOptions
  let AMBIENT_LIGHT: THREE.AmbientLight
  let DIRECTIONAL_LIGHT: THREE.DirectionalLight

  let animationFrameId: number


  let keyHandler
  onMounted(async () => {
    await nextTick()
    if (!CONTAINER.value) {
      console.error("not found three.js viewport container")
      return
    }

    const width = CONTAINER.value.clientWidth
    const height = CONTAINER.value.clientHeight

    RENDERER.setSize(width, height)
    CONTAINER.value.appendChild(RENDERER.domElement)

    CAMERA_2D = new THREE.OrthographicCamera(-1, 1, 1, -1, -10, 10)
    CAMERA_2D.position.set(0,0,-1)

    CAMERA_3D = new THREE.PerspectiveCamera(90, width/height, 0.1, 100)
    CAMERA_3D.position.set(0, 0, -3);

    // init orbit controls for 3d mode
    CONTROLS = new OrbitControls(CAMERA_3D, RENDERER.domElement)
    CONTROLS.enableDamping = true 

    // init lights for 3d mode
    AMBIENT_LIGHT = new THREE.AmbientLight(0xffffff, 1)
    DIRECTIONAL_LIGHT = new THREE.DirectionalLight(0xffffff, 1)
    DIRECTIONAL_LIGHT.position.set(1, 1, 1)

    QUAD = new THREE.Mesh(
      new THREE.PlaneGeometry(2, 2),
      DEFAULT_SHADER_MATERIAL
    )

    setSceneBox()
    SCENE.background = new THREE.Color(0xf0f0f0)

    const animate = () => {
      if (CONTAINER.value != null) {
        const width = CONTAINER.value.clientWidth
        const height = CONTAINER.value.clientHeight
        if (CONTAINER_HEIGHT != height || CONTAINER_WIDTH != width) {
          updateViewportSize(width, height)
        }
      }
      animationFrameId = requestAnimationFrame(animate);
      CONTROLS.update();
      RENDERER.render(SCENE, CURRENT_CAMERA);
    };
    
    animate();

    keyHandler = (event) => {
      if (event.repeat) return // игнорируем автоповтор
      switch (event.code) {
        case "Digit1":
          console.log("set sphere")
          setSceneSphere()
          break
        case "Digit2":
          console.log("set box")
          setSceneBox()
          break
        case "Digit3":
          console.log("set plane")
          setScenePlane()
          break
      }
    }

    window.addEventListener('keydown', keyHandler)
    const material = new THREE.RawShaderMaterial({
      uniforms: {
        uColor: { value: new THREE.Color(0xffffff) },   // основной цвет
        uOutlineColor: { value: new THREE.Color(0x000000) }, // цвет обводки
        uOutlineStrength: { value: 0.3 } // порог (чем больше, тем толще линия)
      },
      vertexShader: DEFAULT_VERTEX_SHADER,
      fragmentShader: DEFAULT_FRAGMENT_SHADER
    })
    //setShaderMaterial(material)
    const gl = RENDERER.getContext()
    checkProgram(gl, DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER)
    
  })

  onUnmounted(() => {
    CONTROLS?.dispose()
    RENDERER?.dispose()
    window.removeEventListener('keydown', keyHandler)
  })


  function setSceneSphere() {
    setShapeSphere()
    setScene3D()
    CURRENT_CAMERA = CAMERA_3D
  }

  function setSceneBox() {
    setShapeBox()
    setScene3D()
    CURRENT_CAMERA = CAMERA_3D
  }

  function setScenePlane() {
    //setShapeQuad()
    setScene2D()
    CURRENT_CAMERA = CAMERA_2D
  }

  function updateViewportSize(w: number, h: number) {
    RENDERER.setSize(w, h)

    CAMERA_3D.aspect = w / h;
    CAMERA_3D.updateProjectionMatrix();

    CAMERA_2D.left   = -w / 2;
    CAMERA_2D.right  = w / 2;
    CAMERA_2D.top    = h / 2;
    CAMERA_2D.bottom = -h / 2;
    CAMERA_2D.updateProjectionMatrix();

    QUAD.geometry.dispose()
    QUAD.geometry = new THREE.PlaneGeometry(w, h)
  }

  function setShapeSphere() {
    if (MESH) {
      console.log("Changing geometry")
      MESH.geometry.dispose()
      MESH.geometry = new THREE.SphereGeometry(1, 64, 32)
    }
    else {
      console.log("Creating mesh")
      MESH = new THREE.Mesh(
        new THREE.SphereGeometry(1, 64, 32),
        DEFAULT_SHADER_MATERIAL
      )
    }
      console.log(MESH.position)
  }

  function setShapeBox() {
    if (MESH) {
      console.log("Changing geometry")
      MESH.geometry.dispose()
      MESH.geometry = new THREE.BoxGeometry(2,2,2)
    }
    else {
      console.log("Creating mesh")
      MESH = new THREE.Mesh(
        new THREE.BoxGeometry(2,2,2),
        DEFAULT_SHADER_MATERIAL
      )
    }
  }

  function setAmbientLight(options: LightOptions) {
    if (!AMBIENT_LIGHT || !isLightOptionsValid(options)) {
      console.error("Ambient light is not initialized or options invalid")
      return
    }
    AMBIENT_LIGHT.intencivity = options.intencivity
    AMBIENT_LIGHT.color.set(options.color)
  }

  function setDirectedLight(options: DirectionalOptions) {
    if (!DIRECTIONAL_LIGHT || !isLightOptionsValid(options)) {
      console.error("Directional light is not initialized or options invalid")
      return
    }
    DIRECTIONAL_LIGHT.intencivity = options.intencivity
    DIRECTIONAL_LIGHT.color.set(options.color)
  }

  function setDirectedPosition(pos: Vector3) {
    if (!DIRECTIONAL_LIGHT || !isVector3(pos)) {
      console.error("Directional light is not initialized or position is incorrect")
      return
    }
    DIRECTIONAL_LIGHT.position.set(pos.x, pos.y, pos.z)
  }

  function setDirectedTarget(target: THREE.Mesh) {
    if (!DIRECTIONAL_LIGHT || !target) {
      console.error("Directional light is not initialized or target not set")
      return
    }
    DIRECTIONAL_LIGHT.target = target
  }

  // clears scene and adds 3d scene objects (except mesh)
  function setScene3D(ambientOptions: AMBIENT_OPTIONS, directionalOptions: DIRECTIONAL_OPTIONS) {
    if (!SCENE) {
      console.error("Failed to set 3D scene.")
      return
    }
    SCENE.clear()
    SCENE.add(AMBIENT_LIGHT)
    SCENE.add(DIRECTIONAL_LIGHT)
    SCENE.add(CAMERA_3D)
    if (!MESH) setShapeSphere()
    SCENE.add(MESH)
  }

  function setScene2D() {
    if (!SCENE || MODE === Mode._2d_) {
      console.error("Failed to set 2D scene.")
      return
    }
    SCENE.clear()
    SCENE.add(CAMERA_2D)
    SCENE.add(QUAD)
  }

  function getCompilationErrors(gl, source, type) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      const log = gl.getShaderInfoLog(shader);
      const typeName = type === gl.VERTEX_SHADER ? "VERTEX" : "FRAGMENT";
      return `${typeName}\n${log}`;
    }
    return null;
  }

  function validateShaderProgram(renderer, vertexSource, fragmentSource) {
    const gl = renderer.getContext();

    const vErr = getCompilationErrors(gl, vertexSource, gl.VERTEX_SHADER);
    const fErr = getCompilationErrors(gl, fragmentSource, gl.FRAGMENT_SHADER);

    const errors = {};
    if (vErr) errors.vertex = vErr;
    if (fErr) errors.fragment = fErr;

    return errors;
  }


  function setShaderMaterial(materia: THREE.RawShaderMaterial) {
    if (!MESH || !QUAD) {
      console.error("Can't set shader material: mesh is not set.");
      return
    }
    const originalError = console.error
    const originalMaterial = MESH.material

    //const material = new THREE.RawShaderMaterial({
    //  vertexShader: DEFAULT_VERTEX_SHADER,
    //  fragmentShader: DEFAULT_FRAGMENT_SHADER
    //})

    console.log("Changing material...")
    let errors = []

    console.error = (...args) => {
      errors.push(args.join(" "))
    }

    //MESH.material = material
    //RENDERER.render(SCENE, CURRENT_CAMERA)
    if (errors.length !== 0) {
      console.log("Has errors: ", errors);
      MESH.material = originalMaterial
      material.dispose()
    }
    else {
      console.log("All good")
      originalMaterial.dispose()
    }

    console.error = originalError
  }

  function checkShader(gl, source, type) {
  // создаём шейдер
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  // проверяем статус
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const log = gl.getShaderInfoLog(shader);
    console.error(
      `Ошибка компиляции ${type === gl.VERTEX_SHADER ? "вершинного" : "фрагментного"} шейдера:`,
      log
    );
    console.log("Код шейдера:\n", source);
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

function checkProgram(gl, vertexSource, fragmentSource) {
  const vs = checkShader(gl, vertexSource, gl.VERTEX_SHADER);
  const fs = checkShader(gl, fragmentSource, gl.FRAGMENT_SHADER);
  if (!vs || !fs) return null;

  // создаём программу
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);

  // проверяем линковку
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const log = gl.getProgramInfoLog(program);
    console.error("Ошибка линковки программы:", log);
    return null;
  }

  console.log("✅ Шейдеры успешно скомпилированы и связаны!");
  return program;
}


</script>

<script lang="ts">
export default {
  name: 'ViewportLayout'
}
</script>
