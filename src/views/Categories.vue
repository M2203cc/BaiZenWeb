<template>
  <div class="px-[50px] py-4">
    <h1 class="text-2xl font-bold mb-6">Categories</h1>

    <!-- 错误状态 -->
    <div v-if="error" class="flex flex-col items-center justify-center min-h-[200px]">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button 
        @click="fetchCategories"
        class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-500"
      >
        Retry
      </button>
    </div>

    <!-- 数据展示 -->
    <div v-else class="bg-white rounded-sm border border-secondary-100">
      <table class="w-full caption-bottom text-sm">
        <thead class="[&_tr]:border-b">
          <tr class="border-b bg-[#FAFAFA]">
            <th class="h-12 py-2 px-4 text-left align-middle text-md leading-[19.2px] text-gray-600">Category name</th>
            <th class="h-12 py-2 px-4 text-left align-middle text-md leading-[19.2px] text-gray-600">Number of products</th>
            <th class="h-12 py-2 px-4 text-left align-middle text-md leading-[19.2px] text-gray-600">Selling points</th>
          </tr>
        </thead>
        <tbody class="[&_tr:last-child]:border-0">
          <!-- Loading State -->
          <template v-if="loading">
            <tr v-for="i in 10" :key="i" class="border-b animate-pulse h-[55px]">
              <td class="px-4 align-middle">
                <div class="h-4 w-48 bg-gray-200 rounded"></div>
              </td>
              <td class="px-4 align-middle">
                <div class="h-4 w-16 bg-gray-200 rounded"></div>
              </td>
              <td class="px-4 align-middle">
                <div class="flex gap-2">
                  <div class="h-6 w-20 bg-gray-200 rounded-full"></div>
                  <div class="h-6 w-20 bg-gray-200 rounded-full"></div>
                  <div class="h-6 w-20 bg-gray-200 rounded-full"></div>
                </div>
              </td>
            </tr>
          </template>
          
          <!-- Content -->
          <template v-else>
            <tr 
              v-for="category in categories" 
              :key="category.category_name"
              class="border-b transition-colors duration-200 ease-curve hover:bg-secondary-100 cursor-pointer"
              @click="goToCategoryDetail(category)"
            >
              <td class="py-4 px-4 text-gray-700 relative group">
                <span class="block truncate">{{ category.category_name }}</span>
                <!-- 悬停时显示的完整内容 -->
                <div 
                  class="absolute left-0 bottom-full mb-2 p-2 bg-gray-900 text-white rounded-md shadow-lg z-10 max-w-md text-sm
                         invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-200"
                >
                  {{ category.category_name }}
                </div>
              </td>
              <td class="py-4 px-4 text-gray-600">{{ category.num_products[0]?.count || 0 }}</td>
              <td class="py-4 px-4">
                <div class="flex gap-2 flex-wrap">
                  <span 
                    v-for="(point, index) in getTopSellingPoints(category.selling_points_analysis_json)" 
                    :key="index"
                    class="px-3 py-1 rounded-full text-sm bg-purple-50 text-purple-600 border border-purple-100"
                  >
                    {{ point }}
                  </span>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Categories',
  data() {
    return {
      categories: [],
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      this.loading = true
      this.error = null
      
      try {
        const response = await fetch('http://localhost:8000/categories/')
        const data = await response.json()
        
        console.log('Categories API response:', data)
        
        if (data && data.data) {
          // 检查每个类别对象的结构
          data.data.forEach(category => {
            console.log('Category:', {
              id: category.id,
              name: category.category_name
            });
          });
          
          this.categories = data.data
        }
      } catch (error) {
        console.error('Error fetching categories:', error)
        this.error = 'Failed to load categories. Please try again later.'
      } finally {
        this.loading = false
      }
    },
    getTopSellingPoints(sellingPointsJson) {
      if (!sellingPointsJson || !Array.isArray(sellingPointsJson)) return []
      
      // 只返回前3个selling points
      return sellingPointsJson
        .slice(0, 3)
        .map(point => point.selling_point)
    },
    goToCategoryDetail(category) {
      console.log('Full category object:', category);
      console.log('Category ID:', category.id);
      console.log('Category name:', category.category_name);
      
      // 确保有 ID 才进行路由跳转
      if (!category.id) {
        console.error('No category ID found:', category);
        this.error = 'Invalid category selected';
        return;
      }

      // 修改路由跳转方式
      this.$router.push({
        name: 'CategoryDetail', // 使用命名路由
        params: { 
          id: category.id.toString() // 确保 ID 是字符串
        },
        query: { 
          name: category.category_name
        }
      })
    }
  }
}
</script>

<style scoped>
/* 确保表格单元格内容溢出时显示省略号 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 悬浮提示框的过渡效果 */
.group:hover .group-hover\:visible {
  visibility: visible;
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
</style> 