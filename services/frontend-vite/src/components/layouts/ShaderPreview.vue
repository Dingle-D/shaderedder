<template>
  <RenderLayout :fragmentShader="frag_shader" :uniforms="uniforms"/>
</template>

<script setup lang="ts">
  import {onMounted, ref, watch} from "vue"
  import RenderLayout from "@/components/layouts/RenderLayout.vue"
  import ApiService from "@/common/api.service"
  import {Uniform, isUniform, Status} from '@/common/types.ts'

  const props = defineProps<{
    shaderId: number
  }>()

  const uniforms = ref<Uniform[]>([])
  const frag_shader = ref<String>("")

  onMounted(() => {
    loadShader(props.shaderId);
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
      frag_shader.value = await blob.text()
    } catch (error) {
      uniforms.value = []
      frag_shader.value = ""
      console.error(error);
    }

    console.log("Source:", frag_shader.value)
    console.log("Uniforms:", uniforms.value)
  }
</script>
