<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 标题和搜索框部分 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-4">Brands</h1>
      <div class="flex gap-2 max-w-2xl">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search brands..."
          class="flex-grow px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
          @input="handleSearch"
        />
        <button
          @click="handleSearch"
          class="px-6 py-2 bg-[#6366F1] text-white rounded-md hover:bg-[#5558E3]"
        >
          Search
        </button>
      </div>
    </div>

    <!-- 品牌列表表格 -->
    <div class="bg-white rounded-lg shadow overflow-hidden relative">
      <div v-if="loading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Brand
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Number of products
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Total sales
            </th>
          </tr>
        </thead>
        <tbody v-show="!loading && brands.length > 0" class="bg-white divide-y divide-gray-200">
          <tr 
            v-for="brand in brands" 
            :key="brand.id"
            class="hover:bg-gray-50 cursor-pointer"
            @click="viewBrandDetails(brand.id)"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10">
                  <img
                    :src="brand.brand_url"
                    :alt="brand.name"
                    class="h-10 w-10 rounded-lg object-cover"
                    @error="handleImageError"
                  />
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">{{ brand.name }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ brand.num_products }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              ${{ formatNumber(brand.total_sales) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="mt-4 flex justify-between items-center">
      <!-- 左侧显示结果数量 -->
      <div class="text-sm text-gray-700">
        Showing {{ startIndex + 1 }} to {{ Math.min(endIndex, totalBrands) }} of {{ totalBrands }} results
      </div>

      <!-- 中间分页按钮 -->
      <div class="flex-1 flex justify-center">
        <div class="flex items-center space-x-1">
          <button
            @click="goToPage(1)"
            :disabled="currentPage === 1"
            :class="[
              'px-3 py-1 text-sm',
              currentPage === 1
                ? 'bg-[#6366F1] text-white rounded-md'
                : 'text-gray-500 hover:text-[#6366F1] disabled:text-gray-300'
            ]"
          >
            1
          </button>

          <button
            v-if="showLeftEllipsis"
            class="px-3 py-1 text-sm text-gray-500"
          >
            ...
          </button>

          <button
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="[
              'px-3 py-1 text-sm',
              currentPage === page
                ? 'bg-[#6366F1] text-white rounded-md'
                : 'text-gray-500 hover:text-[#6366F1]'
            ]"
          >
            {{ page }}
          </button>

          <button
            v-if="showRightEllipsis"
            class="px-3 py-1 text-sm text-gray-500"
          >
            ...
          </button>

          <button
            v-if="totalPages > 1"
            @click="goToPage(totalPages)"
            :class="[
              'px-3 py-1 text-sm',
              currentPage === totalPages
                ? 'bg-[#6366F1] text-white rounded-md'
                : 'text-gray-500 hover:text-[#6366F1]'
            ]"
          >
            {{ totalPages }}
          </button>
        </div>
      </div>

      <!-- 右侧空白区域，用于保持对称 -->
      <div class="w-[250px]"></div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import brandAPI from '../services/brandAPI'

export default defineComponent({
  name: 'Brands',
  data() {
    return {
      brands: [],
      currentPage: 1,
      pageSize: 10,
      totalBrands: 0,
      searchQuery: '',
      loading: false,
      error: null
    }
  },
  computed: {
    startIndex() {
      return (this.currentPage - 1) * this.pageSize
    },
    endIndex() {
      return Math.min(this.startIndex + this.pageSize, this.totalBrands)
    },
    totalPages() {
      return Math.ceil(this.totalBrands / this.pageSize)
    },
    visiblePages() {
      let start = Math.max(2, this.currentPage - 2)
      let end = Math.min(this.totalPages - 1, start + 4)
      
      // 调整起始位置，确保始终显示5个页码
      if (end - start + 1 < 5) {
        start = Math.max(2, end - 4)
      }
      
      const pages = []
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    },
    showLeftEllipsis() {
      return this.visiblePages.length > 0 && this.visiblePages[0] > 2
    },
    showRightEllipsis() {
      return this.visiblePages.length > 0 && 
             this.visiblePages[this.visiblePages.length - 1] < this.totalPages - 1
    }
  },
  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat().format(num)
    },
    async fetchBrands() {
      try {
        this.loading = true
        const response = await brandAPI.getBrands({
          page: this.currentPage,
          pageSize: this.pageSize,
          search: this.searchQuery,
          withImages: true
        })

        if (response && response.data) {
          this.brands = response.data.map(brand => ({
            id: brand.seller_id,
            name: brand.name,
            brand_url: brand.brand_url,
            num_products: brand.num_products,
            total_sales: brand.total_sales,
            category_id: brand.category_id,
            created_at: brand.created_at,
            last_updated_at: brand.last_updated_at
          }))
          this.totalBrands = response.total
        }
      } catch (error) {
        console.error('Error fetching brands:', error)
        this.error = 'Failed to load brands'
      } finally {
        this.loading = false
      }
    },
    viewBrandDetails(brandId) {
      this.$router.push(`/brands/${brandId}`)
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.fetchBrands()
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.fetchBrands()
      }
    },
    goToPage(page) {
      if (page !== this.currentPage) {
        this.currentPage = page
        this.fetchBrands()
      }
    },
    handleSearch() {
      this.currentPage = 1
      this.fetchBrands()
    },
    handleImageError(e) {
      e.target.src = '/default-brand.png'
    }
  },
  created() {
    this.fetchBrands()
  }
})
</script>

<style>
.bg-primary {
  background-color: #6366F1;
}

.text-primary {
  color: #6366F1;
}

.ring-primary {
  --tw-ring-color: #6366F1;
}

.hover\:bg-primary:hover {
  background-color: #6366F1;
}
</style> 