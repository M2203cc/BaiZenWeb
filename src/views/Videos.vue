<template>
  <div class="px-[50px] py-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-900">Videos</h2>
    </div>

    <!-- Search Bar -->
    <div class="flex gap-4 mb-6 max-w-2xl">
        <input 
        v-model="searchQuery"
          type="text"
        placeholder="Search videos..."
        class="flex min-h-10 w-full rounded-md border border-gray-300 bg-white px-4 py-3 text-[16px]"
        >
        <button 
          @click="searchVideos"
        class="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Search
        </button>
    </div>

    <!-- Filters Section -->
    <div class="flex flex-wrap gap-4 mb-6">
      <!-- Brand Filter -->
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Brand</label>
        <select 
          v-model="filters.brand"
          class="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-500"
        >
          <option value="" class="text-gray-500">Filter by brands</option>
          <option v-for="brand in brandOptions" :key="brand" :value="brand" class="text-gray-900">
            {{ brand }}
          </option>
        </select>
      </div>

      <!-- Product Filter -->
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Product</label>
        <select 
          v-model="filters.product"
          class="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-500"
        >
          <option value="" class="text-gray-500">Filter by products</option>
          <option v-for="product in productOptions" :key="product" :value="product" class="text-gray-900">
            {{ product }}
          </option>
        </select>
      </div>

      <!-- View Count Filter -->
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">View Count</label>
        <select 
          v-model="filters.viewCount"
          class="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-500"
        >
          <option value="" class="text-gray-500">Filter by video views</option>
          <option value="1000000" class="text-gray-900">1M+</option>
          <option value="500000" class="text-gray-900">500K+</option>
          <option value="100000" class="text-gray-900">100K+</option>
          <option value="50000" class="text-gray-900">50K+</option>
        </select>
    </div>

      <!-- Export Button -->
      <div class="flex items-end">
      <button 
          @click="showExportModal = true"
          class="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
      >
        Add creators to list
      </button>
      </div>
    </div>

    <!-- Videos Table -->
    <div class="relative w-full overflow-x-auto rounded-sm border border-secondary-100 bg-white">
        <table class="w-full caption-bottom text-sm">
          <thead class="[&_tr]:border-b">
          <tr class="border-b">
            <th class="py-3 px-2 text-left align-middle">Thumbnail</th>
            <th class="py-3 px-2 text-left align-middle">Creator</th>
            <th class="py-3 px-2 text-left align-middle">Posted Time</th>
            <th class="py-3 px-2 text-left align-middle">Views</th>
            <th class="py-3 px-2 text-left align-middle">Likes</th>
            <th class="py-3 px-2 text-left align-middle">Description</th>
            <th class="py-3 px-2 text-left align-middle">Product</th>
            <th class="py-3 px-2 text-left align-middle">Brand</th>
            </tr>
          </thead>
          <tbody class="[&_tr:last-child]:border-0">
          <tr 
            v-for="video in filteredVideos" 
            :key="video.video_id"
            class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
            @click="goToVideoDetail(video.video_id)"
            >
              <td class="py-3 px-2 align-middle">
              <div class="flex items-center gap-3">
                <img 
                  :src="video.thumbnail_url || 'https://via.placeholder.com/160x120'" 
                  :alt="video.title"
                  class="w-[60px] h-[80px] rounded-md object-cover"
                  @error="handleImageError"
                >
              </div>
              </td>
              <td class="py-3 px-2 align-middle">
              <div class="flex items-center gap-2 relative creator-tooltip">
                <img 
                  :src="video.creator_profile_url || 'https://via.placeholder.com/32x32'" 
                  :alt="video.creators?.handle"
                  class="w-8 h-8 rounded-full object-cover"
                  @error="handleImageError"
                >
                <span class="truncate">{{ video.creators?.handle || 'Unknown Creator' }}</span>
                <div class="tooltip-content">{{ video.creators?.handle || 'Unknown Creator' }}</div>
              </div>
            </td>
            <td class="py-3 px-2 align-middle">{{ getTimeAgo(video.posted_date) }}</td>
            <td class="py-3 px-2 align-middle">{{ formatNumber(video.views_count || 0) }}</td>
            <td class="py-3 px-2 align-middle">{{ formatNumber(video.likes_count || 0) }}</td>
            <td class="py-3 px-2 align-middle max-w-xs">
              <div class="relative description-tooltip">
                <p class="truncate">{{ video.description || 'No description' }}</p>
                <div class="tooltip-content">{{ video.description || 'No description' }}</div>
                </div>
              </td>
            <td class="py-3 px-2 align-middle">
              <div class="flex items-center gap-2 relative product-tooltip">
                <img 
                  :src="video.seller_product_photo_url || 'https://via.placeholder.com/40x40'" 
                  :alt="video.seller_products?.title"
                  class="w-10 h-10 rounded-md object-cover"
                  @error="handleImageError"
                >
                <span class="truncate max-w-[150px]">{{ video.seller_products?.title || 'Unknown Product' }}</span>
                <div class="tooltip-content">{{ video.seller_products?.title || 'Unknown Product' }}</div>
                </div>
              </td>
            <td class="py-3 px-2 align-middle">
              <div class="flex items-center gap-2 relative brand-tooltip">
                <img 
                  :src="video.seller_photo_url || 'https://via.placeholder.com/40x40'" 
                  :alt="video.seller_products?.sellers?.name"
                  class="w-10 h-10 rounded-md object-cover"
                  @error="handleImageError"
                >
                <span class="truncate">{{ video.seller_products?.sellers?.name || 'Unknown Brand' }}</span>
                <div class="tooltip-content">{{ video.seller_products?.sellers?.name || 'Unknown Brand' }}</div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

      <!-- Loading State -->
      <div v-if="loading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="p-4 text-center text-red-600">
        {{ error }}
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && videos.length === 0" class="p-4 text-center text-gray-500">
        No videos found
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="videos.length > 0" class="mt-4 flex justify-between items-center">
      <!-- 显示结果数量 -->
      <div class="text-sm text-gray-700">
        Showing {{ startIndex }} to {{ Math.min(endIndex, total) }} of {{ total }}
      </div>

      <!-- 分页按钮容器 - 居中 -->
      <div class="flex-1 flex justify-center">
        <div class="flex items-center space-x-1">
          <!-- 上一页按钮 -->
          <button 
            @click="prevPage"
            :disabled="currentPage === 1"
            class="px-2 py-1 text-gray-600 hover:text-primary-600"
          >
            <span class="text-sm">‹</span>
          </button>

          <!-- 页码按钮 -->
          <template v-for="n in displayedPages" :key="n">
            <button 
              v-if="n !== '...'"
              @click="goToPage(n)"
              class="px-3 py-1 rounded"
              :class="[
                currentPage === n 
                  ? 'bg-primary-500 text-white' 
                  : 'text-gray-600 hover:text-primary-600'
              ]"
            >
              {{ n }}
            </button>
            <span v-else class="px-2">...</span>
          </template>

          <!-- 下一页按钮 -->
          <button 
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-2 py-1 text-gray-600 hover:text-primary-600"
          >
            <span class="text-sm">›</span>
          </button>
        </div>
      </div>

      <!-- 空的 div 用于保持布局平衡 -->
      <div class="invisible text-sm text-gray-700">
        Showing {{ startIndex }} to {{ Math.min(endIndex, total) }} of {{ total }}
      </div>
    </div>

    <!-- Export Modal -->
    <ExportModal
      v-if="showExportModal"
      :show="showExportModal"
      :influencers="selectedInfluencers"
      @close="showExportModal = false"
    />
  </div>
