<template>
  <div id="app">
    <TopNavigation />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import TopNavigation from './components/TopNavigation.vue'

export default {
  name: 'App',
  components: {
    TopNavigation
  }
}
</script>

<style lang="scss">
#app {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  padding-top: 20px;
  padding-bottom: 40px;
}
</style>
