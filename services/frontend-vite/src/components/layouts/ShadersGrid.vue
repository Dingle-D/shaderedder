<template>
  <div class="w-full bg-white justify-center">
    <div class="mx-auto max-w-2xl px-4 py-4 sm:px-6 sm:py-4 lg:max-w-6xl lg:px-8">
      <h2 class="sr-only">Shaders grid</h2>

      <div class="grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
        <button
          v-for="shader in shaders"
          :key="shader.id"
          @click="onShaderClick(shader.id)"
          class="group block rounded-lg border border-gray-300 hover:border-gray-900 hover:opacity-75 duration-200"
        >
          <!--
          <img
            :src="shader.preview" 
            :alt="shader.title"
            class="aspect-square w-full rounded-lg bg-gray-200 object-cover group-hover:opacity-75 xl:aspect-7/8"
          />-->
          <div class="aspect-square w-full rounded-lg bg-gray-200 object-cover group-hover:opacity-75 xl:aspect-7/8">
          <ShaderViewport :shaderId="shader.id" />
          </div>
          <div class="my-2 mx-4">
            <h3 class="text-lg text-gray-900">{{shader.title}}</h3>
            <p class="text-sm text-gray-500">{{shader.author}}</p>
            <div class="flex flex-wrap gap-2">
              <!--<ShaderTag 
                 v-for="tag in shader.tags.filter(t => t)"
                 :key="tag"
                 :label="tag"
              />-->
            </div>
          </div>
        </button>
      </div>
    </div>
    <PaginationCommon
        :totalPages="totalPages"
        :currentPage="page"
        :maxVisiblePages="3"
        lg:maxVisiblePages="5"
        @page-change="onPageChanged"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import ApiService from "@/common/api.service";
import PaginationCommon from "@/components/PaginationComponent.vue";
import ShaderTag from "@/components/ShaderTag.vue"
import ShaderViewport from "@/components/layouts/ShaderPreview.vue"

const shaders = ref([])
const page = ref(1)
const totalPages = ref(10)
const limit = 10;

const props = defineProps({
  search: {
    type: String,
    required: false,
    default: ""
  },
  author: {
    type: String,
    required: false,
    default: ""
  }
})

const emit = defineEmits(['selected']);
let gAuthorSearch = props.author;
let gSearch = props.search;

onMounted(async () => {
  updateContent(1, null);
})

watch(() => props.search, (searchPattern) => {
  let pattern = (searchPattern === "") ? null : searchPattern;
  console.log("Updated search pattern. updating content.")
  page.value = 1;
  gSearch = pattern
  updateContent(page.value, search=gSearch, author=gAuthorSearch);
});

watch(() => props.author, (searchPattern) => {
  let pattern = (searchPattern === "") ? null : searchPattern;
  console.log("Updated author filter pattern. updating content.")
  page.value = 1;
  gAuthorSearch = pattern
  updateContent(page.value, search=gSearch, author=gAuthorSearch);
});


function onPageChanged(newPage) {
  console.log("Page changed to", newPage);
  page.value = newPage;
  console.log("value", page.value);
  updateContent(newPage, searchPattern.value);
}

function onShaderClick(id) {
  emit('selected', id)
}

async function updateContent(newPageNumber, search = null, author=null) {
  if (newPageNumber < 1) return;
  try {
    let params = {limit, offset: (newPageNumber - 1) * limit}

    if (search)
      params['search'] = search;

    if (author)
      params['author'] = author;

    console.log(import.meta.env)
    console.log(ApiService.getApiUrl())
    const response = await ApiService.query(`explore`, params);
    console.log(response)
    const meta = response.data.meta;
    shaders.value = response.data.data;
    totalPages.value = Math.floor(meta.total / meta.limit) + 1;
    page.value = Math.floor(meta.offset / meta.limit) + 1;
    console.log("in update page value:", page.value, ", meta:", meta);
  } catch (error) {
    console.error('Could not load /explore data:', error)
  }
}

</script>

<script>
export default {
  name: "ShadersLayout"
}
</script>
