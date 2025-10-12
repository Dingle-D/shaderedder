<template>
  <div class="w-full bg-white justify-center">
    <div class="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-6xl lg:px-8">
      <h2 class="sr-only">Collections grid</h2>

      <div class="grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
        <a
          v-for="collection in collections"
          :key="collection.id"
          :href="`/home`"
          class="group block rounded-lg border border-gray-300 hover:border-gray-900 hover:opacity-75 duration-200"
        >
          <div class="my-4 mx-4 space-y-4">
            <h3 class="text-lg text-gray-900">{{collection.title}}</h3>
            <!-- Тут должен быть контейнер с картинками -->
            <div class="overflow-x-auto scrollbar-hidden">
              <div class="flex gap-4 w-max">
                <img
                  v-for="img in collection.preview"
                  :key="img"
                  :src="img"
                  class="h-40 w-60 object-cover rounded-md shrink-0"
                  alt="preview"
                />
              </div>
            </div>
          </div>
        </a>
      </div>
    </div>
    <PaginationCommon
        :totalPages="10"
        :currentPage="page"
        :maxVisiblePages="3"
        lg:maxVisiblePages="5"
        @page-change="val => page = val"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ApiService from "@/common/api.service";
import PaginationCommon from "@/components/PaginationComponent.vue";

const collections = ref([])
const page = ref(1)

onMounted(async () => {
  try {
    const response = await ApiService.get(`collections`);
    console.log("RESPONSE: ", response);
    collections.value = response.data;
  } catch (error) {
    console.error('Could not load /collections data:', error)
  }
})
</script>

<script>
export default {
  name: "CollectionsLayout"
}
</script>

<style>
.scrollbar-hidden {
  scrollbar-width: none;       /* Firefox */
  -ms-overflow-style: none;    /* IE 10+ */
}
.scrollbar-hidden::-webkit-scrollbar {
  display: none;               /* Chrome, Safari */
}
</style>
