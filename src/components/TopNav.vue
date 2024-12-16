<template>
  <nav class="px-[50px] mx-auto">
    <div class="relative flex flex-row justify-between py-4 align-center">
      <div class="flex items-center">
        <!-- Mobile menu button -->
        <button 
          class="sm:hidden inline-flex items-center p-2 text-sm text-gray-500 rounded-lg hover:bg-gray-100"
          @click="toggleSidebar"
        >
          Menu
        </button>
      </div>
      
      <div class="flex justify-end flex-1 space-x-2">
        <a 
          href="https://discord.gg/pxBD5Harg5" 
          target="_blank"
          class="nav-button"
        >
          Support
        </a>
        <router-link to="/plans" class="nav-button">
          Free Plan
        </router-link>
        <router-link to="/account" class="nav-button">
          My Account
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    toggleSidebar() {
      this.$emit('toggle-sidebar')
    }
  }
}
</script>

<style scoped>
.nav-button {
  @apply py-2.5 px-3 text-sm leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] 
  transition-all duration-200 bg-transparent hover:bg-secondary-100 text-primary-600 !ring-0 !ring-offset-0;
}
</style> 