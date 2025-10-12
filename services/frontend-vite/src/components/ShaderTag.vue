<script>
export default {
  name: "ShaderTag",
  props: {
    label: {
      type: String,
      default: 'something'
    }
  },
  computed: {
    tagClass() {
      const colorMap = {
        vertex: 'bg-green-100 text-green-800',
        fragment: 'bg-pink-100 text-pink-800',
        scene: 'bg-blue-100 text-blue-800',
        animated: 'bg-yellow-100 text-yellow-800',
        not_animated: 'bg-indigo-100 text-indigo-800',
        default: 'bg-gray-100 text-gray-800'
      }
      return colorMap[this.label] || colorMap.default
    }
  }
}
</script>

<template>
  <span :class="`px-3 py-1 rounded-full text-xs ${tagClass}`">
    #{{ label }}
  </span>
</template>
