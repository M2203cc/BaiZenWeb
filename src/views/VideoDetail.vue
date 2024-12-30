<template>
  <div class="px-[50px] py-4">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex items-center justify-center min-h-screen text-red-600">
      {{ error }}
    </div>

    <!-- Content -->
    <div v-else-if="video">
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

      <!-- Main Content -->
      <div class="flex gap-x-[60px] max-w-[1600px] mx-auto">
        <div class="flex flex-col w-full">
          <!-- 上半部分：视频信息和Content Insights -->
          <div class="flex gap-x-[60px]">
            <!-- 左侧内容区域 -->
            <div class="w-[500px]">
              <!-- 视频缩略图 -->
              <div class="relative group w-[280px] mx-auto">
                <img 
                  :src="video.thumbnail_url" 
                  :alt="video.description"
                  class="w-full aspect-[9/16] rounded-[12px]"
                  @error="handleImageError"
                >
              </div>

              <!-- 视频信息 -->
              <div class="mt-6 space-y-3">
                <!-- Creator -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Creator:</span>
                  <span class="text-gray-900">{{ video.creators?.handle }}</span>
                </div>
                
                <!-- Posted Time -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Posted:</span>
                  <span class="text-gray-900">{{ formatTimeAgo(video.posted_date) }}</span>
                </div>
                
                <!-- Views -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Views:</span>
                  <span class="text-gray-900">{{ formatNumber(video.views_count) }}</span>
                </div>
                
                <!-- Likes -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Likes:</span>
                  <span class="text-gray-900">{{ formatNumber(video.likes_count) }}</span>
                </div>
                
                <!-- Product -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Product:</span>
                  <span class="text-gray-900">{{ video.seller_products?.sellers?.name }}</span>
                </div>
              </div>
            </div>

            <!-- 右侧 Content Insights -->
            <div v-if="hasContentInsights" class="flex-1">
              <h2 class="text-16xl leading-7 -tracking-[0.26px] font-bold text-[#303030] mb-[9px]">
                Content Insights
              </h2>
              <div class="w-full bg-white p-5 rounded-[5px] gap-2.5 border border-[#919EAB]">
                <!-- Key Idea -->
                <div v-if="video.analysis_json?.key_idea">
                  <h2 class="text-xl font-semibold text-gray-900">Key idea</h2>
                  <p class="mt-3 text-gray-700">{{ video.analysis_json.key_idea }}</p>
                </div>

                <!-- Top Hooks -->
                <div v-if="video.analysis_json?.hooks?.length" class="mt-5">
                  <h2 class="text-xl font-semibold mb-2">Top Hooks</h2>
                  <div class="grid grid-flow-row gap-4">
                    <div 
                      v-for="(hook, index) in video.analysis_json.hooks" 
                      :key="index"
                      class="flex items-center gap-4"
                    >
                      <span class="w-3">{{ index + 1 }}</span>
                      <div class="py-2.5 px-3 bg-secondary-100 rounded-md text-sm">
                        {{ hook }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Top Selling Points -->
                <div v-if="video.analysis_json?.selling_points?.length" class="mt-5">
                  <h2 class="text-xl font-semibold mb-2">Top Selling Points</h2>
                  <div class="grid grid-flow-row gap-4">
                    <div 
                      v-for="(point, index) in video.analysis_json.selling_points" 
                      :key="index"
                      class="flex items-center gap-4"
                    >
                      <span class="w-3">{{ index + 1 }}</span>
                      <div class="py-2.5 px-3 bg-secondary-100 rounded-md text-sm">
                        {{ point }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Transcript -->
                <div v-if="video.analysis_json?.transcript" class="mt-5">
                  <h2 class="text-xl font-semibold text-gray-900">Transcript</h2>
                  <p class="mt-3 text-gray-700 whitespace-pre-line">{{ video.analysis_json.transcript }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 下半部分：Audience Demographics -->
          <div class="mt-8">
            <h2 class="text-[20px] leading-7 -tracking-[0.26px] font-bold text-[#303030] mb-[9px]">
              Audience Demographics
            </h2>
            <AudienceDemographics
              v-if="demographics"
              :gender-data="{ 
                male: parseFloat(demographics.gender.male),
                female: parseFloat(demographics.gender.female)
              }"
              :age-data="Object.fromEntries(
                Object.entries(demographics.age).map(([key, value]) => [key, parseFloat(value)])
              )"
              :locations-data="Object.entries(demographics.locations)
                .map(([name, value]) => ({ name, value: parseFloat(value) }))
                .sort((a, b) => b.value - a.value)
                .slice(0, 5)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { videoAPI } from '@/services/videoAPI'
import AudienceDemographics from '@/components/AudienceDemographics.vue'

export default defineComponent({
  name: 'VideoDetail',
  components: {
    AudienceDemographics
  },
  setup() {
    const route = useRoute()
    const video = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const demographics = ref(null)

    // 计算属性
    const hasContentInsights = computed(() => {
      return !!(
        video.value?.analysis_json?.key_idea ||
        video.value?.analysis_json?.hooks?.length ||
        video.value?.analysis_json?.selling_points?.length ||
        video.value?.analysis_json?.transcript
      )
    })

    // 格式化时间的方法
    const formatTimeAgo = (date) => {
      if (!date) return 'Unknown date'
      const now = new Date()
      const postedDate = new Date(date)
      const diffTime = Math.abs(now - postedDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      const months = Math.floor(diffDays / 30)
      if (months > 0) {
        return months === 1 ? 'a month ago' : `${months} months ago`
      }
      return diffDays === 1 ? '1 day ago' : `${diffDays} days ago`
    }

    // 格式化数字的方法
    const formatNumber = (num) => {
      if (!num) return '0'
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }

    // 获取视频详情的方法
    const fetchVideoDetails = async () => {
      try {
        loading.value = true
        error.value = null
        
        const videoId = route.params.id
        if (!videoId) {
          throw new Error('Video ID is required')
        }

        const response = await videoAPI.getVideoDetail(videoId)
        if (response && response.data) {
          video.value = response.data
          await fetchDemographics(videoId)
          // 打印成功获取的数据以便调试
          console.log('Successfully fetched video data:', video.value)
        } else {
          throw new Error('Invalid response format')
        }
      } catch (err) {
        console.error('Error fetching video details:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status
        })
        
        // 根据不同错误类型显示不同的错误信息
        if (err.response?.status === 404) {
          error.value = '视频不存在或已被删除'
        } else if (err.response?.status === 500) {
          error.value = '服务器错误，请稍后重试'
        } else {
          error.value = err.response?.data?.detail || 
                       err.message || 
                       '加载视频详情失败'
        }
      } finally {
        loading.value = false
      }
    }

    // 在组件挂载时获取数据
    onMounted(() => {
      fetchVideoDetails()
    })

    // 获取人口统计数据的方法
    const fetchDemographics = async (videoId) => {
      try {
        const response = await videoAPI.getVideoDemographics(videoId)
        if (response && response.data && response.data.data) {  // 注意这里要访问 response.data.data
          demographics.value = {
            gender: response.data.data.follower_genders,
            age: response.data.data.follower_ages,
            locations: response.data.data.follower_locations
          }
          console.log('Demographics data:', demographics.value)
        }
      } catch (err) {
        console.error('Error fetching demographics:', err)
      }
    }

    return {
      video,
      loading,
      error,
      demographics,
      hasContentInsights,
      formatTimeAgo,
      formatNumber,
      fetchVideoDetails
    }
  }
})
</script> 