</template>

<script>
import videoAPI from '../services/videoAPI'
import ExportModal from '../components/ExportModal.vue'

export default {
  name: 'Videos',
  components: {
    ExportModal
  },
  data() {
    return {
      videos: [],
      loading: false,
      error: null,
      currentPage: 1,
      pageSize: 10,
      total: 0,
      searchQuery: '',
      showExportModal: false,
      filters: {
        brand: '',
        product: '',
        viewCount: ''
      },
      brandOptions: [],
      productOptions: [],
      fetchTimer: null
    }
  },
  computed: {
    startIndex() {
      return (this.currentPage - 1) * this.pageSize + 1
    },
    endIndex() {
      return Math.min(this.startIndex + this.pageSize - 1, this.total)
    },
    totalPages() {
      return Math.ceil(this.total / this.pageSize)
    },
    selectedInfluencers() {
      // 将视频数据转换为导出所需格式
      return this.videos.map(video => ({
        handle: video.creators?.handle,
        // 可以添加其他需要段
      }))
    },
    
    filteredData() {
      let filtered = [...this.videos];

      // 应用品牌筛选
      if (this.filters.brand) {
        filtered = filtered.filter(video => 
          video.seller_products?.sellers?.name === this.filters.brand
        );
      }

      // 应用产品筛选
      if (this.filters.product) {
        filtered = filtered.filter(video => 
          video.seller_products?.title === this.filters.product
        );
      }

      // 应用观看次数筛选
      if (this.filters.viewCount) {
        const minViews = parseInt(this.filters.viewCount);
        filtered = filtered.filter(video => 
          (video.views_count || 0) >= minViews
        );
      }

      return filtered;
    },

    filteredVideos() {
      // 如果没有筛选条件，使用 API 返回的 total
      if (!this.filters.brand && !this.filters.product && !this.filters.viewCount) {
        return this.videos;
      }

      // 选条件时，更新 total 为筛选后的数量
      this.total = this.filteredData.length;

      // 返回当前页的数据
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredData.slice(start, end);
    },

    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      let pages = [];

      if (total <= 5) {
        // 如果总页数小于等于5，显示所有页码
      for (let i = 1; i <= total; i++) {
          pages.push(i);
        }
      } else {
        // 总页数大于5的情况
        if (current <= 3) {
          // 在前几页时显示: 1 2 3 4 ... n
          pages = [1, 2, 3, 4, '...', total];
        } else if (current >= total - 2) {
          // 在后几页时显示: 1 ... n-3 n-2 n-1 n
          pages = [1, '...', total - 3, total - 2, total - 1, total];
        } else {
          // 在中间页时显示: 1 ... current-1 current current+1 current+2 ... n
          pages = [
            1,
            '...',
            current - 1,
            current,
            current + 1,
            current + 2,
            '...',
            total
          ];
        }
      }

      return pages;
    }
  },
  methods: {
    formatNumber(num) {
      if (!num) return '0'
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    },
    formatDate(timestamp) {
      if (!timestamp) return 'Unknown date'
      const date = new Date(timestamp * 1000)
      return date.toLocaleDateString()
    },
    handleImageError(e) {
      // 片加载失败时使用默认图
      if (e.target.classList.contains('rounded-full')) {
        e.target.src = 'https://via.placeholder.com/32x32'
      } else {
        e.target.src = 'https://via.placeholder.com/160x120'
      }
    },
    async fetchFiltersOptions() {
      // 只在第一次加载时获取筛选选项
      if (this.brandOptions.length === 0 && this.productOptions.length === 0) {
        const brands = new Set()
        const products = new Set()
        
        this.videos.forEach(video => {
          if (video.seller_products?.sellers?.name) {
            brands.add(video.seller_products.sellers.name)
          }
          if (video.seller_products?.title) {
            products.add(video.seller_products.title)
          }
        })
        
        this.brandOptions = Array.from(brands)
        this.productOptions = Array.from(products)
      }
    },
    async fetchVideos(page = 1, applyFilters = false) {
      try {
        this.loading = true
        const params = {
          page,
          page_size: 10,
          search: this.searchQuery || undefined
        }
        
        // 添加筛选条件到请求参数
        if (applyFilters) {
          if (this.filters.views.min) params.views_min = this.filters.views.min
          if (this.filters.views.max) params.views_max = this.filters.views.max
          if (this.filters.likes.min) params.likes_min = this.filters.likes.min
          if (this.filters.likes.max) params.likes_max = this.filters.likes.max
          if (this.filters.dateRange.start) params.posted_after = this.filters.dateRange.start
          if (this.filters.dateRange.end) params.posted_before = this.filters.dateRange.end
          if (this.filters.brands.length) params.brands = this.filters.brands
          if (this.filters.products.length) params.products = this.filters.products
        }

        const response = await videoAPI.getVideos(params)
        this.videos = response.data.items
        this.totalPages = response.data.total_pages
        this.currentPage = page
      } catch (error) {
        console.error('Error fetching videos:', error)
      } finally {
        this.loading = false
      }
    },
    goToVideoDetail(videoId) {
      this.$router.push(`/videos/${videoId}`)
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.fetchVideos()
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.fetchVideos()
      }
    },
    searchVideos() {
      this.currentPage = 1
      this.fetchVideos()
    },
    getTimeAgo(date) {
      if (!date) return 'Unknown date'
      const now = new Date()
      const postedDate = new Date(date)
      const diffTime = Math.abs(now - postedDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      // 计算月份差异
      const months = Math.floor(diffDays / 30)
      
      if (months > 0) {
        if (months === 1) {
          return 'a month ago'
        }
        return `${months} months ago`
      } else {
        if (diffDays === 1) {
          return '1 day ago'
        }
        return `${diffDays} days ago`
      }
    },
    goToPage(page) {
      if (page !== this.currentPage) {
        this.currentPage = page
        this.fetchVideos()
      }
    },
    // 应用筛选条件
    applyFilters() {
      this.currentPage = 1 // 重置到第一页
      this.fetchVideos(1, true)
    },
    // 搜索处理
    handleSearch: debounce(function() {
      this.currentPage = 1
      this.fetchVideos(1)
    }, 300)
  },
  created() {
    this.fetchVideos()
  },
  watch: {
    searchQuery(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.currentPage = 1
        this.fetchVideos()
      }
    },
    'filters': {
      deep: true,
      handler() {
        this.currentPage = 1
        this.fetchVideos()
      }
      },
    currentPage(newPage) {
      this.fetchVideos()
    }
  }
}
</script>

