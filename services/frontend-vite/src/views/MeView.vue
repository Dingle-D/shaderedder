<template>
  <div>
    
  </div>
</template>

<script setup lang="ts">
  import { useRouter } from "vue-router"
  import { useStore } from "vuex"
  import { onMounted } from "vue"

  const store = useStore()
  const router = useRouter()

  onMounted(() => {
    const id = store.state.auth.user?.id
    if (!id) {
      router.push({name: "login"})
    }
    else {
      router.push({path: `/user/${id}`})
    }
  })
</script>
