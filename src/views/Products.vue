<template>
  <div class="px-[50px] py-4">
    <!-- 标题部分 -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-gray-900">Products</h2>
    </div>

    <!-- 产品列表表格 -->
    <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
      <div v-if="loading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
      <table class="w-full caption-bottom text-sm">
        <thead class="[&_tr]:border-b">
          <tr class="border-b transition-colors hover:bg-white">
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 min-w-64">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Product</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Price</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Sold Count</div>
            </th>
          </tr>
        </thead>
        <tbody v-if="!loading && products.length > 0" class="[&_tr:last-child]:border-0">
          <tr 
            v-for="product in getCurrentPageProducts" 
            :key="product.id"
            class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
            @click="viewProductDetail(product)"
          >
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000 max-w-64">
              <div class="flex items-center gap-2">
                <img 
                  :src="product.image" 
                  :alt="product.name"
                  class="rounded-md object-cover w-12 h-12 flex-shrink-0"
                >
                <button class="!ring-0 text-left truncate w-auto">
                  {{ product.name }}
                </button>
              </div>
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              ${{ product.price }}
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              {{ product.soldCount }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 无数据状态 -->
      <div v-if="!loading && products.length === 0" class="py-20 text-center text-gray-500">
        No products found
      </div>
    </div>

    <!-- 分页部分 -->
    <div class="mt-4 flex justify-between items-center">
      <!-- 左侧显示结果数量 -->
      <div class="text-sm text-gray-700">
        Showing {{ startIndex + 1 }} to {{ Math.min(endIndex, totalProducts) }} of {{ totalProducts }} results
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
export default {
  name: 'Products',
  data() {
    return {
      products: [],
      currentPage: 1,
      pageSize: 10,
      loading: false,
      totalItems: 0
    }
  },
  computed: {
    totalProducts() {
      return this.totalItems
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.pageSize)
    },
    getCurrentPageProducts() {
      return this.products
    },
    startIndex() {
      return (this.currentPage - 1) * this.pageSize
    },
    endIndex() {
      return Math.min(this.currentPage * this.pageSize, this.totalItems)
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
    async fetchProducts() {
      try {
        this.loading = true
        const response = await fetch(`http://192.168.0.170:8000/products/?page=${this.currentPage}&page_size=${this.pageSize}`)
        
        const data = await response.json()
        
        if (response.status === 200 && data.data) {
          this.products = data.data.map(item => ({
            id: item.product_id,
            name: item.title,
            price: item.real_price,
            soldCount: item.sold_count,
            image: `https://btsplwsgjvpilxywmaba.supabase.co/storage/v1/object/public/seller_products_photos/${item.product_id}.jpg`
          }))
          
          this.totalItems = data.total
        }
      } catch (error) {
        console.error('获取产品数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    goToPage(page) {
      if (page !== this.currentPage) {
        this.currentPage = page
        this.fetchProducts()
      }
    },
    viewProductDetail(product) {
      this.$router.push(`/products/${product.id}`)
    }
  },
  created() {
    this.fetchProducts()
  }
}
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