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
      <div class="w-[300px]">
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
                :min-date="getMinDate()"
                :max-date="new Date()"
                :columns="2"
                :disabled-dates="[
                  {
                    start: new Date(0),
                    end: getMinDate()
                  }
                ]"
                :initial-page="new Date()"
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
      <div class="w-[400px]">
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
                v-for="option in filteredAvailableViewCounts"
                :key="option.value"
                @click.stop="selectViewCount(option.value)"
                class="px-4 py-2 text-sm hover:bg-gray-100 cursor-pointer"
              >
                {{ formatViewCount(option.value) }}
              </div>
              <!-- 添加一个提示，当所有选项都被选中时显示 -->
              <div
                v-if="filteredAvailableViewCounts.length === 0"
                class="px-4 py-2 text-sm text-gray-500"
              >
                No more options available
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
            <tr class="border-b bg-[#F8F9FB]">
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
            <!-- Loading State -->
            <template v-if="loading">
              <tr v-for="i in 10" :key="i" class="border-b animate-pulse h-[55px]">
                <td class="px-2 align-middle">
                  <div class="h-4 w-4 bg-gray-200 rounded"></div>
                </td>
                <td class="px-2 align-middle">
                  <div class="h-[40px] w-[30px] bg-gray-200 rounded-md"></div>
                </td>
                <td class="px-2 align-middle min-w-[200px]">
                  <div class="flex items-center gap-2">
                    <div class="h-8 w-8 bg-gray-200 rounded-full flex-shrink-0"></div>
                    <div class="h-4 w-32 bg-gray-200 rounded flex-1"></div>
                  </div>
                </td>
                <td class="px-2 align-middle min-w-[120px]">
                  <div class="h-4 w-24 bg-gray-200 rounded"></div>
                </td>
                <td class="px-2 align-middle min-w-[80px]">
                  <div class="h-4 w-16 bg-gray-200 rounded"></div>
                </td>
                <td class="px-2 align-middle min-w-[80px]">
                  <div class="h-4 w-16 bg-gray-200 rounded"></div>
                </td>
                <td class="px-2 align-middle min-w-[300px]">
                  <div class="h-4 w-full max-w-[400px] bg-gray-200 rounded"></div>
                </td>
                <td class="px-2 align-middle min-w-[200px]">
                  <div class="flex items-center gap-2">
                    <div class="h-8 w-8 bg-gray-200 rounded-md flex-shrink-0"></div>
                    <div class="h-4 w-32 bg-gray-200 rounded flex-1"></div>
                  </div>
                </td>
                <td class="px-2 align-middle min-w-[200px]">
                  <div class="flex items-center gap-2">
                    <div class="h-8 w-8 bg-gray-200 rounded-md flex-shrink-0"></div>
                    <div class="h-4 w-24 bg-gray-200 rounded flex-1"></div>
                  </div>
                </td>
              </tr>
            </template>

            <!-- Content -->
            <template v-else>
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
            </template>
          </tbody>
        </table>

      <!-- Error State -->
      <div v-if="error" class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ error }}
        <button 
          @click="fetchVideos()" 
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

    <!-- ExportModal 组件 -->
    <ExportModal
      v-if="showExportModal"
      :show="showExportModal"
      :influencers="selectedVideos.map(video => ({
        id: video.video_id,
        name: video.creator,
        avatar: video.creatorAvatar
      }))"
      @close="closeExportModal"
      @export="handleCreateList"
    />

    <!-- 添加点击其他区域关闭下拉框的处理 -->
    <div
      v-if="showViewCountDropdown"
      class="fixed inset-0 z-0"
      @click="showViewCountDropdown = false"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { videoAPI } from '@/services/videoAPI'
import ExportModal from '../components/ExportModal.vue'
import { DatePicker } from 'v-calendar'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

// 初始化响应式数据
const videos = ref([])
const loading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const selectedVideos = ref([])
const showExportModal = ref(false)
const searchQuery = ref('')
const selectedCreators = ref([])
const listName = ref('')

// 设置初始日期范围为当前月
const initializeDateRange = () => {
  const now = new Date()
  const firstDayOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
  return {
    start: firstDayOfMonth,
    end: now
  }
}

// 日期相关的响应式数据
const dateRange = ref(initializeDateRange())
const showDatePicker = ref(false)

// 视图数相关的响应式数据
const showViewCountDropdown = ref(false)
const selectedViewCounts = ref([])

// 视图数预设选项
const availableViewCounts = [
  { label: '0-1K', value: [0, 1000] },
  { label: '1K-10K', value: [1000, 10000] },
  { label: '10K-1M', value: [10000, 1000000] },
  { label: '1M+', value: [1000000, Infinity] }
]

