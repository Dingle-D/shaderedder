<template>
  <splitpanes class="default-theme" style="height: 100vh; width: 100vw;">
    <!-- Левая панель -->
    <pane size="40" class="flex flex-col h-full">
      <div class="bg-white w-full flex flex-col px-2 py-2 space-y-2">
        <div class="flex bg-white w-full h-14 items-center px-2">
          <img class="h-12 aspect-square" src="@/assets/icons/logo.svg" alt="icon"/>
        </div>
        <div class="flex flex-col">
          <button class="flex items-center space-x-2 hover:bg-gray-200 w-full px-2 py-1 rounded-md text-sm font-medium">
            <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" aria-hidden="true">
              <FilePath/>
            </svg>
            <p>Save</p>
          </button>
          <button class="flex items-center space-x-2 hover:bg-gray-200 w-full px-2 py-1 rounded-md text-sm font-medium">
            <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" aria-hidden="true">
              <FilePath/>
            </svg>
            <p>Export</p>
          </button>
          <button class="flex items-center space-x-2 hover:bg-gray-200 w-full px-2 py-1 rounded-md text-sm font-medium">
            <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" aria-hidden="true">
              <InfoPath/>
            </svg>
            <p>Info</p>
          </button>
        </div>
      </div>
      <hr/>
      <div class="flex flex-1 justify-center h-full w-full">
        <EditorControlsLayout :uniforms="uniforms"/>
      </div>
    </pane>

    <!-- Правая часть (два окна по вертикали) -->
    <pane size="60">
      <splitpanes horizontal>
        <pane size="50">
          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
            <EditorLayout @code-change="onCodeChange" :highlightLines="highlighted" :content="initialFragmentShader" />
          </div>
        </pane>
        <pane size="50">
          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
            <div v-if="error" class="bg-red-200 text-red-700 w-full whitespace-pre-line font-[monospace] text-[14px]">
              {{error}}
            </div>
            <RenderLayout @compile="onCompile" :fragmentShader='fragmentSource' :uniforms='uniforms'/>
          </div>
        </pane>
      </splitpanes>
    </pane>
  </splitpanes>
</template>

<script setup lang='ts'>
import EditorControlsLayout from "@/components/layouts/ControlsLayout.vue"
import EditorLayout from "@/components/layouts/EditorLayout.vue"
import ViewportLayout from "@/components/layouts/ViewportLayout.vue"
import RenderLayout from "@/components/layouts/RenderLayout.vue"
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Uniform, Status } from '@/common/types.ts'
import ApiService from '@/common/api.service'

// refs
const highlighted = ref<number[]>([]);
const fragmentSource = ref<string>("");
const uniforms = ref<Uniform[]>([]);
const error = ref<string | null>(null);

let reservedUniforms: string[] = ['uTime', 'uTimeDelta', 'uResolution']

let initialFragmentShader = ""


const isFileMenuOpen = false;


onMounted(() => {
  const route = useRoute()
  let shid = route.params.id;
  console.log("Shader index at start:", shid);
  if (!shid) {
    shid = Math.floor(Math.random() * 6) + 1;
  }
  console.log("Shader index: ", shid);
  loadShader(shid);
})

function parseUniformsString(uniformsString: String) {
  console.log("Uniforms string: ", uniformsString)
  const uforms = JSON.parse(uniformsString)
  for (const uform in uforms) {
    if (!isUniform(uform)) throw new Error(`Invalid uniform: ${uform}`)
  }
  return uforms
}

async function loadShader(shaderId: number) {
    if (!shaderId) {
      console.error("Shader id is not set!");
    }
    const response = await ApiService.query(`/shader/download/${shaderId}`, {responseType: 'blob'})
    const blob = response.data
    console.log("Response:", response)
    console.log("Blob in memory:", blob)
    let uniformsString = response.headers['Uniforms']
    if (!uniformsString) {
      const r1 = await ApiService.query(`/shader/meta/${shaderId}`)
      console.log("meta response:", r1)
      uniformsString = r1.data.Uniforms
    }
    try {
      uniforms.value = parseUniformsString(uniformsString)
      initialFragmentShader = await blob.text()
      fragmentSource.value = initialFragmentShader
    } catch (error) {
      uniforms.value = []
      fragmentSource.value = initialFragmentShader
      console.error(error);
    }

    console.log("Source:", fragmentSource.value)
    console.log("Uniforms:", uniforms.value)
}

