<template>
  <div>
    <div class="flex space-x-4 px-16 py-6 border-b">
      <img class="aspect-square w-32 mr-6" 
           src="https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg" 
           alt="PROFILE IMG"/>
      <div>
        <h3 class="text-3xl mb-4"> {{ name }} </h3>
        <button class="hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900"> 
          <p class="text-xs">EDIT PROFILE</p>
        </button>
      </div>
    </div>
    <div class="px-16 py-6">
      <div class="flex space-x-4 justify-center">
        <button
          v-for="item in menu"
          :key="item.key"
          @click="changeTabAndLayout(item.key, item.comp)"
          class="px-4 py-2 rounded-lg border text-sm text-left transition-all duration-150"
          :class="selected === item.key
            ? 'bg-gray-900 text-white border-gray-900'
            : 'bg-white text-gray-800 border-gray-600 hover:bg-gray-100'"
        >
          {{ item.label }}
        </button>
      </div>
      <div class="full-w flex">
        <component :is="tab" />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, markRaw } from 'vue'
  import ShadersLayout from '@/components/layouts/ShadersGrid.vue'
  import CollectionsLayout from '@/components/layouts/CollectionsGrid.vue'

  const menu = [
    {key: "collections", label: "Collections", comp: ShadersLayout},
    {key: "shaders", label: "Shaders", comp: CollectionsLayout},
    {key: "saved", label: "Saved", comp: ShadersLayout},
  ]

  const selected = ref('collections')

  const tab = ref(null)

  tab.value = markRaw(ShadersLayout)

  function changeTabAndLayout(tab_name, layout) {
    selected.value = tab_name;
    tab.value = markRaw(layout);
  }

</script>

<script>
export default {
  name: "ProfileView",
  data() {
    return {
      name: 'username'
    }
  }
}
</script>
