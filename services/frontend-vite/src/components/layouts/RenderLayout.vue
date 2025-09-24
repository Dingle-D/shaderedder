<template>
  <canvas ref="canvas" class="w-full h-full rounded rounded-md"> </canvas>
</template>

<script setup lang="ts">
  import * as THREE from 'three'
  import {onMounted, onBeforeUnmount, watch, ref} from 'vue'
  import {Uniform, UniformValue, isUniformValue, Status} from '@/common/types.ts'

  const props = defineProps<{
    fragmentShader: string,
    uniforms: Uniform[]
  }>()

  const emit = defineEmits<{
    (e: 'compile', status: Status): void
    (e: 'init', code: string, reservedUniforms: string[]): void
  }>();

  const canvas = ref<HTMLCanvasElement | null>(null)

  let gl;
  let program;
  let startTime; 
  let lastTime;
  let animationFrameId: number 
  let errorDisplay;

  let userDefinedUniforms

  onMounted(() => {
    init();
  })

  watch (() => props.uniforms, (newUniforms) => {
    let udu = {}

    for (const key in newUniforms) {
      if (!isUniformValue(newUniforms[key].value)) {
        console.log("NOT UNIFORM:", key)
        continue
      }
      udu[key] = newUniforms[key]
      console.log("UNIFORM:", key, ", UDU: ", udu)
    }

    userDefinedUniforms = udu;
    console.log("RECEIVED UNIFORMS:", newUniforms)
    console.log("USER DEFINED UNIFORMS:", userDefinedUniforms)
  })

  watch (() => props.fragmentShader, (code) => {
    
    try {
      compileShader(defaultVertexShaderSource, code);
      emit('compile', {success: true, message: ''});
    }
    catch (error) {
      emit('compile', {success: false, message: error.message});
    }
  })

  function initGL() {
    if (!canvas) {
      console.error("Canvas is not set!");
      return;
    }

    gl = canvas.value.getContext('webgl2')
    if (!gl) {
      throw new Error('WebGL2 is not supported');
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
  }

  function resizeCanvas() {
    if (canvas.value && canvas.value.parentElement) {
      const width = canvas.value.parentElement.clientWidth;
      const height = canvas.value.parentElement.clientHeight;

      canvas.value.width = width;
      canvas.value.height = height;
      gl.viewport(0, 0, canvas.value.width, canvas.value.height)
    }
  }

  function createShader(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      const error = gl.getShaderInfoLog(shader);
      gl.deleteShader(shader);
      throw new Error(error);
    }

    return shader;
  }

  function compileShader(vsource, fsource) {
    const vertexShader = createShader(gl.VERTEX_SHADER, vsource)
    const fragmentShader = createShader(gl.FRAGMENT_SHADER, fsource)

    const newProgram = gl.createProgram();
    gl.attachShader(newProgram, vertexShader);
    gl.attachShader(newProgram, fragmentShader);
    gl.linkProgram(newProgram)

    if (!gl.getProgramParameter(newProgram, gl.LINK_STATUS)) {
      const error = gl.getProgramInfoLog(newProgram);
      gl.deleteProgram(newProgram);
      throw new Error(error);
    }

    // clean up old program if it exists
    if (program) {
      gl.deleteProgram(program)
    }
    program = newProgram;

    /*
    const positions = new Float32Array([
      -1, -1,
      1, -1,
      -1, 1, 1, 1
    ]);

    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
    const positionAttributeLocation = gl.getAttribLocation(program, 'position');
    gl.enableVertexAttribArray(positionAttributeLocation);
    gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
    */ 
    const vertices = new Float32Array([
      -1, -1,   0, 0,
      1, -1,   1, 0,
      -1,  1,   0, 1,
      1,  1,   1, 1
    ]);

    const vertexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

    const stride = 4 * 4; // 4 float (x,y,u,v)

    // --- позиция ---
    const positionAttributeLocation = gl.getAttribLocation(program, "position");
    gl.enableVertexAttribArray(positionAttributeLocation);
    gl.vertexAttribPointer(
      positionAttributeLocation,
      2, gl.FLOAT, false,
      stride,
      0
    );

    // --- uv ---
    const uvAttributeLocation = gl.getAttribLocation(program, "uv");
    gl.enableVertexAttribArray(uvAttributeLocation);
    gl.vertexAttribPointer(
      uvAttributeLocation,
      2, gl.FLOAT, false,
      stride,
      2 * 4
    );
  }

  function render(time) {
    if (canvas.value == null) return 

    if (!startTime) startTime = time;
    if (!lastTime) lastTime = time;

    const currentTime = (time - startTime) * 0.001;
    const deltaTime = (time - lastTime) * 0.001;
    lastTime = time;

    gl.useProgram(program);

    const defaultUniforms = {
      uTime: gl.getUniformLocation(program, 'uTime'),
      uTimeDelta: gl.getUniformLocation(program, 'uTimeDelta'),
      uResolution: gl.getUniformLocation(program, 'uResolution'),
    };

    const width = canvas.value.parentElement.clientWidth;
    const height = canvas.value.parentElement.clientHeight;

    gl.uniform1f(defaultUniforms.uTime, currentTime);
    gl.uniform1f(defaultUniforms.uTimeDelta, deltaTime);
    gl.uniform3f(defaultUniforms.uResolution, width, height, 1.0);

    updateUserDefinedUniforms(program)

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    animationFrameId = requestAnimationFrame(render);
  }

  function updateUserDefinedUniforms(program, ignore = []) {
    for (const key in userDefinedUniforms) {
      if (ignore.includes(key)) continue

      const loc = gl.getUniformLocation(program, key)
      const value = userDefinedUniforms[key]

      if (!loc) continue

      if (typeof value === 'number') {
        gl.uniform1f(loc, value)
      }
      else if (Array.isArray(value) && value.length === 2 && value.every(el => typeof el === "number")) {
        gl.uniform2f(loc, value)
      }
      else if (Array.isArray(value) && value.length === 3 && value.every(el => typeof el === "number")) {
        gl.uniform3f(loc, value)
      }
      else if (Array.isArray(value) && value.length === 4 && value.every(el => typeof el === "number")) {
        gl.uniform4f(loc, value)
      }
    }
  }

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  async function init() {
    initGL();
    try {
      compileShader(defaultVertexShaderSource, defaultFragmentShaderSource)
      emit('init', defaultFragmentShaderSource, ['uTime', 'uTimeDelta', 'uResolution'])
      animationFrameId = requestAnimationFrame(render);
    }
    catch (error) {
      console.error(error.message);
    }
  }
;

  const defaultVertexShaderSource = `#version 300 es 
    in vec2 uv;
    in vec4 position;

    out vec2 vUv;
    out vec4 vPosition;

    void main() {
      gl_Position = position;
      vUv = uv;
      vPosition = gl_Position;
    }`;

  const defaultFragmentShaderSource =  `#version 300 es
  precision highp float;
  precision highp int;

  out vec4 fragColor;

  void main() {
      vec3 color = vec3(0.9f, 0.9f, 0.9f);
      fragColor = vec4(color, 1.0f);
  }`;
</script>

<script lang="ts">
  export default {
    name: "RenderLayout"
  }
</script>
