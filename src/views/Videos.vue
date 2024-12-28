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
      <!-- Date Range Filter -->
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Date Range</label>
        <div class="relative">
          <div 
            class="flex items-center w-full rounded-md border border-gray-300 bg-white px-3 py-2 cursor-pointer"
            @click="showDatePicker = true"
          >
            <span v-if="!dateRange.start || !dateRange.end" class="text-gray-500">
              Select date range
            </span>
            <span v-else class="text-gray-900">
              {{ formatDateRange }}
            </span>
            <button
              v-if="dateRange.start && dateRange.end"
              @click.stop="clearDateRange"
              class="ml-auto text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>

          <!-- 日期选择器弹窗 -->
          <div
            v-if="showDatePicker"
            class="absolute z-50 mt-1 p-4 bg-white border border-gray-300 rounded-md shadow-lg"
            style="min-width: 600px"
          >
            <div class="flex flex-col">
              <div class="flex justify-between items-center mb-4">
                <span class="text-sm font-medium">Select date range</span>
                <button
                  @click="clearDateRange"
                  class="text-sm text-gray-500 hover:text-gray-700"
                >
                  Clear
                </button>
              </div>
              
              <!-- 快捷选项 -->
              <div class="flex gap-2 mb-4">
                <button
                  v-for="(option, index) in datePresets"
                  :key="index"
                  @click="selectDatePreset(option)"
                  class="px-3 py-1 text-sm rounded-md hover:bg-gray-100"
                >
                  {{ option.label }}
                </button>
              </div>

              <!-- 日历组件 -->
              <v-date-picker
                v-model="dateRange"
                is-range
                :min-date="new Date(2020, 0, 1)"
                :max-date="new Date()"
                :columns="2"
                class="rounded-md"
              />

              <!-- 操作按钮 -->
              <div class="flex justify-end gap-2 mt-4">
                <button
                  @click="showDatePicker = false"
                  class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  @click="applyDateRange"
                  class="px-4 py-2 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700"
                >
                  Apply
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- View Count Filter -->
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">View Count</label>
        <div class="relative">
          <!-- 输入框区域 -->
          <div 
            class="flex items-center w-full rounded-md border border-gray-300 bg-white px-3 py-2 cursor-pointer"
            @click="showViewCountDropdown = true"
          >
            <div class="flex flex-1 flex-wrap gap-2 min-h-[28px]">
              <!-- 已选择的标签 -->
              <div
                v-for="(count, index) in selectedViewCounts"
                :key="index"
                class="inline-flex items-center gap-1 bg-gray-100 px-2 py-1 rounded-md text-sm"
              >
                <span>{{ formatViewCount(count) }}</span>
                <button
                  @click.stop="removeViewCount(count)"
                  class="text-gray-500 hover:text-gray-700"
                >
                  ×
                </button>
              </div>
              
              <!-- 占位文本 -->
              <span v-if="!selectedViewCounts.length" class="text-gray-500">
                Filter by video views
              </span>
            </div>

            <!-- 右侧按钮区域 -->
            <div class="flex items-center gap-1">
              <button
                v-if="selectedViewCounts.length"
                @click.stop="clearViewCounts"
                class="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
              <svg 
                class="w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth="2" 
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </div>

          <!-- 下拉选项 -->
          <div
            v-if="showViewCountDropdown"
            class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg"
          >
            <div class="py-1">
              <div
                v-for="option in availableViewCounts"
                :key="option.value"
                @click.stop="selectViewCount(option.value)"
                class="px-4 py-2 text-sm hover:bg-gray-100 cursor-pointer"
              >
                {{ option.label }}
              </div>
            </div>
          </div>
        </div>
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

    <!-- 添加点击其他区域关闭下拉框的处理 -->
    <div
      v-if="showViewCountDropdown"
      class="fixed inset-0 z-0"
      @click="showViewCountDropdown = false"
    ></div>
  </div>
</template>

