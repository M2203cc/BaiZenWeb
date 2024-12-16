<template>
  <aside 
    class="fixed left-0 top-0 z-40 h-screen w-52 transition-transform sm:translate-x-0" 
    :class="{ '-translate-x-full': !isOpen }"
    aria-label="Sidebar"
  >
    <div class="h-full overflow-y-auto bg-secondary-100 px-3 py-6">
      <!-- Logo -->
      <a href="/" class="flex w-fit items-center px-3 py-2.5 !ring-0">
        <div class="flex items-center space-x-4 mb-4">
          <span class="self-center whitespace-nowrap text-2xl font-bold leading-[28.8px] text-textPrimary">BaiZen</span>
        </div>
      </a>

      <!-- Navigation Menu -->
      <ul class="space-y-1">
        <li>
          <router-link to="/dashboard" class="sidebar-item group" :class="{ 'active': $route.path === '/dashboard' }">
            <span class="flex-1 whitespace-nowrap pl-3">Dashboard</span>
          </router-link>
        </li>

        <!-- OUTREACH Section -->
        <li class="space-y-1">
          <div class="mt-6 text-sm font-bold leading-[16.8px] text-[#6C7381]">OUTREACH</div>
          <router-link to="/campaigns" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">My Bots</span>
          </router-link>
        </li>

        <li>
          <router-link to="/email" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">Emails</span>
          </router-link>
        </li>

        <li>
          <router-link to="/lists" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">Lists</span>
          </router-link>
        </li>

        <li>
          <router-link to="/influencers" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">Find Influencers</span>
          </router-link>
        </li>

        <!-- CRM Section -->
        <li class="space-y-1">
          <div class="mt-6 text-sm font-bold leading-[16.8px] text-[#6C7381]">CRM</div>
          <router-link to="/affiliates" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">My Affiliates</span>
          </router-link>
        </li>

        <li>
          <router-link to="/groups" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">Segments</span>
          </router-link>
        </li>

        <!-- SOCIAL LISTENING & AI Section -->
        <li class="space-y-1">
          <div class="mt-6 text-sm font-bold leading-[16.8px] text-[#6C7381]">SOCIAL LISTENING & AI</div>
          <router-link to="/my-brand" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">My Brand</span>
          </router-link>

          <!-- Discover 下拉菜单 -->
          <div class="sidebar-dropdown">
            <div 
              class="sidebar-item group" 
              @click="toggleDiscover"
            >
              <span class="flex-1 whitespace-nowrap pl-3">Discover</span>
              <span 
                class="arrow transition-transform" 
                :class="{ 'rotate-180': isDiscoverOpen }"
              >▼</span>
            </div>
            
            <div v-if="isDiscoverOpen" class="submenu-container">
              <router-link to="/videos" class="sidebar-item group pl-6">
                <span class="flex-1 whitespace-nowrap pl-3">Videos</span>
              </router-link>
              <router-link to="/brands" class="sidebar-item group pl-6">
                <span class="flex-1 whitespace-nowrap pl-3">Brands</span>
              </router-link>
              <router-link to="/products" class="sidebar-item group pl-6">
                <span class="flex-1 whitespace-nowrap pl-3">Products</span>
              </router-link>
              <router-link to="/categories" class="sidebar-item group pl-6">
                <span class="flex-1 whitespace-nowrap pl-3">Categories</span>
              </router-link>
            </div>
          </div>
        </li>

        <li>
          <router-link to="/avatar-shorts" class="sidebar-item group">
            <span class="flex-1 whitespace-nowrap pl-3">AI Avatar Shorts</span>
          </router-link>
        </li>
      </ul>
    </div>
  </aside>
</template>

<script>
export default {
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isDiscoverOpen: false
    }
  },
  methods: {
    toggleDiscover() {
      this.isDiscoverOpen = !this.isDiscoverOpen
    }
  }
}
</script>

<style scoped>
.sidebar-item {
  @apply flex items-center px-3 py-2 text-base font-normal text-gray-900 rounded-lg;
  transition: all 0.3s ease;
}

.sidebar-item:hover {
  @apply bg-gray-100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateX(5px);
}

.sidebar-item.active {
  @apply bg-blue-50 font-semibold;
  border-right: 3px solid #1890ff;
}

.arrow {
  font-size: 10px;
  margin-left: auto;
  color: #6C7381;
  opacity: 0.8;
}

.submenu-container {
  @apply bg-secondary-100;
  border-left: 2px solid rgba(108, 115, 129, 0.2);
  margin-left: 10px;
  margin-top: 2px;
}

.submenu-container .sidebar-item {
  font-size: 0.9em;
  opacity: 0.9;
}

.submenu-container .sidebar-item:hover {
  @apply bg-gray-100/10;
  transform: translateX(3px);
}

.sidebar-dropdown {
  transition: all 0.3s ease;
}
</style> 