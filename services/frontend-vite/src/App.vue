<template>
  <div id="app">
    <AppHeader v-if="$route.meta.header !== false" />
    <router-view />
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

h1 {
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.toggle-link {
  margin-top: 15px;
  display: block;
  color: #42b983;
  cursor: pointer;
}

.toggle-link:hover {
  text-decoration: underline;
}

</style>

