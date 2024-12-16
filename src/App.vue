<template>
  <div class="min-h-screen bg-gray-50">
    <Sidebar :is-open="isSidebarOpen" />
    <div class="sm:ml-52">
      <TopNav @toggle-sidebar="toggleSidebar" />
      <main class="min-h-[calc(100dvh-4rem)] md:min-h-[calc(100dvh-5rem)]">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'
import TopNav from './components/TopNav.vue'

export default {
  name: 'App',
  components: {
    Sidebar,
    TopNav
  },
  data() {
    return {
      isSidebarOpen: false
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen
    }
  }
}
</script> 