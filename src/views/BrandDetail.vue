<template>
  <div class="px-[50px] py-4">
    <!-- Back Button -->
    <div class="mb-6">
      <button 
        @click="$router.back()"
        class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
      >
        <svg 
          class="w-5 h-5" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
        <span>Back</span>
      </button>
    </div>

    <!-- 基础数据加载状态 -->
    <div v-if="loading" class="flex flex-col justify-center items-center min-h-[200px] space-y-4">
      <!-- 主加载动画 -->
      <div class="relative">
        <div class="w-16 h-16 border-4 border-gray-200 rounded-full animate-spin">
          <div class="absolute top-0 left-0 w-16 h-16 border-4 border-primary-600 rounded-full animate-loading"></div>
        </div>
      </div>
      <!-- 加载文字 -->
      <div class="text-gray-500 font-medium animate-pulse">Loading brand details...</div>
    </div>

    <!-- 基础数据错误状态 -->
    <div v-else-if="error" class="flex flex-col items-center justify-center min-h-[200px]">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button 
        @click="fetchBrandData"
        class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-500"
      >
        Retry
      </button>
    </div>

    <template v-else-if="brand">
      <!-- Brand Header -->
      <div class="flex flex-col items-center justify-center mb-8">
        <div class="w-[128px] h-[128px] mb-4">
          <img 
            :src="brand.image" 
            :alt="brand.name"
            class="w-full h-full rounded-lg object-cover"
            @error="handleImageError"
          >
        </div>
        <h1 class="text-2xl font-bold">{{ brand.name }}</h1>
      </div>

      <!-- Products Section -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold mb-4">Products</h2>
        <div class="relative w-full">
          <div class="bg-white rounded-sm border border-secondary-100">
            <!-- Loading Skeleton -->
            <div v-if="productsLoading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
            <table class="w-full caption-bottom text-sm">
              <thead class="[&_tr]:border-b">
                <tr class="border-b">
                  <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[55%]">Product</th>
                  <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[20%]">Price</th>
                  <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[25%]">Sold Count</th>
                </tr>
              </thead>
              <tbody class="[&_tr:last-child]:border-0">
                <!-- Skeleton Rows when loading -->
                <template v-if="productsLoading">
                  <tr v-for="i in 10" :key="i" class="border-b">
                    <td class="min-h-16 py-3 px-2 align-middle">
                      <div class="flex items-center gap-3">
                        <div class="w-12 h-12 rounded-md bg-gray-200 animate-pulse"></div>
                        <div class="h-4 bg-gray-200 rounded w-3/4 animate-pulse"></div>
                      </div>
                    </td>
                    <td class="min-h-16 py-3 px-2 align-middle">
                      <div class="h-4 bg-gray-200 rounded w-16 animate-pulse"></div>
                    </td>
                    <td class="min-h-16 py-3 px-2 align-middle">
                      <div class="h-4 bg-gray-200 rounded w-20 animate-pulse"></div>
                    </td>
                  </tr>
                </template>
                <!-- Actual Data -->
                <template v-else>
                  <tr 
                    v-for="product in products" 
                    :key="product.id"
                    class="border-b transition-colors duration-200 ease-curve hover:bg-secondary-100 cursor-pointer group"
                    @click="goToProductDetail(product.id)"
                  >
                    <td class="min-h-16 py-3 px-2 align-middle relative w-[55%]">
                      <div class="flex items-center gap-3 max-w-full">
                        <img 
                          :src="product.image" 
                          :alt="product.name"
                          class="w-10 h-10 rounded-md object-cover flex-shrink-0"
                        >
                        <div class="min-w-0 flex-1">
                          <span class="block truncate">{{ product.name }}</span>
                        </div>
                        <!-- 悬浮提示框 -->
                        <div 
                          class="absolute left-0 top-full mt-2 p-2 bg-gray-900 text-white rounded-md shadow-lg z-10 max-w-md 
                                 invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-200"
                        >
                          {{ product.name }}
                        </div>
                      </div>
                    </td>
                    <td class="min-h-16 py-3 px-2 align-middle w-[20%]">${{ product.price ? product.price.toFixed(2) : '0.00' }}</td>
                    <td class="min-h-16 py-3 px-2 align-middle w-[25%]">{{ formatNumber(product.soldCount || 0) }}</td>
                  </tr>
                </template>
              </tbody>
            </table>

            <!-- Products Pagination -->
            <div class="mt-4 flex justify-between items-center p-4">
              <div class="text-sm text-gray-700">
                Showing {{ productsStartIndex }} to {{ Math.min(productsEndIndex, totalProducts) }} of {{ totalProducts }}
              </div>

              <div class="flex-1 flex justify-center">
                <div class="flex items-center space-x-1">
                  <button 
                    @click="prevProductsPage"
                    :disabled="productsCurrentPage === 1"
                    class="px-2 py-1 text-gray-600 hover:text-primary-600"
                  >
                    <span class="text-sm">‹</span>
                  </button>

                  <template v-for="n in productsDisplayedPages" :key="n">
                    <button 
                      v-if="n !== '...'"
                      @click="changeProductsPage(n)"
                      class="px-3 py-1 rounded"
                      :class="[
                        productsCurrentPage === n 
                          ? 'bg-[#6366F1] text-white' 
                          : 'text-gray-600 hover:text-primary-600'
                      ]"
                    >
                      {{ n }}
                    </button>
                    <span v-else class="px-2">...</span>
                  </template>

                  <button 
                    @click="nextProductsPage"
                    :disabled="productsCurrentPage === productsTotalPages"
                    class="px-2 py-1 text-gray-600 hover:text-primary-600"
                  >
                    <span class="text-sm">›</span>
                  </button>
                </div>
              </div>

              <div class="invisible text-sm text-gray-700">
                Showing {{ productsStartIndex }} to {{ Math.min(productsEndIndex, totalProducts) }} of {{ totalProducts }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Videos Section -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold">Top videos featuring this brand</h2>
          <div class="flex items-center space-x-4">
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
        </div>

        <!-- Videos Content -->
        <div v-if="videos.length > 0" class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
          <!-- Loading Skeleton -->
          <div v-if="videosLoading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
          <table class="w-full caption-bottom text-sm">
            <thead class="[&_tr]:border-b">
              <tr class="border-b">
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[5%]">
                  <input 
                    type="checkbox" 
                    class="rounded border-gray-300"
                    :checked="isCurrentPageAllSelected"
                    @change="selectAll"
                  >
                </th>
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[10%]">Thumbnail</th>
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[20%]">Creator</th>
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[15%]">Posted Time</th>
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[15%]">Views</th>
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[15%]">Likes</th>
                <th class="h-[90px] py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[25%]">Product</th>
              </tr>
            </thead>
            <tbody class="[&_tr:last-child]:border-0">
              <!-- Skeleton Rows when loading -->
              <template v-if="videosLoading">
                <tr v-for="i in 10" :key="i" class="border-b h-[90px]">
                  <td class="py-3 px-2 align-middle">
                    <div class="w-4 h-4 bg-gray-200 rounded animate-pulse"></div>
                  </td>
                  <td class="py-3 px-2 align-middle">
                    <div class="w-[63px] h-[112px] bg-gray-200 rounded-md animate-pulse"></div>
                  </td>
                  <td class="py-3 px-2 align-middle">
                    <div class="flex items-center gap-2">
                      <div class="w-8 h-8 bg-gray-200 rounded-full animate-pulse"></div>
                      <div class="h-4 bg-gray-200 rounded w-32 animate-pulse"></div>
                    </div>
                  </td>
                  <td class="py-3 px-2 align-middle">
                    <div class="h-4 bg-gray-200 rounded w-24 animate-pulse"></div>
                  </td>
                  <td class="py-3 px-2 align-middle">
                    <div class="h-4 bg-gray-200 rounded w-16 animate-pulse"></div>
                  </td>
                  <td class="py-3 px-2 align-middle">
                    <div class="h-4 bg-gray-200 rounded w-16 animate-pulse"></div>
                  </td>
                  <td class="py-3 px-2 align-middle">
                    <div class="flex items-center gap-2">
                      <div class="w-10 h-10 bg-gray-200 rounded-md animate-pulse"></div>
                      <div class="h-4 bg-gray-200 rounded w-40 animate-pulse"></div>
                    </div>
                  </td>
                </tr>
              </template>
              <!-- Actual Data -->
              <template v-else>
                <tr 
                  v-for="video in videos" 
                  :key="video.id"
                  class="border-b transition-colors duration-200 ease-curve hover:bg-secondary-100 cursor-pointer h-[90px]"
                  @click="goToVideoDetail(video.id)"
                >
                  <td class="h-[90px] py-3 px-2 align-middle" @click.stop>
                    <input 
                      type="checkbox" 
                      class="rounded border-gray-300"
                      :checked="selectedVideos.some(v => v.id === video.id)"
                      @change="handleVideoSelect(video, $event)"
                    >
                  </td>
                  <td class="h-[90px] py-3 px-2 align-middle">
                    <div class="flex items-center h-full">
                      <img 
                        :src="video.thumbnail" 
                        :alt="video.title"
                        class="w-[63px] h-[112px] rounded-md object-cover"
                      >
                    </div>
                  </td>
                  <td class="h-[90px] py-3 px-2 align-middle relative group">
                    <div class="flex items-center gap-2">
                      <img 
                        :src="video.creatorAvatar" 
                        :alt="video.creator"
                        class="w-8 h-8 rounded-full object-cover flex-shrink-0"
                      >
                      <div class="min-w-0 flex-1">
                        <span class="block truncate">{{ video.creator }}</span>
                      </div>
                    </div>
                    <!-- Creator 悬浮提示 -->
                    <div 
                      class="absolute left-0 top-full mt-2 p-2 bg-gray-900 text-white rounded-md shadow-lg z-10 max-w-md 
                             invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-200"
                    >
                      {{ video.creator }}
                    </div>
                  </td>
                  <td class="h-[90px] py-3 px-2 align-middle whitespace-nowrap">{{ video.postedTime }}</td>
                  <td class="h-[90px] py-3 px-2 align-middle">{{ formatNumber(video.views || 0) }}</td>
                  <td class="h-[90px] py-3 px-2 align-middle">{{ formatNumber(video.likes || 0) }}</td>
                  <td class="h-[90px] py-3 px-2 align-middle relative group">
                    <div class="flex items-center gap-3 max-w-full">
                      <img 
                        :src="video.productImage" 
                        :alt="video.productName"
                        class="w-10 h-10 rounded-md object-cover flex-shrink-0"
                      >
                      <div class="min-w-0 flex-1">
                        <span class="block truncate">{{ video.productName }}</span>
                      </div>
                    </div>
                    <!-- Product 悬浮提示 -->
                    <div 
                      class="absolute left-0 top-full mt-2 p-2 bg-gray-900 text-white rounded-md shadow-lg z-10 max-w-md 
                             invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-200"
                    >
                      {{ video.productName }}
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>

          <!-- Videos Pagination -->
          <div class="mt-4 flex justify-between items-center p-4">
            <div class="text-sm text-gray-700">
              Showing {{ videosStartIndex }} to {{ Math.min(videosEndIndex, totalVideos) }} of {{ totalVideos }}
            </div>

            <div class="flex-1 flex justify-center">
              <div class="flex items-center space-x-1">
                <button 
                  @click="prevVideosPage"
                  :disabled="videosCurrentPage === 1"
                  class="px-2 py-1 text-gray-600 hover:text-primary-600"
                >
                  <span class="text-sm">‹</span>
                </button>

                <template v-for="n in videosDisplayedPages" :key="n">
                  <button 
                    v-if="n !== '...'"
                    @click="changeVideosPage(n)"
                    class="px-3 py-1 rounded"
                    :class="[
                      videosCurrentPage === n 
                        ? 'bg-[#6366F1] text-white' 
                        : 'text-gray-600 hover:text-primary-600'
                    ]"
                  >
                    {{ n }}
                  </button>
                  <span v-else class="px-2">...</span>
                </template>

                <button 
                  @click="nextVideosPage"
                  :disabled="videosCurrentPage === videosTotalPages"
                  class="px-2 py-1 text-gray-600 hover:text-primary-600"
                >
                  <span class="text-sm">›</span>
                </button>
              </div>
            </div>

            <div class="invisible text-sm text-gray-700">
              Showing {{ videosStartIndex }} to {{ Math.min(videosEndIndex, totalVideos) }} of {{ totalVideos }}
            </div>
          </div>
        </div>
        <div v-else class="text-center text-gray-500 py-8">
          No videos available
        </div>
      </div>

      <!-- Demographics Charts -->
      <div class="mt-8">
        <!-- Analytics Error State -->
        <div v-if="analyticsError" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p class="text-red-600">{{ analyticsError }}</p>
          <button 
            @click="retryAnalytics"
            class="mt-2 px-4 py-2 text-sm text-primary-600 hover:text-primary-500"
          >
            Retry loading demographics
          </button>
        </div>

        <!-- Analytics Loading State -->
        <div v-else-if="analyticsLoading" class="flex flex-col justify-center items-center min-h-[200px] space-y-4">
          <div class="relative">
            <div class="w-16 h-16 border-4 border-gray-200 rounded-full animate-spin">
              <div class="absolute top-0 left-0 w-16 h-16 border-4 border-primary-600 rounded-full animate-loading"></div>
            </div>
          </div>
          <div class="text-gray-500 font-medium animate-pulse">Loading demographics data...</div>
        </div>

        <template v-else>
          <CreatorDemographics 
            v-if="creatorDemographics.gender"
            :data="creatorDemographics" 
            class="mb-8"
          />
          <AudienceDemographics 
            v-if="audienceDemographics.gender"
            :data="audienceDemographics" 
            class="mb-8"
          />
        </template>
      </div>

      <!-- Modal -->
      <div v-if="showCreateListModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-[500px]">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold">Create New List</h3>
            <button @click="showCreateListModal = false" class="text-gray-500 hover:text-gray-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">List Name</label>
              <input 
                v-model="listName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
            </div>
          </div>

          <div class="mt-6 flex justify-end">
            <button 
              @click="showCreateListModal = false"
              class="mr-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
            >
              Cancel
            </button>
            <button 
              @click="handleCreateList"
              class="px-4 py-2 text-sm text-white bg-primary-600 hover:bg-primary-700 rounded-md"
            >
              Create
            </button>
          </div>
        </div>
      </div>

      <!-- 添加导出模态框组件 -->
      <ExportModal
        v-if="showExportModal"
        :show="showExportModal"
        :influencers="selectedCreators"
        @close="closeExportModal"
      />
    </template>
  </div>
