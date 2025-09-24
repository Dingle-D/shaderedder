<template>
  <div class="bg-white">
    <div class="mx-auto max-w-2xl px-4 py-4 sm:px-6 sm:py-4 lg:max-w-6xl lg:px-8">
      <h2 class="sr-only">Explore</h2>

      <div class="flex items-center w-full h-full space-x-4">
        <input 
          id="search"
          class="block max-w-sm min-w-sm rounded-md border border-gray-300 bg-white py-2 px-3 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none sm:text-sm" 
          placeholder="Search" 
          type="search" 
          name="search" 
          v-model="searchInputContent" 
          @keydown.enter="onSearchFilter(searchInputContent)"
        >
        <button class="block px-3 py-2 rounded-md bg-gray-900 text-white" @click="onSearchFilter(searchInputContent)">
          <svg class="h-5 w-5" 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 20 20" 
            fill="currentColor" 
            aria-hidden="true">
            <SearchIcon/>
          </svg>
        </button>

      </div>
      <ShadersGrid @selected="onShaderClick" :author="authorPattern" :search="searchPattern"/>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ApiService from "@/common/api.service";
import PaginationCommon from "@/components/PaginationComponent.vue";
import ShadersGrid from "@/components/layouts/ShadersGrid.vue";
import SearchIcon from "@/components/icons/search.vue";

const shaders = ref([])
const page = ref(1)

const searchInputContent = ref('')
const searchPattern = ref('')
const authorPattern = ref('')

const router = useRouter();

onMounted(async () => {
  try {
  } catch (error) {
    console.error('Could not load /explore data:', error)
  }
})

function onSearchFilter(search) {
  console.log("search pushed. value: ", search);
  searchPattern.value = searchInputContent.value;
}

function onShaderClick(id) {
  router.push({ name: "editor", params: {id} })
}

</script>
