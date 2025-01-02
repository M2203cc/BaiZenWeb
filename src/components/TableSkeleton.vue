<template>
  <div class="animate-pulse">
    <!-- 表头骨架 -->
    <div class="border-b">
      <div class="flex">
        <div class="p-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded"></div>
        </div>
        <div class="p-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded"></div>
        </div>
        <div class="p-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded"></div>
        </div>
        <div class="p-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded"></div>
        </div>
        <div class="p-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded"></div>
        </div>
        <div class="p-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>

    <!-- 表格内容骨架 -->
    <div v-for="i in 10" :key="i" class="border-b">
      <div class="flex py-4">
        <!-- Handle 列 -->
        <div class="px-2 w-1/6">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-gray-200 rounded-full mr-3"></div>
            <div class="flex-1">
              <div class="h-4 bg-gray-200 rounded w-20 mb-1"></div>
              <div class="h-3 bg-gray-200 rounded w-24"></div>
            </div>
          </div>
        </div>
        <!-- Bio 列 -->
        <div class="px-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
        <!-- Product Category 列 -->
        <div class="px-3 w-1/6">
          <div class="flex gap-1">
            <div class="h-6 bg-gray-200 rounded w-16"></div>
            <div class="h-6 bg-gray-200 rounded w-16"></div>
          </div>
        </div>
        <!-- Follower Count 列 -->
        <div class="px-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded w-12"></div>
        </div>
        <!-- GMV 列 -->
        <div class="px-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded w-16"></div>
        </div>
        <!-- Profile 列 -->
        <div class="px-3 w-1/6">
          <div class="h-4 bg-gray-200 rounded w-24"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TableSkeleton'
}
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style> 