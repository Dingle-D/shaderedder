<template>
  <div class="flex-1 w-full bg-white">
    <div>
      <ControlComponent @control-changed="onControlChanged" :controls="uniform_controls" />
    </div>
  </div>
</template>

<script setup lang='ts'>
  import ControlComponent from '@/components/ControlComponent.vue'
  import {Uniform} from '@/common/types.ts'
  import {ref, watch} from 'vue'

  const props = defineProps<{
    uniforms: Uniforms[]
  }>()

  let world_controls = [
    {
      params: {test: true},
      label: "test",
      type: "bool",
      optional: null,
    },
  ]

  const object_controls = ref<object>([
    {
      params: {rotation: 0},
      label: "rotation",
      type: "float",
      optional: {step: 1, min: -180, max: 180},
    },
    {
      params: {model: 0},
      label: "model",
      optional: {options: {sphere: 'sphere', box: 'box', plane: 'plane'}},
      type: "enum",
    },
  ])

  const uniform_controls = ref<object>([])

  let prev_uniforms: Uniform[] = []

  // compares {} and [] by values
  function isSameValue(obj: any, arr: any): boolean {
    if (typeof obj === 'number' && typeof arr === 'number') return true

    const values = Object.values(obj);
    console.error("values obj:", values, values.length)
    console.error("values arr:", arr, arr.length)
    if (values.length !== arr.length) return false;

    //return values.every((val, i) => val === arr[i]);
    return true
  }

  watch(() => props.uniforms, (newUniforms) => {
    let updatedUniforms = []
    console.error("New uniforms: ", newUniforms);
    
    for (const val of newUniforms) {
      const existing = uniform_controls.value.find(obj => obj.label === val.name)
      if (existing && isSameValue(existing.params[val.name], val.value)) {
        console.error("Same value")
        updatedUniforms.push(existing)
      }
      else {
        console.error("New uniform!", val.name);
        if (typeof val.value === 'number') {
          const params = {[val.name]: val.value}
          updatedUniforms.push({params, label: val.name, type: 'float'})
        }
        else if (Array.isArray(val.value) && val.value.length === 2 && val.value.every(el => typeof el === "number")) {
          const params = {[val.name]: {x: val.value[0], y: val.value[1]}}
          updatedUniforms.push({params, label: val.name})
        } 
        else if (Array.isArray(val.value) && val.name.match(/[Cc]olor/) && val.value.every(el => typeof el === "number")) {
          if (val.value.length === 3) {
            const params = {[val.name]: {r: 0.0, g: 1.0, b: 0.5}}
            updatedUniforms.push({params, label: val.name, optional: {color: {type: "float"}}})
          } else if (val.value.length === 4) {
            const params = {[val.name]: {r: 0.0, g: 1.0, b: 0.5, a: 1.0}}
            updatedUniforms.push({params, label: val.name, optional: {color: {type: "float"}}})
          }
        }
        else if (Array.isArray(val.value) && val.value.every(el => typeof el === "number")) {
          if (val.value.length === 3) {
            const params = {[val.name]: {x: 0.0, y: 0.0, z: 0.0}}
            updatedUniforms.push({params, label: val.name})
          } else if (val.value.length === 4) {
            const params = {[val.name]: {x: 0.0, y: 0.0, z: 0.0, w: 0.0}}
            updatedUniforms.push({params, label: val.name})
          }
        }
      }
    }
    console.log("Updating uniforms (controls):", updatedUniforms)
    uniform_controls.value = updatedUniforms;
    console.log("Updated uniforms:", uniform_controls.value)
  });

  function onControlChanged(label: string, ev: object) {
    const uf = uniform_controls.value.find(obj => obj.label === label);
    if (uf) {
      uf.params[label] = ev;
      console.log("Changed field value. current uniforms:", uniform_controls)
    }
  }
</script>