function onCodeChange(code: string) {
  let uforms = parseUniforms(code)
  updateUniforms(uforms)
  fragmentSource.value = code;
}

// params:
//    code: fragment shader source code 
//    reserved: names of reserved uniforms
function onRendererInit(code: string, reserved: string[]) {
  console.log("ON render init executed")
  fragmentSource.value = code;
  reservedUniforms = reserved;
}

function onCompile(status: Status) {
  console.log("onCompile emited:", status)
  if (status && status.success === false) {
    console.log("shader compilation failed")
    if (status.message && status.message != null) {
      error.value = status.message
      highlighted.value = parseLinesWithErrors(status.message)
    }
  }
  else if (status && status.success === true) {
    console.log("shader compilation success")
    error.value = null
    highlighted.value = []
  }
}

function parseUniforms(code: string) {
  type GLSLType =
  | "float"
  | "vec2"
  | "vec3"
  | "vec4";

  const regex = /uniform\s+(int|uint|float|vec[2-4])\s+(\w+)\s*;/g;
  const uniforms: {type: GLSLType; name:string }[] = [];

  let match;
  while ((match = regex.exec(code)) !== null) {
    const type = match[1] as GLSLType;
    const name = match[2];
    if (!reservedUniforms.includes(name))  uniforms.push({ type, name });
  }

  return uniforms;
}

function parseLinesWithErrors(error: string) {
  const regex = /ERROR:\s*0:(\d+):/g;
  let match;
  const lines: number[] = [];

  while ((match = regex.exec(error)) !== null) {
    lines.push(Number(match[1]));
  }

  return lines;
}

function updateUniforms(uforms) {
  let newUniforms: Uniform[] = []
  console.log("to parse:", uforms)

  for (const val of uforms) {
    
    console.log(val)

    let newValue
    if (val.type === "float") {
      newValue = 0
    } else if (val.type === 'vec2') {
      newValue = [0,0]
    } else if (val.type === 'vec3') {
      newValue = [0,0,0]
    } else if (val.type === 'vec4') {
      newValue = [0,0,0,0]
    }

    const existing = uniforms.value.find(obj => obj.name === val.name)
    if (existing && existing.value.length === newValue.length) {
      newUniforms.push({name: existing.name, value: existing.value})
      continue
    }

    newUniforms.push({name: val.name, value: newValue});
  }

  uniforms.value = newUniforms;
  console.log("parsed uniforms:", newUniforms)
}

/*
const initialFragmentShader = 
`#version 300 es
precision highp float;
precision highp int;

out vec4 fragColor;

void mainImage( out vec4 fragColor)
{
    vec3 col = vec3(0.8f, 0.8f, 0.8f);

    // Output to screen
    fragColor = vec4(col,1.0);
}

void main() {
    mainImage(fragColor);
}`;
*/

</script>

<script lang='ts'>
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'

import FilePath from '@/components/icons/file.vue'
import InfoPath from '@/components/icons/info.vue'

export default {
  name: 'EditorView',
  components: { Splitpanes, Pane },
}
</script>

<style lang="postcss">
.splitpanes--vertical > .splitpanes__splitter {
  min-width: 6px !important;
  background: transparent !important;
  border: none !important;
  border-right: 3px dashed #e0e0e0 !important;
}

.splitpanes--horizontal > .splitpanes__splitter {
  min-height: 6px !important;
  background: transparent !important;
  border: none !important;
  border-top: 3px dashed #e0e0e0 !important;
}

.splitpanes__splitter::before,
.splitpanes__splitter::after,
.splitpanes__splitter > * {
  display: none !important;
}
</style>