<script>
import videoAPI from '../services/videoAPI'
import ExportModal from '../components/ExportModal.vue'
import { DatePicker } from 'v-calendar'

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
    ExportModal,
    'v-date-picker': DatePicker
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
      selectedCreators: [],
      showViewCountDropdown: false,
      selectedViewCounts: [],
      viewCountOptions: [
        { value: '0-100', label: '0-100' },
        { value: '100-500', label: '100-500' },
        { value: '500-2000', label: '500-2K' },
        { value: '2000+', label: '2K+' }
      ],
      showDatePicker: false,
      dateRange: {
        start: null,
        end: null
      },
      datePresets: [
        { label: 'Today', getValue: () => {
          const today = new Date();
          return { start: today, end: today };
        }},
        { label: 'Yesterday', getValue: () => {
          const yesterday = new Date();
          yesterday.setDate(yesterday.getDate() - 1);
          return { start: yesterday, end: yesterday };
        }},
        { label: 'Last 7 Days', getValue: () => {
          const end = new Date();
          const start = new Date();
          start.setDate(start.getDate() - 6);
          return { start, end };
        }},
        { label: 'Last 30 Days', getValue: () => {
          const end = new Date();
          const start = new Date();
          start.setDate(start.getDate() - 29);
          return { start, end };
        }},
        { label: 'This Month', getValue: () => {
          const now = new Date();
          const start = new Date(now.getFullYear(), now.getMonth(), 1);
          const end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
          return { start, end };
        }}
      ]
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
      // 将视频数据换为导出需格式
      return this.videos.map(video => ({
        handle: video.creators?.handle,
        // 可以添加其他需段
      }))
    },
    
    filteredData() {
      let filtered = [...this.videos];

      // 应用日期范围筛选
      if (this.dateRange.start && this.dateRange.end) {
        const startDate = new Date(this.dateRange.start);
        const endDate = new Date(this.dateRange.end);
        // 将结束日期设置为当天的最后一刻
        endDate.setHours(23, 59, 59, 999);
        
        filtered = filtered.filter(video => {
          const postedDate = new Date(video.posted_date);
          return postedDate >= startDate && postedDate <= endDate;
        });
      }

      // 应用观看次数筛选
      if (this.selectedViewCounts.length > 0) {
        filtered = filtered.filter(video => {
          const viewCount = video.views_count || 0;
          return this.selectedViewCounts.some(range => {
            if (range === '2000+') {
              return viewCount >= 2000;
            }
            
            const [min, max] = range.split('-').map(Number);
            if (max) {
              return viewCount >= min && viewCount <= max;
            }
            return viewCount >= min;
          });
        });
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
      
      // 调整起始位置，确保始终示5个页码
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
    },
    availableViewCounts() {
      return this.viewCountOptions.filter(
        option => !this.selectedViewCounts.includes(option.value)
      )
    },
    formatDateRange() {
      if (!this.dateRange.start || !this.dateRange.end) {
        return '';
      }
      const formatDate = (date) => {
        if (!date) return '';
        return new Date(date).toLocaleDateString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      };
      return `${formatDate(this.dateRange.start)} ~ ${formatDate(this.dateRange.end)}`;
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
      // 片加载失败使用默认图
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
        this.loading = true;
        this.error = null;
        
        const params = {
          page,
          pageSize: this.pageSize
        };
        
        if (this.searchQuery?.trim()) {
          params.search = this.searchQuery.trim();
        }

        // 修改日期范围参数的格式
        if (this.dateRange.start && this.dateRange.end) {
          // 确保开始日期是当天的开始
          const startDate = new Date(this.dateRange.start);
          startDate.setHours(0, 0, 0, 0);
          
          // 确保结束日期是当天的结束
          const endDate = new Date(this.dateRange.end);
          endDate.setHours(23, 59, 59, 999);
          
          params.startDate = startDate.toISOString();
          params.endDate = endDate.toISOString();
        }

        const response = await videoAPI.getVideos(params);
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
      
      // 算月份差异
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
      this.fetchVideos(1)
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
    },
    formatViewCount(value) {
      // 处理范围值
      if (value.includes('-')) {
        return value.replace('2000', '2K');
      }
      // 处理 2000+ 的情况
      if (value === '2000+') {
        return '2K+';
      }
      return value;
    },
    selectViewCount(value) {
      if (!this.selectedViewCounts.includes(value)) {
        this.selectedViewCounts.push(value);
      }
      this.showViewCountDropdown = false;
      this.applyViewCountFilter();
    },
    removeViewCount(value) {
      const index = this.selectedViewCounts.indexOf(value);
      if (index > -1) {
        this.selectedViewCounts.splice(index, 1);
      }
      this.applyViewCountFilter();
    },
    clearViewCounts() {
      this.selectedViewCounts = [];
      this.applyViewCountFilter();
    },
    applyViewCountFilter() {
      this.fetchVideos(1);
    },
    clearDateRange() {
      this.dateRange = {
        start: null,
        end: null
      };
      this.showDatePicker = false;
      this.fetchVideos(1);
    },
    applyDateRange() {
      if (this.dateRange.start && this.dateRange.end) {
        this.showDatePicker = false;
        this.fetchVideos(1);
      }
    },
    selectDatePreset(preset) {
      this.dateRange = preset.getValue();
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
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
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

/* 添加表��行高样式 */
th, td {
  height: 55px !important;
}

/* 或者使用 min-height 来确保最小高度 */
.min-h-16 {
  min-height: 55px;
}

/* 添加新的样式 */
.view-count-dropdown {
  max-height: 250px;
  overflow-y: auto;
}

.view-count-option {
  transition: background-color 0.2s ease;
}

.view-count-option:hover {
  background-color: #f3f4f6;
}

/* 下拉箭头动画 */
.dropdown-arrow {
  transition: transform 0.2s ease;
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.selected-tag {
  transition: all 0.2s ease;
}

.selected-tag:hover {
  background-color: #e5e7eb;
}

/* 日期选择器样式 */
.v-date-picker {
  font-family: inherit;
}

.date-preset-button {
  @apply px-3 py-1 text-sm rounded-md hover:bg-gray-100;
}

.date-preset-button.active {
  @apply bg-primary-600 text-white;
}

/* 确保日期选择器在其他元素之上 */
.date-picker-popup {
  z-index: 1000;
}
</style> 