<template>
  <div class="px-[50px] py-4" v-if="product">
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

    <!-- 产品卡片部分 -->
    <div class="w-full max-w-2xl m-auto my-8 border rounded-[12px] border-secondary-300 flex">
      <div class="relative group">
        <img 
          :src="`https://btsplwsgjvpilxywmaba.supabase.co/storage/v1/object/public/seller_products_photos/${product.id}.jpg`"
          :alt="product.title"
          class="h-full rounded-l-[12px] min-w-[250px]"
        >
      </div>
      <div class="w-full py-4">
        <h2 class="text-[40px] leading-[48px] font-bold text-textPrimary px-4">
          <button class="w-fit !ring-0 text-left line-clamp-4">
            {{ product.title }}
          </button>
        </h2>
        <p class="text-[16px] text-gray-600 px-4 mt-2">
          {{ product.seller_name }}
        </p>
      </div>
    </div>

    <!-- 视频格式部分 -->
    <h2 class="text-xl font-semibold mt-10 mb-2">Top Video Formats</h2>
    <div class="flex gap-4 flex-wrap">
      <button 
        v-for="format in videoFormats" 
        :key="format.video_format_name"
        @click="openFormatModal(format)"
        class="py-2.5 px-6 text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed border bg-transparent border-secondary-400 hover:bg-secondary-100 disabled:bg-transparent disabled:text-secondary-400 disabled:border-secondary-600 text-primary-500 focus:bg-primary-100 focus:border-primary-500 active:bg-primary-100 h-[46px]"
      >
        {{ format.video_format_name }}
      </button>
    </div>

    <!-- Top Selling Points 部分 -->
    <div class="mt-10">
      <h2 class="text-xl font-semibold mb-4">Top Selling Points</h2>
      <div class="grid grid-cols-2 gap-x-8 gap-y-4">
        <div 
          v-for="(point, index) in paginatedSellingPoints" 
          :key="index"
          class="flex items-center gap-4 p-2 rounded-md"
        >
          <span class="w-3 text-gray-500">{{ index + 1 }}</span>
          <div class="flex items-center gap-3 flex-1">
            <img 
              :src="point.creator_profile_url"
              class="w-8 h-8 rounded-full object-cover"
              alt="Creator"
            >
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-2 relative group">
                <div class="bg-[#F1F3F5] hover:bg-[#E9ECEF] rounded-md px-3 py-2">
                  <p class="text-sm text-gray-900 max-w-[490px] truncate">{{ point.selling_point_phrasing }}</p>
            </div>
                <div class="flex items-center gap-1.5 text-neutral-400 text-[12px] whitespace-nowrap flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary flex-shrink-0">
              <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
              <polyline points="16 7 22 7 22 13"></polyline>
            </svg>
                  <span>{{ formatNumber(point.views_count) }} views</span>
                </div>
                <!-- 悬停时显示的完整内容 -->
                <div 
                  class="absolute left-0 top-full mt-2 p-2 bg-gray-900 text-white rounded-md shadow-lg z-10 max-w-md 
                         invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-200"
                >
                  {{ point.selling_point_phrasing }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Hooks 部分 -->
    <div class="mt-10">
      <h2 class="text-xl font-semibold mb-4">Top Hooks</h2>
        <div class="grid grid-cols-2 gap-x-8 gap-y-4">
          <div 
          v-for="(hook, index) in hooks" 
            :key="index" 
          class="flex items-center gap-4 p-2 rounded-md"
        >
          <span class="w-3 text-gray-500">{{ index + 1 }}</span>
          <div class="flex items-center gap-3 flex-1">
            <img 
              :src="hook.creator_profile_url"
              class="w-8 h-8 rounded-full object-cover"
              alt="Creator"
            >
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-2 relative group">
                <div class="bg-[#F1F3F5] hover:bg-[#E9ECEF] rounded-md px-3 py-2">
                  <p class="text-sm text-gray-900 max-w-[490px] truncate">{{ hook.hook_phrasing }}</p>
            </div>
                <div class="flex items-center gap-1.5 text-neutral-400 text-[12px] whitespace-nowrap flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary flex-shrink-0">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                <polyline points="16 7 22 7 22 13"></polyline>
              </svg>
                  <span>{{ formatNumber(hook.views_count) }} views</span>
                </div>
                <!-- 悬停时显示的完整内容 -->
                <div 
                  class="absolute left-0 top-full mt-2 p-2 bg-gray-900 text-white rounded-md shadow-lg z-10 max-w-md 
                         invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-200"
                >
                  {{ hook.hook_phrasing }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Format详情模��� -->
    <div v-if="showFormatModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-[500px]">
        <!-- 标题和关闭按钮 -->
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold">{{ selectedFormat.video_format_name }}</h3>
          <button @click="showFormatModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 描述部分 -->
        <p class="text-[14px] leading-[20px] text-gray-600 mb-4">
          {{ selectedFormat.description }}
        </p>

        <!-- Tips部分 -->
        <div class="mb-4">
          <p class="text-[14px] leading-[20px] text-gray-600">
            <span class="font-medium">Tips:</span> {{ selectedFormat.tips_to_use }}
          </p>
        </div>

        <!-- 示例部分 -->
        <div class="mt-4" v-if="selectedFormat.examples && selectedFormat.examples.length > 0">
          <div class="relative w-[250px] mx-auto" style="padding-top: 88.89%">
            <img 
              :src="`https://btsplwsgjvpilxywmaba.supabase.co/storage/v1/object/public/creator_videos_photos/${selectedFormat.examples[0].video_id}.webp`"
              class="absolute top-0 left-0 w-full h-full object-cover rounded-lg"
              alt="Example"
            >
          </div>
          <p class="text-[12px] leading-[16px] text-gray-500 mt-2">
            {{ selectedFormat.examples[0].explanation }}
          </p>
        </div>

        <!-- 关闭按钮 -->
        <div class="mt-6 flex justify-end">
          <button 
            @click="showFormatModal = false"
            class="px-4 py-2 bg-[#27AE60] text-white rounded-md hover:bg-[#219653]"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Videos featuring this product 部分 -->
    <div class="mt-10">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Videos featuring this product</h2>
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

      <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
        <!-- Loading Skeleton -->
        <div v-if="videosLoading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        
        <table class="w-full caption-bottom text-sm">
          <thead class="[&_tr]:border-b bg-[#F8F9FA]">
            <tr class="border-b">
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 w-[5%]">
                <input 
                  type="checkbox" 
                  class="rounded border-gray-300"
                  :checked="isCurrentPageAllSelected"
                  @change="selectAll"
                >
              </th>
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Thumbnail</th>
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Creator</th>
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Posted Time</th>
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Views</th>
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Likes</th>
              <th class="py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Description</th>
            </tr>
          </thead>
          <tbody class="[&_tr:last-child]:border-0">
            <tr 
              v-for="video in videos" 
              :key="video.video_id"
              class="border-b hover:bg-secondary-100 h-[90px] cursor-pointer"
              @click="goToVideoDetail(video.video_id)"
            >
              <td class="h-[90px] py-3 px-2 align-middle" @click.stop>
                <input 
                  type="checkbox" 
                  class="rounded border-gray-300"
                  :checked="selectedVideos.some(v => v.video_id === video.video_id)"
                  @change="handleVideoSelect(video, $event)"
                >
              </td>
              <td class="h-[90px] py-3 px-2 align-middle">
                <div class="flex items-center h-full">
                  <img 
                    :src="video.thumbnail_url" 
                    class="w-[63px] h-[112px] rounded-md object-cover"
                    alt="Video thumbnail"
                  >
                </div>
              </td>
              <td class="h-[90px] py-3 px-2 align-middle">
                <div class="flex items-center gap-2">
                  <img 
                    :src="video.creator_profile_url" 
                    class="w-8 h-8 rounded-full"
                    alt="Creator avatar"
                  >
                  <span>{{ video.creators.handle }}</span>
                </div>
              </td>
              <td class="h-[90px] py-3 px-2 align-middle">{{ formatDate(video.posted_date) }}</td>
              <td class="h-[90px] py-3 px-2 align-middle">{{ formatNumber(video.views_count) }}</td>
              <td class="h-[90px] py-3 px-2 align-middle">{{ formatNumber(video.likes_count) }}</td>
              <td class="h-[90px] py-3 px-2 align-middle max-w-md">
                <p class="truncate">{{ video.description }}</p>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Videos Pagination -->
        <div class="mt-4 flex justify-between items-center p-4">
          <!-- 左侧显示数量信息 -->
          <div class="text-sm text-gray-700">
            Showing {{ videosStartIndex }} to {{ Math.min(videosEndIndex, totalVideos) }} of {{ totalVideos }}
          </div>

          <!-- 中间分页按钮 -->
          <div class="flex-1 flex justify-center">
            <div class="flex items-center space-x-1">
              <!-- 上一页按钮 -->
              <button 
                @click="prevVideosPage"
                :disabled="videosCurrentPage === 1"
                class="px-2 py-1 text-gray-600 hover:text-primary-600"
              >
                <span class="text-sm">‹</span>
              </button>

              <!-- 页码按钮 -->
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

              <!-- 下一页按钮 -->
              <button 
                @click="nextVideosPage"
                :disabled="videosCurrentPage === videosTotalPages"
                class="px-2 py-1 text-gray-600 hover:text-primary-600"
              >
                <span class="text-sm">›</span>
              </button>
            </div>
          </div>

          <!-- 右侧占位，保持对称 -->
          <div class="invisible text-sm text-gray-700">
            Showing {{ videosStartIndex }} to {{ Math.min(videosEndIndex, totalVideos) }} of {{ totalVideos }}
          </div>
        </div>
      </div>
    </div>

    <!-- Export Modal -->
    <div v-if="showExportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-[400px]">
        <h3 class="text-lg font-semibold mb-4">Create New List</h3>
        
        <!-- List Name Input -->
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">List Name</label>
            <input 
              v-model="listName"
              type="text"
            placeholder="Enter list name"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
        </div>

        <!-- Selected Creators -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Selected Creators ({{ selectedCreators.length }})
          </label>
          <div class="border border-gray-300 rounded-md p-2 max-h-[100px] overflow-y-auto">
            <div v-for="creator in selectedCreators" :key="creator" class="text-sm text-gray-600">
              {{ creator }}
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex justify-end gap-3">
          <button 
            @click="closeExportModal"
            class="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button 
            @click="handleCreateList"
            class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Create List
          </button>
        </div>
      </div>
    </div>

    <!-- Demographics Section -->
    <div class="mt-10">
      <!-- Creator Demographics -->
      <div class="bg-[#F8F9FA] rounded-lg border border-secondary-100 p-6 mb-8">
        <h2 class="text-xl font-semibold mb-6">Creator Demographics</h2>
        
        <!-- Loading State -->
        <div v-if="analyticsLoading" class="min-h-[300px] flex items-center justify-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        
        <!-- Error State -->
        <div v-else-if="analyticsError" class="min-h-[300px] flex flex-col items-center justify-center">
          <p class="text-red-500 mb-4">{{ analyticsError }}</p>
          <button 
            @click="retryAnalytics"
            class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Retry
          </button>
        </div>
        
        <!-- Content -->
        <div v-else>
          <CreatorDemographics 
            :gender-data="creatorDemographics.gender"
            :language-data="creatorDemographics.language"
          />
        </div>
      </div>

      <!-- Audience Demographics -->
      <div class="bg-[#F8F9FA] rounded-lg border border-secondary-100 p-6">
        <h2 class="text-xl font-semibold mb-6">Audience Demographics</h2>
        
        <!-- Loading State -->
        <div v-if="analyticsLoading" class="min-h-[300px] flex items-center justify-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        
        <!-- Error State -->
        <div v-else-if="analyticsError" class="min-h-[300px] flex flex-col items-center justify-center">
          <p class="text-red-500 mb-4">{{ analyticsError }}</p>
          <button 
            @click="retryAnalytics"
            class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Retry
          </button>
        </div>
        
        <!-- Content -->
        <div v-else>
          <AudienceDemographics 
            :gender-data="audienceDemographics.gender"
            :age-data="audienceDemographics.age"
            :locations-data="audienceDemographics.locations"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CreatorDemographics from '@/components/CreatorDemographics.vue'
import AudienceDemographics from '@/components/AudienceDemographics.vue'

export default {
  name: 'ProductDetail',
  components: {
    CreatorDemographics,
    AudienceDemographics
  },
  data() {
    return {
      product: null,
      videoFormats: [],
      showFormatModal: false,
      selectedFormat: null,
      sellingPoints: [],
      hooks: [],
      videos: [],
      selectedVideos: [],
      selectedCreators: [],
      showExportModal: false,
      isCurrentPageAllSelected: false,
      hasSelectedVideos: false,
      videosLoading: false,
      videosCurrentPage: 1,
      videosPerPage: 5,
      totalVideos: 0,
      listName: '',
      analyticsLoading: false,
      analyticsError: null,
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
        age: {},
        locations: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 5,
        totalPages: 0,
        visiblePages: 5
      }
    }
  },
  computed: {
    hasSelectedVideos() {
      return this.selectedVideos.length > 0;
    },
    isCurrentPageAllSelected() {
      return this.videos.length > 0 && 
             this.videos.every(video => 
               this.selectedVideos.some(v => v.video_id === video.video_id)
             );
    },
    videosTotalPages() {
      return Math.ceil(this.totalVideos / this.videosPerPage);
    },
    videosStartIndex() {
      return (this.videosCurrentPage - 1) * this.videosPerPage + 1;
    },
    videosEndIndex() {
      return this.videosCurrentPage * this.videosPerPage;
    },
    visibleVideoPages() {
      const current = this.videosCurrentPage;
      const total = this.videosTotalPages;
      const visible = 5;
      
      let start = Math.max(current - Math.floor(visible / 2), 1);
      let end = Math.min(start + visible - 1, total);
      
      if (end - start + 1 < visible) {
        start = Math.max(end - visible + 1, 1);
      }
      
      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },
    paginatedSellingPoints() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize;
      const end = start + this.pagination.pageSize;
      return this.sellingPoints.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.sellingPoints.length / this.pagination.pageSize);
    },
    visiblePageNumbers() {
      const current = this.pagination.currentPage;
      const total = this.totalPages;
      const visible = this.pagination.visiblePages;
      
      let start = Math.max(current - Math.floor(visible / 2), 1);
      let end = Math.min(start + visible - 1, total);
      
      if (end - start + 1 < visible) {
        start = Math.max(end - visible + 1, 1);
      }
      
      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },
    videosDisplayedPages() {
      const total = this.videosTotalPages;
      const current = this.videosCurrentPage;
      const pages = [];
      
      if (total <= 7) {
        // 如果总页数小于等于7，显示所有页码
        for (let i = 1; i <= total; i++) pages.push(i);
      } else {
        if (current <= 4) {
          // 当前页靠近开始
          for (let i = 1; i <= 5; i++) pages.push(i);
          pages.push('...');
          pages.push(total);
        } else if (current >= total - 3) {
          // 当前页靠近结束
          pages.push(1);
          pages.push('...');
          for (let i = total - 4; i <= total; i++) pages.push(i);
        } else {
          // 当前页在中间，显示当前页前后各2页
          pages.push(1);
          pages.push('...');
          for (let i = current - 2; i <= current + 2; i++) pages.push(i);
          pages.push('...');
          pages.push(total);
        }
      }
      return pages;
    }
  },
  async created() {
    const productId = this.$route.params.id;
    try {
      const response = await fetch(`http://192.168.0.170:8000/products/${productId}`);
      const data = await response.json();
      
      this.product = {
        id: productId,
        title: data.title,
        seller_name: data.videos?.[0]?.seller_products?.sellers?.name || 'Loading'
      };
      
      // 设置视频格式数据
      this.videoFormats = data.video_formats_analysis_json;
      
      // 处理selling points数据
      this.sellingPoints = data.selling_points_analysis_json.flatMap(point => 
        point.examples.map(example => ({
          selling_point_phrasing: example.selling_point_phrasing,
          creator_profile_url: example.creator_profile_url,
          views_count: example.views_count
        }))
      ).slice(0, 10);

      // 处理hooks数据
      this.hooks = data.hooks_analysis_json.flatMap(hook => 
        hook.examples.map(example => ({
          hook_phrasing: example.hook_phrasing,
          creator_profile_url: example.creator_profile_url,
          views_count: example.views_count
        }))
      ).slice(0, 10); // 同样限制为10条数据

      // 获取视频数据
      await this.fetchVideos(); // 初始加载第一页数据
      await this.fetchAnalytics();
    } catch (error) {
      console.error('Failed to fetch product data:', error);
    }
  },
  methods: {
    openFormatModal(format) {
      this.selectedFormat = format;
      this.showFormatModal = true;
    },
    formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      return num.toString();
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      const diffMonths = Math.floor(diffDays / 30);
      
      if (diffDays < 30) {
        return diffDays === 1 ? '1 day ago' : `${diffDays} days ago`;
      } else if (diffMonths === 1) {
        return 'a month ago';
      } else {
        return `${diffMonths} months ago`;
      }
    },
    handleVideoSelect(video, event) {
      event.stopPropagation();
      
      const index = this.selectedVideos.findIndex(v => v.video_id === video.video_id);
      if (index === -1) {
        this.selectedVideos.push(video);
        if (!this.selectedCreators.includes(video.creators.handle)) {
          this.selectedCreators.push(video.creators.handle);
        }
      } else {
        this.selectedVideos.splice(index, 1);
        const hasOtherVideos = this.selectedVideos.some(v => 
          v.creators.handle === video.creators.handle
        );
        if (!hasOtherVideos) {
          const creatorIndex = this.selectedCreators.indexOf(video.creators.handle);
          if (creatorIndex !== -1) {
            this.selectedCreators.splice(creatorIndex, 1);
          }
        }
      }
    },
    selectAll(event) {
      const isChecked = event.target.checked;
      const currentPageVideoIds = this.videos.map(video => video.video_id);
      
      if (isChecked) {
        // 添加当前页未选中的视频
        this.videos.forEach(video => {
          if (!this.selectedVideos.some(v => v.video_id === video.video_id)) {
            this.selectedVideos.push(video);
            if (!this.selectedCreators.includes(video.creators.handle)) {
              this.selectedCreators.push(video.creators.handle);
            }
          }
        });
      } else {
        // 只移除当前页的选中项
        this.selectedVideos = this.selectedVideos.filter(video => 
          !currentPageVideoIds.includes(video.video_id)
        );
        
        // 重新计算selectedCreators
        const remainingCreators = new Set(
          this.selectedVideos.map(video => video.creators.handle)
        );
        this.selectedCreators = Array.from(remainingCreators);
      }
    },
    clearSelection() {
      this.selectedVideos = [];
      this.selectedCreators = [];
    },
    openExportModal() {
      if (this.selectedCreators.length === 0) {
        alert('Please select at least one video first');
        return;
      }
      this.showExportModal = true;
    },
    goToVideoDetail(videoId) {
      this.$router.push(`/videos/${videoId}`);
    },
    async fetchVideos(page = 1) {
      this.videosLoading = true;
      try {
        const productId = this.$route.params.id;
        const response = await fetch(
          `http://192.168.0.170:8000/products/${productId}/videos?page=${page}&per_page=${this.videosPerPage}`
        );
        const data = await response.json();
        this.videos = data.data;
        this.totalVideos = data.total;
        
        // 设置卖家名称
        if (data.data && data.data[0]?.seller_products?.sellers?.name) {
          this.product.seller_name = data.data[0].seller_products.sellers.name;
        }
      } catch (error) {
        console.error('Failed to fetch videos:', error);
      } finally {
        this.videosLoading = false;
      }
    },
    async changeVideosPage(page) {
      if (page === this.videosCurrentPage) return;
      this.videosCurrentPage = page;
      await this.fetchVideos(page);
    },
    async prevVideosPage() {
      if (this.videosCurrentPage > 1) {
        await this.changeVideosPage(this.videosCurrentPage - 1);
      }
    },
    async nextVideosPage() {
      if (this.videosCurrentPage < this.videosTotalPages) {
        await this.changeVideosPage(this.videosCurrentPage + 1);
      }
    },
    closeExportModal() {
      this.showExportModal = false;
      this.listName = '';
    },
    async handleCreateList() {
      try {
        const creators = this.selectedVideos.map(video => ({
          handle: video.creators.handle,
          profileUrl: `/videos/${video.video_id}`
        }));
        
        const listData = {
          name: this.listName,
          type: 'Filters',
          description: 'Exported from products',
          creators: creators.map(c => c.handle),
          creatorUrls: creators.reduce((acc, c) => {
            acc[c.handle] = c.profileUrl;
            return acc;
          }, {})
        };
        
        await this.$store.dispatch('createList', listData);
        this.closeExportModal();
        this.$router.push('/lists');
      } catch (error) {
        console.error('Failed to create list:', error);
      }
    },
    async fetchAnalytics() {
      this.analyticsLoading = true;
      this.analyticsError = null;
      
      try {
        const productId = this.$route.params.id;
        const response = await fetch(`http://192.168.0.170:8000/products/${productId}/analytics`);
        const { data } = await response.json();
        
        // 处理Creator Demographics数据
        this.creatorDemographics = {
          gender: {
            female: parseFloat(data.creator_genders.female),
            male: parseFloat(data.creator_genders.male)
          },
          language: Object.entries(data.creator_languages).reduce((acc, [key, value]) => {
            acc[key] = parseFloat(value);
            return acc;
          }, {})
        };
        
        // 处理Audience Demographics数据
        this.audienceDemographics = {
          gender: {
            female: parseFloat(data.follower_genders.female),
            male: parseFloat(data.follower_genders.male)
          },
          age: Object.entries(data.follower_ages).reduce((acc, [key, value]) => {
            acc[key] = parseFloat(value);
            return acc;
          }, {}),
          locations: Object.entries(data.follower_locations)
            .map(([name, value]) => ({
              name,
              value: parseFloat(value)
            }))
            .sort((a, b) => b.value - a.value)
            .slice(0, 5)
        };
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
        this.analyticsError = 'Failed to load demographics data. Please try again later.';
      } finally {
        this.analyticsLoading = false;
      }
    },
    async retryAnalytics() {
      await this.fetchAnalytics();
    },
    async fetchSellingPoints() {
      try {
        const productId = this.$route.params.id;
        const response = await fetch(`http://192.168.0.170:8000/products/${productId}/selling_points`);
        const { data } = await response.json();
        this.sellingPoints = data;
        this.pagination.totalPages = Math.ceil(data.length / this.pagination.pageSize);
      } catch (error) {
        console.error('Failed to fetch selling points:', error);
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.pagination.currentPage = page;
      }
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

/* 悬浮提示框的样式 */
.group:hover .group-hover\:visible {
  visibility: visible;
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

.bg-primary-600 {
  background-color: #6366F1;
}

.hover\:bg-primary-700:hover {
  background-color: #4F46E5;
}

.focus\:ring-primary-500:focus {
  --tw-ring-color: #6366F1;
}
</style>