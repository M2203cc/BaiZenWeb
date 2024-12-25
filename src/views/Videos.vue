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
    </div>

    <!-- Action Buttons -->
    <div class="flex items-center space-x-4 mb-6">
      <button 
        v-if="hasSelectedVideos"
        @click="openExportModal"
        class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
      >
        Add Creators to List
      </button>
      <button 
        v-if="hasSelectedVideos"
        @click="clearSelection"
        class="px-4 py-2 text-gray-600 hover:text-gray-800"
      >
        Clear Selection
      </button>
    </div>

    <!-- Videos Table -->
    <div class="relative w-full overflow-x-auto rounded-sm border border-secondary-100 bg-white">
        <table class="w-full caption-bottom text-sm">
          <thead class="[&_tr]:border-b">
          <tr class="border-b">
            <th class="py-3 px-2 text-left align-middle">
              <input 
                type="checkbox" 
                class="rounded border-gray-300"
                :checked="isCurrentPageAllSelected"
                @change="selectAll"
              >
            </th>
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
            :key="`${currentPage}-${video.id}`"
            class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
            @click="goToVideoDetail(video)"
            >
              <td class="py-3 px-2 align-middle" @click.stop>
                <input 
                  type="checkbox" 
                  class="rounded border-gray-300"
                  :checked="selectedVideos.some(v => v.id === video.id)"
                  @change="handleVideoSelect(video, $event)"
                >
              </td>
              <td class="py-3 px-2 align-middle">
              <div class="flex items-center gap-3">
                <img 
                  :key="`${currentPage}-${video.id}-thumb`"
                  :src="video.thumbnail_url || 'https://via.placeholder.com/160x120'" 
                  :alt="video.description"
                  class="w-[60px] h-[80px] rounded-md object-cover"
                  @error="handleImageError"
                >
              </div>
              </td>
              <td class="py-3 px-2 align-middle">
                <div class="flex items-center gap-2 relative creator-tooltip">
                  <img 
                    :key="`${currentPage}-${video.id}-creator`"
                    :src="video.creatorAvatar || 'https://via.placeholder.com/40x40'" 
                    :alt="video.creator"
                    class="w-10 h-10 rounded-md object-cover"
                    @error="handleImageError"
                  >
                  <span class="truncate max-w-[150px]">{{ video.creator }}</span>
                  <div class="tooltip-content">{{ video.creator }}</div>
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
                    :key="`${currentPage}-${video.id}-product`"
                    :src="video.productImage || 'https://via.placeholder.com/40x40'" 
                    :alt="video.product"
                    class="w-10 h-10 rounded-md object-cover"
                    @error="handleImageError"
                  >
                  <span class="truncate max-w-[150px]">{{ video.product }}</span>
                  <div class="tooltip-content">{{ video.product }}</div>
                </div>
              </td>
              <td class="py-3 px-2 align-middle">
                <div class="flex items-center gap-2 relative brand-tooltip">
                  <img 
                    :key="`${currentPage}-${video.id}-brand`"
                    :src="video.brandImage || 'https://via.placeholder.com/40x40'" 
                    :alt="video.brand"
                    class="w-10 h-10 rounded-md object-cover"
                    @error="handleImageError"
                  >
                  <span class="truncate">{{ video.brand }}</span>
                  <div class="tooltip-content">{{ video.brand }}</div>
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
      <div v-if="error" class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ error }}
        <button 
          @click="fetchVideos(currentPage)" 
          class="ml-4 text-sm underline hover:text-red-800"
        >
          Retry
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && videos.length === 0" class="p-4 text-center text-gray-500">
        No videos found
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-4 flex justify-between items-center">
      <!-- 左侧显示结果数量 -->
      <div class="text-sm text-gray-700">
        Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, total) }} of {{ total }} results
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

    <!-- Export Modal -->
    <ExportModal
      v-if="showExportModal"
      :show="showExportModal"
      :influencers="selectedCreators"
      @close="closeExportModal"
    />
  </div>
</template>

<script>
import videoAPI from '../services/videoAPI'
import ExportModal from '../components/ExportModal.vue'

