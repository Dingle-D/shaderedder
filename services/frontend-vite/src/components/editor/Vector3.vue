<template>
  <div class="flex space-x-4">
    <div v-for="coord in coords" :key="coord" class="flex space-x-2 items-center">
      <p class="">{{ coord }}:</p>
      <input
        type="text"
        @input="sendData"
        v-model.number="local[coord]"
        class="min-w-8 inline-flex justify-center rounded-full border border-gray-300 bg-white px-4 py-2"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "VectorBlock",
  data() {
    return {
      coords: ['x', 'y', 'z'],
      local: {
        x: 0,
        y: 0,
        z: 0
      }
    }
  },
  methods: {
    sendData() {
      for (const key in this.local) {
        if (this.local[key] === "")
          this.local[key] = 0;
      }
      this.$emit('onUpdate', { ...this.local })
    }
  }
}
</script>