// 日期预设选项
const datePresets = [
  { label: 'Last 7 days', value: 7 },
  { label: 'Last 14 days', value: 14 },
  { label: 'This month', value: 'thisMonth' },
  { label: 'Last month', value: 'lastMonth' }
]

// 计算最小允许日期（上个月的第一天）
const getMinDate = () => {
  const date = new Date()
  date.setDate(1) // 设置为当月第一天
  date.setMonth(date.getMonth() - 1) // 设置为上个月
  return date
}

// 计算属性
const hasSelectedVideos = computed(() => selectedVideos.value.length > 0)
const isCurrentPageAllSelected = computed(() => {
  return videos.value.length > 0 && 
         videos.value.every(video => selectedVideos.value.some(v => v.id === video.id))
})

const filteredVideos = computed(() => {
  return videos.value
})

// 添加分页相关的计算属性
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// 计算可见页码范围
const visiblePages = computed(() => {
  const maxVisiblePages = 5 // 最多显示5个页码
  const currentPageNum = currentPage.value
  const lastPage = totalPages.value
  
  if (lastPage <= maxVisiblePages) {
    // 如果总页数小于等于最大可见页数，返回2到最后一页的页码
    // 因为第1页会单独显示
    return Array.from({ length: lastPage - 1 }, (_, i) => i + 2)
  }
  
  // 计算页码范围
  let startPage = Math.max(currentPageNum - Math.floor(maxVisiblePages / 2), 2) // 从第2页开始
  let endPage = startPage + maxVisiblePages - 1
  
  // 调整范围确保不超出总页数
  if (endPage > lastPage) {
    endPage = lastPage
    startPage = Math.max(endPage - maxVisiblePages + 1, 2) // 确保从第2页开始
  }
  
  return Array.from(
    { length: endPage - startPage + 1 },
    (_, i) => startPage + i
  )
})

// 是否显示左侧省略号
const showLeftEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 2 // 修改为2
})

// 是否显示右侧省略号
const showRightEllipsis = computed(() => {
  return visiblePages.value[visiblePages.value.length - 1] < totalPages.value
})

// 获取视频列表方法
const fetchVideos = async () => {
  try {
    loading.value = true
    error.value = null
    
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      start_date: dateRange.value.start,
      end_date: dateRange.value.end,
      view_counts: selectedViewCounts.value
    }
    
    const response = await videoAPI.getVideosByDate(params)
    
    if (response.data) {
      videos.value = response.data
      total.value = response.total
    } else {
      // 处理空响应
      videos.value = []
      total.value = 0
      error.value = response.message || 'No data available'
    }
  } catch (err) {
    // 处理错误状态
    videos.value = []
    total.value = 0
    error.value = err.message || 'Failed to fetch videos'
    console.error('Error fetching videos:', err)
  } finally {
    loading.value = false
  }
}

// 修改分页方法
const goToPage = async (page) => {
  if (page === currentPage.value || page < 1 || page > totalPages.value) {
    return
  }
  
  currentPage.value = page
  await fetchVideos()
}

// 选择方法
const selectAll = (event) => {
  const isChecked = event.target.checked
  const currentPageVideoIds = videos.value.map(video => video.video_id)
  
  if (isChecked) {
    // 添加当前页未选中的视频
    videos.value.forEach(video => {
      if (!selectedVideos.value.some(v => v.video_id === video.video_id)) {
        selectedVideos.value.push(video)
        if (!selectedCreators.value.includes(video.creator)) {
          selectedCreators.value.push(video.creator)
        }
      }
    })
  } else {
    // 只移除当前页的选中项
    selectedVideos.value = selectedVideos.value.filter(video => 
      !currentPageVideoIds.includes(video.video_id)
    )
    
    // 重新计算selectedCreators
    const remainingCreators = new Set(
      selectedVideos.value.map(video => video.creator)
    )
    selectedCreators.value = Array.from(remainingCreators)
  }
}

const handleVideoSelect = (video, event) => {
  event.stopPropagation()
  
  const index = selectedVideos.value.findIndex(v => v.video_id === video.video_id)
  if (index === -1) {
    selectedVideos.value.push(video)
    if (!selectedCreators.value.includes(video.creator)) {
      selectedCreators.value.push(video.creator)
    }
  } else {
    selectedVideos.value.splice(index, 1)
    const hasOtherVideos = selectedVideos.value.some(v => 
      v.creator === video.creator
    )
    if (!hasOtherVideos) {
      const creatorIndex = selectedCreators.value.indexOf(video.creator)
      if (creatorIndex !== -1) {
        selectedCreators.value.splice(creatorIndex, 1)
      }
    }
  }
}