// 添加 debounce 实现
function debounce(fn, delay) {
  let timeoutId
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn.apply(this, args), delay)
  }
}

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
      fetchTimer: null,
      selectedVideos: [],
      selectedCreators: []
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
      // 将视频数据换为导出所需格式
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
    },

    hasSelectedVideos() {
      return this.selectedVideos.length > 0
    },
    isCurrentPageAllSelected() {
      return this.videos.length > 0 && 
        this.videos.every(video => this.selectedVideos.some(v => v.id === video.id))
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
    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      try {
        const date = new Date(dateString)
        const now = new Date()
        const diff = now - date
        
        // 如果是无效日期
        if (isNaN(date.getTime())) return 'Unknown'
        
        // 小于1小时
        if (diff < 3600000) {
          const minutes = Math.floor(diff / 60000)
          return `${minutes} minutes ago`
        }
        
        // 小于24小时
        if (diff < 86400000) {
          const hours = Math.floor(diff / 3600000)
          return `${hours} hours ago`
        }
        
        // 小于30天
        if (diff < 2592000000) {
          const days = Math.floor(diff / 86400000)
          return `${days} days ago`
        }
        
        // 大于30天
        return date.toLocaleDateString()
      } catch (e) {
        return 'Unknown'
      }
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
      // 只在第一次加载获取筛选选项
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
    async fetchVideos(page = 1) {
      try {
        this.loading = true
        this.error = null
        
        // 在加载新数据前清空当前数据
        this.videos = []
        
        const params = {
          page: page,
          pageSize: this.pageSize || 10
        }
        
        if (this.searchQuery?.trim()) {
          params.search = this.searchQuery.trim()
        }
        
        // 添加筛选条件
        if (this.filters.brand) params.brand = this.filters.brand
        if (this.filters.product) params.product = this.filters.product
        if (this.filters.viewCount) params.viewCount = this.filters.viewCount

        const response = await videoAPI.getVideos(params)
        console.log('API Response for page:', page, response)
        
        if (response && (response.data || response.items)) {
          const items = response.data || response.items || []
          // 使用 nextTick 确保 DOM 更新
          await this.$nextTick()
          
          this.videos = items.map(video => ({
            id: video.id || video.video_id,
            thumbnail_url: video.thumbnail_url || video.cover_image_url,
            creator: video.creators?.handle || 'Unknown Creator',
            creatorAvatar: video.creator_profile_url,
            views_count: video.views_count || video.stats?.play_count || 0,
            likes_count: video.likes_count || video.stats?.digg_count || 0,
            description: video.description || 'No description',
            posted_date: video.posted_date || video.create_time || video.created_at,
            product: video.seller_products?.title || 'Unknown Product',
            productImage: video.seller_product_photo_url,
            brand: video.seller_products?.sellers?.name || 'Unknown Brand',
            brandImage: video.seller_photo_url
          }))
          
          this.total = response.total || response.meta?.total || items.length
          this.currentPage = page
        } else {
          throw new Error('Invalid response format')
        }
      } catch (error) {
        console.error('Error in fetchVideos:', error)
        this.error = error.message || 'Failed to load videos'
        this.videos = []
        this.total = 0
      } finally {
        this.loading = false
      }
    },
    goToVideoDetail(video) {
      // 阻止事件冒泡，避免触发选择事件
      event?.stopPropagation()
      
      if (video && video.id) {
        this.$router.push({
          name: 'VideoDetail',
          params: { id: video.id }
        })
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        const newPage = this.currentPage - 1
        this.fetchVideos(newPage)
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        const newPage = this.currentPage + 1
        this.fetchVideos(newPage)
      }
    },
    searchVideos() {
      this.fetchVideos(1)
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
        this.fetchVideos(page)
      }
    },
    // 应用筛选条件
    applyFilters() {
      this.fetchVideos(1, true)
    },
    // 搜索处理
    handleSearch: debounce(function() {
      this.fetchVideos(1)
    }, 300),
    // 处理视频选择
    handleVideoSelect(video, event) {
      // 阻止点击事件冒泡，避免触发行点击事件
      event.stopPropagation()
      
      const index = this.selectedVideos.findIndex(v => v.id === video.id)
      if (index === -1) {
        this.selectedVideos.push(video)
        // 如果创建者还没有被选中，添加到选中列表
        if (!this.selectedCreators.includes(video.creator)) {
          this.selectedCreators.push(video.creator)
        }
      } else {
        this.selectedVideos.splice(index, 1)
        // 检查是否需要从创建者列表中移除
        const hasOtherVideos = this.selectedVideos.some(v => v.creator === video.creator)
        if (!hasOtherVideos) {
          const creatorIndex = this.selectedCreators.indexOf(video.creator)
          if (creatorIndex !== -1) {
            this.selectedCreators.splice(creatorIndex, 1)
          }
        }
      }
    },
    // 打开导出模态框
    openExportModal() {
      if (this.selectedCreators.length === 0) {
        alert('Please select at least one video first')
        return
      }
      this.showExportModal = true
    },
    // 关闭导出模态框
    closeExportModal() {
      this.showExportModal = false
    },
    // 清除选择
    clearSelection() {
      this.selectedVideos = []
      this.selectedCreators = []
    },
    // 修改全选方法
    selectAll(event) {
      const isChecked = event.target.checked
      
      // 先获取当前页的所有视频ID
      const currentPageVideoIds = this.videos.map(video => video.id)
      
      if (isChecked) {
        // 选中当前页所有视频
        this.videos.forEach(video => {
          // 如果视频还没有被选中，则添加到选中列表
          if (!this.selectedVideos.some(v => v.id === video.id)) {
            this.selectedVideos.push(video)
            // 如果创建者还没有被选中，添加到选中列表
            if (!this.selectedCreators.includes(video.creator)) {
              this.selectedCreators.push(video.creator)
            }
          }
        })
      } else {
        // 只取消选中当前页的视频
        this.selectedVideos = this.selectedVideos.filter(video => 
          !currentPageVideoIds.includes(video.id)
        )
        
        // 更新创建者列表
        this.selectedCreators = []
        this.selectedVideos.forEach(video => {
          if (!this.selectedCreators.includes(video.creator)) {
            this.selectedCreators.push(video.creator)
          }
        })
      }
    }
  },
  created() {
    this.fetchVideos(1)
  },
  watch: {
    searchQuery(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchVideos(1)
      }
    },
    'filters': {
      deep: true,
      handler() {
        this.fetchVideos(1)
      }
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

/* 修改 tooltip 式 */
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

/* 移除默认的 title 框 */
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