</template>

<script>
import CreatorDemographics from '../components/CreatorDemographics.vue'
import AudienceDemographics from '../components/AudienceDemographics.vue'
import brandAPI from '../services/brandAPI'
import ExportModal from '../components/ExportModal.vue'

export default {
  name: 'BrandDetail',
  components: {
    CreatorDemographics,
    AudienceDemographics,
    ExportModal
  },
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      brand: null,
      
      productsLoading: false,
      productsError: null,
      products: [],
      totalProducts: 0,
      
      // 初始化视频相关数据
      videos: [],
      totalVideos: 0,
      videosLoading: false,
      videosError: null,
      
      analyticsLoading: false,
      analyticsError: null,
      
      // 初始化 demographics 数据
      creatorDemographics: {
        gender: {
          female: 0,
          male: 0
        },
        language: {}
      },
      audienceDemographics: {
        gender: {
          female: 0,
          male: 0
        },
        age: {
          '18-24': 0,
          '25-34': 0,
          '35-44': 0,
          '45-54': 0,
          '55+': 0
        },
        locations: []
      },
      
      itemsPerPage: 10,
      productsCurrentPage: 1,
      videosCurrentPage: 1,
      
      showCreateListModal: false,
      listName: '',
      
      showExportModal: false,
      selectedCreators: [],
      selectedVideos: []
    }
  },
  created() {
    this.fetchBrandData()
  },
  computed: {
    // Products pagination
    productsStartIndex() {
      return this.totalProducts === 0 ? 0 : (this.productsCurrentPage - 1) * this.itemsPerPage + 1;
    },
    productsEndIndex() {
      return Math.min(this.productsCurrentPage * this.itemsPerPage, this.totalProducts);
    },
    productsTotalPages() {
      return Math.ceil(this.totalProducts / this.itemsPerPage);
    },
    
    // Videos pagination
    videosStartIndex() {
      return this.totalVideos === 0 ? 0 : (this.videosCurrentPage - 1) * this.itemsPerPage + 1;
    },
    videosEndIndex() {
      return Math.min(this.videosCurrentPage * this.itemsPerPage, this.totalVideos);
    },
    videosTotalPages() {
      return Math.ceil(this.totalVideos / this.itemsPerPage);
    },
    
    productsDisplayedPages() {
      const totalPages = this.productsTotalPages;
      const currentPage = this.productsCurrentPage;
      const pages = [];
      
      if (totalPages <= 7) {
        // 如果总页数小于等于7，显示所有页码
        for (let i = 1; i <= totalPages; i++) {
          pages.push(i);
        }
      } else {
        // 总是显示第一页
        pages.push(1);
        
        if (currentPage > 3) {
          // 如果当前页大于3，添加省略号
          pages.push('...');
        }
        
        // 确定中间页码的范围
        let start = Math.max(2, currentPage - 2);
        let end = Math.min(totalPages - 1, currentPage + 2);
        
        // 如果当前页接近开始或结束，调整范围
        if (currentPage <= 3) {
          end = 5;
        }
        if (currentPage >= totalPages - 2) {
          start = totalPages - 4;
        }
        
        // 添加中间的页码
        for (let i = start; i <= end; i++) {
          pages.push(i);
        }
        
        if (currentPage < totalPages - 2) {
          // 如果当前页小于倒数第三页，添加省略号
          pages.push('...');
        }
        
        // 总显示最后一页
        if (totalPages > 1) {
          pages.push(totalPages);
        }
      }
      
      return pages;
    },
    videosDisplayedPages() {
      const totalPages = this.videosTotalPages;
      const currentPage = this.videosCurrentPage;
      const pages = [];
      
      if (totalPages <= 7) {
        // 如果总页数小于等于7，显示所有页码
        for (let i = 1; i <= totalPages; i++) {
          pages.push(i);
        }
      } else {
        // 总是显示第一页
        pages.push(1);
        
        if (currentPage > 3) {
          // 如果当前页大于3，添加省略号
          pages.push('...');
        }
        
        // 确定中间页码的范围
        let start = Math.max(2, currentPage - 2);
        let end = Math.min(totalPages - 1, currentPage + 2);
        
        // 如果当前页接近开始或结束，调整范围
        if (currentPage <= 3) {
          end = 5;
        }
        if (currentPage >= totalPages - 2) {
          start = totalPages - 4;
        }
        
        // 添加中间的页码
        for (let i = start; i <= end; i++) {
          pages.push(i);
        }
        
        if (currentPage < totalPages - 2) {
          // 如果当前页小于倒数第三页，添加省略号
          pages.push('...');
        }
        
        // 总是显示最后一页
        if (totalPages > 1) {
          pages.push(totalPages);
        }
      }
      
      return pages;
    },
    hasSelectedVideos() {
      return this.selectedCreators.length > 0;
    },
    isCurrentPageAllSelected() {
      return this.videos.length > 0 && 
        this.videos.every(video => this.selectedVideos.some(v => v.id === video.id))
    }
  },
  methods: {
    formatNumber(value) {
      // 添加防护，处理 undefined 或 null 值
      if (value === undefined || value === null) {
        return '0';
      }
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    // Products pagination methods
    async changeProductsPage(page) {
      this.productsCurrentPage = page;
      await this.fetchProducts(); // 重新获取数据
    },

    async prevProductsPage() {
      if (this.productsCurrentPage > 1) {
        this.productsCurrentPage--;
        await this.fetchProducts(); // 重新获取数据
      }
    },

    async nextProductsPage() {
      if (this.productsCurrentPage < this.productsTotalPages) {
        this.productsCurrentPage++;
        await this.fetchProducts(); // 重新获取数据
      }
    },

    // 修改 fetchProducts 方法，加分页参数
    async fetchProducts() {
      this.productsLoading = true;
      this.productsError = null;
      
      try {
        const productsResponse = await brandAPI.getBrandProducts(
          this.id,
          this.productsCurrentPage, // 传入当前页码
          this.itemsPerPage // 传入每页数量
        );
        
        if (productsResponse && productsResponse.data) {
          this.products = productsResponse.data.map(product => ({
            id: product.product_id,
            name: product.title || '',
            image: product.product_url || '',
            price: parseFloat(product.real_price || 0),
            soldCount: parseInt(product.sold_count || 0)
          }));
          this.totalProducts = productsResponse.total || 0;
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        this.productsError = 'Failed to load products. Please try again.';
      } finally {
        this.productsLoading = false;
      }
    },

    // 修改 videos 分页相关的方法
    async changeVideosPage(page) {
      this.videosCurrentPage = page;
      await this.fetchVideos();
    },

    async prevVideosPage() {
      if (this.videosCurrentPage > 1) {
        this.videosCurrentPage--;
        await this.fetchVideos();
      }
    },

    async nextVideosPage() {
      if (this.videosCurrentPage < this.videosTotalPages) {
        this.videosCurrentPage++;
        await this.fetchVideos();
      }
    },

    async fetchVideos() {
      this.videosLoading = true;
      this.videosError = null;
      
      try {
        const videosResponse = await brandAPI.getBrandVideos(
          this.id,
          this.videosCurrentPage,
          this.itemsPerPage
        );
        
        if (videosResponse && videosResponse.data) {
          this.videos = videosResponse.data.map(video => ({
            id: video.video_id,
            thumbnail: video.thumbnail_url,
            title: video.description,
            creator: video.creators.handle,
            creatorAvatar: video.creator_profile_url,
            // 转换posted_date为相对时间
            postedTime: this.getRelativeTime(video.posted_date),
            views: video.views_count,
            likes: video.likes_count,
            productImage: video.seller_product_photo_url,
            productName: video.seller_products.title
          }));
          this.totalVideos = videosResponse.total || 0;
        }
      } catch (error) {
        console.error('Error fetching videos:', error);
        this.videosError = 'Failed to load videos. Please try again.';
      } finally {
        this.videosLoading = false;
      }
    },

    // 添加一个新的方法来计算相对时间
    getRelativeTime(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      const diffMonths = Math.floor(diffDays / 30);

      if (diffDays < 30) {
        return diffDays === 1 ? '1 day ago' : `${diffDays} days ago`;
      } else {
        return diffMonths === 1 ? '1 month ago' : `${diffMonths} months ago`;
      }
    },
    handleImageError(e) {
      e.target.src = '/default-brand.png'
    },
    async fetchBrandData() {
      this.loading = true;
      this.error = null;
      
      try {
        // 只获取基本数据
        const response = await brandAPI.getBrandDetails(this.id);
        
        if (response) {
          this.brand = {
            id: response.seller_id,
            name: response.name,
            image: response.brand_url || '/default-brand.png',
            num_products: response.num_products,
            total_sales: response.total_sales
          };
          
          // 基本数据加载完成后，并行加载其他数据
          Promise.all([
            this.fetchProducts(),
            this.fetchVideos(),
            this.fetchAnalytics()
          ]);
        }
      } catch (error) {
        console.error('Error fetching brand data:', error);
        this.error = 'Failed to load brand data. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    async fetchAnalytics() {
      this.analyticsLoading = true;
      this.analyticsError = null;
      
      try {
        const analyticsData = await brandAPI.getBrandAnalytics(this.id);
        
        if (analyticsData && analyticsData.data) {
          const data = analyticsData.data;
          
          // 确保数据存在并进行安全的赋值
          this.creatorDemographics = {
            gender: {
              female: data.creator_genders?.female || 0,
              male: data.creator_genders?.male || 0
            },
            language: data.creator_languages || {}
          };

          this.audienceDemographics = {
            gender: {
              female: data.follower_genders?.female || 0,
              male: data.follower_genders?.male || 0
            },
            age: data.follower_ages || {
              '18-24': 0,
              '25-34': 0,
              '35-44': 0,
              '45-54': 0,
              '55+': 0
            },
            locations: Object.entries(data.follower_locations || {})
              .map(([name, value]) => ({
                name,
                value
              }))
          };
        }
      } catch (error) {
        console.error('Error fetching analytics:', error);
        this.analyticsError = 'Failed to load demographics data. Please try again later.';
      } finally {
        this.analyticsLoading = false;
      }
    },
    goToProductDetail(productId) {
      this.$router.push(`/products/${productId}`);
    },
    goToVideoDetail(videoId) {
      this.$router.push(`/videos/${videoId}`);
    },
    async handleCreateList() {
      try {
        // 使用完整的videos数组而不是paginatedVideos
        const creators = this.videos.map(video => ({
          handle: video.creator,
          profileUrl: `/videos/${video.id}` // 使用视频详情页面的URL
        }));
        
        const listData = {
          name: this.listName,
          type: 'Filters',
          description: 'Exported from brands',
          creators: creators.map(c => c.handle),
          creatorUrls: creators.reduce((acc, c) => {
            acc[c.handle] = c.profileUrl;
            return acc;
          }, {})
        };
        
        await this.$store.dispatch('createList', listData);
        this.showCreateListModal = false;
        this.listName = '';
        this.$router.push('/lists');
      } catch (error) {
        console.error('Failed to create list:', error);
      }
    },
    async retryAnalytics() {
      this.analyticsLoading = true;
      this.analyticsError = null;

      try {
        const analyticsData = await brandAPI.getBrandAnalytics(this.id);
        
        if (analyticsData && analyticsData.data) {
          const data = analyticsData.data;
          
          // 更新 Creator Demographics 数据
          this.creatorDemographics = {
            gender: {
              female: data.creator_genders?.female || 0,
              male: data.creator_genders?.male || 0
            },
            language: data.creator_languages || {}
          };

          // 更新 Audience Demographics 数据
          this.audienceDemographics = {
            gender: {
              female: data.follower_genders?.female || 0,
              male: data.follower_genders?.male || 0
            },
            age: data.follower_ages || {
              '18-24': 0,
              '25-34': 0,
              '35-44': 0,
              '45-54': 0,
              '55+': 0
            },
            locations: Object.entries(data.follower_locations || {})
              .map(([name, value]) => ({
                name,
                value
              }))
          };
        }
      } catch (error) {
        console.error('Error retrying analytics:', error);
        this.analyticsError = `Failed to load demographics data: ${error.message}`;
      } finally {
        this.analyticsLoading = false;
      }
    },
    formatProductName(name) {
      // 如果名称长度超过200个字符，截取200个字符并添加省略号
      if (name.length > 350) {
        return name.substring(0, 350) + '...';
      }
      return name;
    },
    openExportModal() {
      if (this.selectedCreators.length === 0) {
        alert('Please select at least one video first')
        return
      }
      this.showExportModal = true
    },
    closeExportModal() {
      this.showExportModal = false
    },
    handleVideoSelect(video, event) {
      event.stopPropagation()
      
      const index = this.selectedVideos.findIndex(v => v.id === video.id)
      if (index === -1) {
        this.selectedVideos.push(video)
        if (!this.selectedCreators.includes(video.creator)) {
          this.selectedCreators.push(video.creator)
        }
      } else {
        this.selectedVideos.splice(index, 1)
        const hasOtherVideos = this.selectedVideos.some(v => v.creator === video.creator)
        if (!hasOtherVideos) {
          const creatorIndex = this.selectedCreators.indexOf(video.creator)
          if (creatorIndex !== -1) {
            this.selectedCreators.splice(creatorIndex, 1)
          }
        }
      }
    },
    selectAll(event) {
      const isChecked = event.target.checked
      const currentPageVideoIds = this.videos.map(video => video.id)
      
      if (isChecked) {
        this.videos.forEach(video => {
          if (!this.selectedVideos.some(v => v.id === video.id)) {
            this.selectedVideos.push(video)
            if (!this.selectedCreators.includes(video.creator)) {
              this.selectedCreators.push(video.creator)
            }
          }
        })
      } else {
        this.selectedVideos = this.selectedVideos.filter(video => 
          !currentPageVideoIds.includes(video.id)
        )
        
        this.selectedCreators = []
        this.selectedVideos.forEach(video => {
          if (!this.selectedCreators.includes(video.creator)) {
            this.selectedCreators.push(video.creator)
          }
        })
      }
    },
    clearSelection() {
      this.selectedVideos = []
      this.selectedCreators = []
    }
  }
}
</script>

<style scoped>
.text-primary-600 {
  color: #6366F1;
}

.hover\:text-primary-600:hover {
  color: #6366F1;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button {
  transition: all 0.2s ease-in-out;
}

/* 确保表格单元格内容溢出时显示省略号 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: calc(100% - 3rem); /* 减去图标和间距的宽度 */
}

/* 悬浮提示框的样式 */
.group:hover .group-hover\:visible {
  visibility: visible;
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

@keyframes loading {
  0% {
    clip-path: polygon(50% 50%, 0 0, 0 0, 0 0, 0 0, 0 0);
  }
  25% {
    clip-path: polygon(50% 50%, 0 0, 100% 0, 100% 0, 100% 0, 100% 0);
  }
  50% {
    clip-path: polygon(50% 50%, 0 0, 100% 0, 100% 100%, 100% 100%, 100% 100%);
  }
  75% {
    clip-path: polygon(50% 50%, 0 0, 100% 0, 100% 100%, 0 100%, 0 100%);
  }
  100% {
    clip-path: polygon(50% 50%, 0 0, 100% 0, 100% 100%, 0 100%, 0 0);
  }
}

.animate-loading {
  animation: loading 1.5s ease-in-out infinite;
}
</style> 