// 修改 ExportModal 相关的方法
const openExportModal = () => {
  if (selectedCreators.value.length === 0) {
    error.value = 'Please select at least one video first'
    return
  }
  showExportModal.value = true
}

const closeExportModal = () => {
  showExportModal.value = false
  listName.value = ''
}

// 清除选择
const clearSelection = () => {
  selectedVideos.value = []
  selectedCreators.value = []
}

// 图片错误处理
const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/40x40'
}

// 监听日期范围变化
watch(dateRange, () => {
  fetchVideos()
})

// 组件挂载时获取数据
onMounted(() => {
  fetchVideos()
})

// 在其他 const 声明之后添加这个函数
const getTimeAgo = (date) => {
      if (!date) return 'Unknown date'
      const now = new Date()
      const postedDate = new Date(date)
      const diffTime = Math.abs(now - postedDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
  if (diffDays > 30) {
      const months = Math.floor(diffDays / 30)
    return months === 1 ? 'a month ago' : `${months} months ago`
      } else {
    return diffDays === 1 ? '1 day ago' : `${diffDays} days ago`
  }
}

// 添加格式化数字的函数
const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 1000000) {
    return Math.floor(num / 1000000) + 'M'
  } else if (num >= 1000) {
    return Math.floor(num / 1000) + 'K'
  }
  return Math.floor(num).toString()
}

// 添加日期格式化函数
const formatDateRange = computed(() => {
  if (!dateRange.value.start || !dateRange.value.end) return ''
  const start = new Date(dateRange.value.start)
  const end = new Date(dateRange.value.end)
  return `${start.toLocaleDateString()} - ${end.toLocaleDateString()}`
})


// 修改日期预设选择方法
const selectDatePreset = (preset) => {
  const now = new Date()
  let start = new Date()
  let end = now

  switch (preset.value) {
    case 'thisMonth':
      start = new Date(now.getFullYear(), now.getMonth(), 1)
      break
    case 'lastMonth':
      start = new Date(now.getFullYear(), now.getMonth() - 1, 1)
      end = new Date(now.getFullYear(), now.getMonth(), 0) // 上月最后一天
      break
    default:
      start = new Date(now)
      start.setDate(start.getDate() - preset.value)
  }

  // 确保日期在允许范围内
  const minDate = getMinDate()
  if (start < minDate) {
    start = new Date(minDate)
  }

  dateRange.value = { start, end }
  fetchVideos()
}

const clearDateRange = () => {
  dateRange.value = initializeDateRange() // 重置为当前月
  showDatePicker.value = false
  fetchVideos()
}

const applyDateRange = () => {
  if (!dateRange.value.start || !dateRange.value.end) {
    dateRange.value = initializeDateRange() // 如果没有选择，重置为当前月
  }
  showDatePicker.value = false
  fetchVideos()
}

// 修改格式化函数以处理范围值
const formatViewCount = (range) => {
  if (Array.isArray(range)) {
    if (range[1] === Infinity) {
      return `${formatNumber(range[0])}+`
    }
    return `${formatNumber(range[0])}-${formatNumber(range[1])}`
  }
  return formatNumber(range)
}

// 修改选择视图数的方法
const selectViewCount = (range) => {
  const rangeKey = JSON.stringify(range) // 使用字符串作为键来比较数组
  if (!selectedViewCounts.value.some(v => JSON.stringify(v) === rangeKey)) {
    selectedViewCounts.value.push(range)
    fetchVideos()
  }
  showViewCountDropdown.value = false
}

// 修改移除视图数的方法
const removeViewCount = (range) => {
  const rangeKey = JSON.stringify(range)
  selectedViewCounts.value = selectedViewCounts.value.filter(
    v => JSON.stringify(v) !== rangeKey
  )
  fetchVideos()
}

// 修改过滤可用选项的计算属性
const filteredAvailableViewCounts = computed(() => {
  return availableViewCounts.filter(option => 
    !selectedViewCounts.value.some(
      selected => JSON.stringify(selected) === JSON.stringify(option.value)
    )
  )
})

// 添加视频详情导航方法
const goToVideoDetail = (video) => {
  router.push(`/videos/${video.video_id}`)
}

// 添加创建列表的方法
const handleCreateList = async ({ creators, name }) => {
  try {
    const listData = {
      name: name,
      type: 'Filters',
      description: 'Exported from videos',
      creators: creators.map(c => c.name), // 使用 creator.name 而不是 handle
      creatorUrls: creators.reduce((acc, c) => {
        acc[c.name] = `/videos/${c.id}`
        return acc
      }, {})
    }
    
    await store.dispatch('createList', listData)
    closeExportModal()
    router.push('/lists')
  } catch (error) {
    console.error('Failed to create list:', error)
  }
}

const router = useRouter()
const store = useStore()
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

/* 添加表行高样式 */
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