<style scoped>
.max-w-xs {
  max-width: 20rem;
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.filter-select {
  @apply flex w-full rounded-md border border-gray-300 bg-white 
  text-sm transition-all hover:border-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500;
}

/* 分页器样式 */
.text-primary-600 {
  color: #6366F1;
}

.bg-primary-500 {
  background-color: #6366F1;
}

.hover\:text-primary-600:hover {
  color: #6366F1;
}

/* 禁用状态的按钮样式 */
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 分页按钮的过渡效果 */
button {
  transition: all 0.2s ease-in-out;
}

/* 修改 tooltip 样式 */
[title] {
  position: relative;
}

[title]:hover::before {
  content: attr(title);
  position: absolute;
  top: -8px;
  left: 0;
  transform: translateY(-100%);
  padding: 4px 8px;
  background-color: #000;
  color: white;
  border-radius: 4px;
  font-size: 12px;
  white-space: normal;
  max-width: 300px;
  word-wrap: break-word;
  z-index: 10;
}

[title]:hover::after {
  display: none;
}

[title] {
  cursor: pointer;
}

/* 移除默认的 title 示框 */
[title] {
  pointer-events: none;
}

/* 自定义提示框样式 */
.creator-tooltip,
.description-tooltip,
.product-tooltip,
.brand-tooltip {
  position: relative;
}

.tooltip-content {
  display: none;
  position: absolute;
  top: -8px;
  left: 0;
  transform: translateY(-100%);
  background-color: #000;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: normal;
  max-width: 300px;
  word-wrap: break-word;
  z-index: 10;
}

.creator-tooltip:hover .tooltip-content,
.description-tooltip:hover .tooltip-content,
.product-tooltip:hover .tooltip-content,
.brand-tooltip:hover .tooltip-content {
  display: block;
}

/* 添加表格行高样式 */
th, td {
  height: 55px !important;
}

/* 或者使用 min-height 来确保最小高度 */
.min-h-16 {
  min-height: 55px;
}
</style> 