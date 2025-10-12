<template>
  <div ref="container" class="w-full h-full"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, watch, ref } from 'vue'
import * as Tweakpane from 'tweakpane'
import PaneRecrod from '@/common/types.ts'

interface ScriptItem {
  label: string
  type: string
  params: object
  optional: object | null
}

const props = defineProps<{
  title?: string 
  controls?: ScriptItem[]
}>()

const container = ref<HTMLElement | null>(null)
let pane: Tweakpane.Pane

const emit = defineEmits<{
  (e: 'control-changed', label: string, ev: object): void
}>()

onMounted(() => {
  if (!container.value) return

  // Создаем панель внутри контейнера
  pane = new Tweakpane.Pane({
    container: container.value,
    title: props.title,
  })

  updateControls();
  
  applyLightTheme()
})

onUnmounted(() => {
  pane.dispose()
})

function applyLightTheme() {
  const root = document.documentElement
  root.style.setProperty('--tp-font-family', 'monospace')
  root.style.setProperty('--tp-font-size', '14px')
  root.style.setProperty('--tp-base-background-color', '#ffffff')
  root.style.setProperty('--tp-base-shadow-color', 'rgba(0, 0, 0, 0.0)')
  root.style.setProperty('--tp-button-background-color', '#f0f0f0')
  root.style.setProperty('--tp-button-background-color-active', '#d0d0d0')
  root.style.setProperty('--tp-button-foreground-color', '#151515')
  root.style.setProperty('--tp-container-background-color', '#e5e5e5')
  root.style.setProperty('--tp-container-foreground-color', '#151515')
  root.style.setProperty('--tp-groove-foreground-color', '#151515')
  root.style.setProperty('--tp-label-text-color', '#111111')
  root.style.setProperty('--tp-input-background-color', '#e5e5e5')
  root.style.setProperty('--tp-input-foreground-color', '#151515')
  root.style.setProperty('--tp-label-foreground-color', '#151515')
  root.style.setProperty('--tp-monitor-background-color', '#ffffff')
  root.style.setProperty('--tp-monitor-foreground-color', '#151515')
}

function isArraysEqual<T>(a: T[], b: T[]): boolean {
  if (a.length !== b.length) return false;
  return a.every((val, i) => val === b[i]);
}

// удаляем элементы первого массива без совпадающих имен во втором
// для удаляемых элементов вызываем callback
function processAndFilter(arrayA, arrayB, callback) {
  const validLabels = new Set(arrayB.map(item => item.label));

  const filtered = arrayA.filter(item => {
    const shouldKeep = validLabels.has(item.label);
    if (!shouldKeep) {
      callback(item);
    }
    return shouldKeep;
  });

  console.error("Filtered: ", filtered)
  return filtered;
}

function processAndFilter2(arrayA, arrayB, callback) {
  
}

let currentControls = []

function addPaneElement(label: string, params: object, optional: object | null = null) {
  if (optional != null) {
    let input = pane.addInput(params, label, optional);
    input.on('change', (ev) => {
      onFieldChange(label, ev);
    });
    return input;
  } else {
    let input = pane.addInput(params, label);
    input.on('change', (ev) => {
      onFieldChange(label, ev);
    });
    return input;
  }
}

function updateControls() {
  if (!pane || !props.controls) {
    console.error("can't update controls");
    return;
  }
  processAndFilter(currentControls, props.controls, (toremove) => {
    toremove.descriptor.dispose();
  });
  processAndFilter(props.controls, currentControls, (toadd) => {
    console.add("Adding new element: ", toadd.params)
    const controlDesc = addPaneElement(toadd.label, toadd.params, toadd.optional);
    currentControls.push({descriptor: controlDesc, label: toadd.label, type: toadd.type});
  });
}

function updateControls2(controls) {
  if (!pane) {
    console.error("can't update controls");
    return;
  }
  console.log("currentControls: ", currentControls)
  console.log("NewControls: ", controls)
  processAndFilter(currentControls, [], (toremove) => {
    console.log("removing: ", toremove)
    toremove.descriptor.dispose();
    currentControls = currentControls.filter(e => e.label !== toremove.label)
  });
  console.error("Controls after remove:", currentControls);
  
  processAndFilter(controls, currentControls, (toadd) => {
    console.log("add: ", toadd)
    const controlDesc = addPaneElement(toadd.label, toadd.params, toadd.optional);
    currentControls.push({descriptor: controlDesc, label: toadd.label, type: toadd.type});
  });
  console.error("updating controls 2");
  
}

function onFieldChange(label: string, ev: object) {
  if (ev.last == true) {
    console.log(`Новое значение поля ${label} : ${ev.value}`);
    emit('control-changed', label, ev.value)
  }
}

watch(() => props.controls, updateControls2)

</script>

<style>
.tp-rotv {
  font-size: 14px !important;
}

.tp-lblv_v {
  min-width: 200px;
  width: 70% !important;
}
</style>
