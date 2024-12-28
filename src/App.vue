<template>
  <div class="min-h-screen bg-gray-50">
    <Sidebar :is-open="isSidebarOpen" />
    <div class="sm:ml-52">
      <TopNav @toggle-sidebar="toggleSidebar" />
      <main class="min-h-[calc(100dvh-4rem)] md:min-h-[calc(100dvh-5rem)]">
        <keep-alive include="Influencers">
          <router-view v-slot="{ Component }">
            <component :is="Component" />
          </router-view>
        </keep-alive>
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

<style>
/* 全局样式 */
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-50;
}

.bg-primary-600 {
  background-color: #6366F1;
}

.hover\:bg-primary-700:hover {
  background-color: #4F46E5;
}

.text-primary-600 {
  color: #6366F1;
}

.border-primary-600 {
  border-color: #6366F1;
}
</style> 