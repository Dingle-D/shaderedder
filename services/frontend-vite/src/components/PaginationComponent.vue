<template>
  <div class="relative flex justify-center">
    <nav class="flex items-center gap-x-4 min-w-max">
      <!-- Назад -->
      <button
        class="text-gray-700 hover:text-gray-900 p-4 inline-flex items-center md:mr-8 mr-1"
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
      >
        <span>Back</span>
      </button>

      <!-- Страницы -->
      <template v-for="page in pagesToShow" :key="page">
        <button
          v-if="page === '...'"
          disabled
          class="w-2 h-10 text-gray-700 p-2 inline-flex items-center justify-center"
        >
          ...
        </button>
        <button
          v-else
          :class="[
            'w-10 h-10 p-2 inline-flex items-center justify-center rounded-full transition-all duration-150',
            page === currentPage
              ? 'bg-gray-900 text-white'
              : 'bg-transparent text-gray-700 hover:text-gray-900',
          ]"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>

      <!-- Вперед -->
      <button
        class="text-gray-700 hover:text-gray-900 p-4 inline-flex items-center md:ml-8 ml-1"
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
      >
        <span>Next</span>
      </button>
    </nav>
  </div>
</template>

<script>
export default {
  name: "PaginationCommon",
  props: {
    totalPages: {
      type: Number,
      required: true,
    },
    currentPage: {
      type: Number,
      required: true,
    },
    maxVisiblePages: {
      type: Number,
      default: 5,
    },
  },
  emits: ["page-change"],
  computed: {
    pagesToShow() {
      const pages = [];

      if (this.totalPages <= this.maxVisiblePages) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        let start = Math.max(1, this.currentPage - 1);
        let end = Math.min(this.totalPages, start + this.maxVisiblePages - 1);

        if (end - start < this.maxVisiblePages - 1) {
          start = Math.max(1, end - this.maxVisiblePages + 1);
        }

        if (start > 1) {
          pages.push(1);
          if (start > 2) pages.push("...");
        }

        for (let i = start; i <= end; i++) {
          pages.push(i);
        }

        if (end < this.totalPages) {
          if (end < this.totalPages - 1) pages.push("...");
          pages.push(this.totalPages);
        }
      }

      return pages;
    },
  },
  methods: {
    goToPage(page) {
      if (page === "..." || page < 1 || page > this.totalPages) return;
      console.log("Emited");
      this.$emit("page-change", page);
    },
  },
};
</script>
