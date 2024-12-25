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
      <!-- 返回按钮 -->
      <div class="at-btnholder mb-4">
        <button 
          class="text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed border bg-transparent border-secondary-400 hover:bg-secondary-100 disabled:bg-transparent disabled:text-secondary-400 disabled:border-secondary-600 text-primary-500 focus:bg-primary-100 focus:border-primary-500 active:bg-primary-100 p-2 mr-2 h-auto"
          @click="$router.go(-1)"
        >
          Back
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
                <div class="absolute w-full h-full flex items-center justify-center bg-secondary-100/40 opacity-0 transition-all duration-300 ease-curve group-hover:opacity-100">
                  <a 
                    target="_blank" 
                    class="flex items-center justify-center p-4 rounded-full bg-black/60 !ring-0"
                    :href="`https://tiktok.com/@${video?.creator || ''}/video/${video?.id || ''}`"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-play text-white">
                      <polygon points="6 3 20 12 6 21 6 3"></polygon>
                    </svg>
                  </a>
                </div>
                <img 
                  :src="video.thumbnail" 
                  :alt="video.description"
                  class="w-full aspect-[9/16] rounded-[12px]"
                >
              </div>

              <!-- 视频信息 -->
              <div class="mt-6 space-y-3">
                <!-- Creator -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Creator:</span>
                  <span class="text-gray-900">{{ video.creator }}</span>
                </div>
                
                <!-- Posted Time -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Posted:</span>
                  <span class="text-gray-900">{{ video.postedTime }}</span>
                </div>
                
                <!-- Views -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Views:</span>
                  <span class="text-gray-900">{{ formatNumber(video.views) }}</span>
                </div>
                
                <!-- Likes -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Likes:</span>
                  <span class="text-gray-900">{{ formatNumber(video.likes) }}</span>
                </div>
                
                <!-- Product -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Product:</span>
                  <span class="text-gray-900 text-right flex-1 ml-4 truncate">{{ video.product }}</span>
                </div>
                
                <!-- Brand -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Brand:</span>
                  <span class="text-gray-900">{{ video.brand }}</span>
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
                <div v-if="insights.keyIdea">
                  <h2 class="text-xl font-semibold text-gray-900">Key idea</h2>
                  <p class="mt-3 text-gray-700">{{ insights.keyIdea }}</p>
                </div>

                <!-- Top Hooks -->
                <div v-if="insights.topHooks?.length" class="flex gap-2 flex-col">
                  <h2 class="text-xl font-semibold mb-2 mt-5">Top Hooks</h2>
                  <div class="grid grid-flow-row lg:grid-flow-col gap-4 p-4 border-2 border-secondary-100 rounded-lg grid-cols-1 grid-rows-none !grid-flow-row">
                    <div v-for="(hook, index) in insights.topHooks" :key="index" class="flex items-center gap-4">
                      <span class="w-3">{{ index + 1 }}</span>
                      <button class="py-2.5 text-12xl leading-[19.2px] items-center justify-center whitespace-nowrap transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-textPrimary hover:shadow-light-2 hover:bg-secondary-200 disabled:bg-secondary-100 disabled:text-secondary-800 disabled:shadow-none bg-secondary-100 focus:bg-secondary-100 active:bg-secondary-100 h-9 rounded-md px-3 block truncate max-w-full">
                        {{ hook }}
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Top Selling Points -->
                <div v-if="insights.topSellingPoints?.length" class="flex gap-2 flex-col">
                  <h2 class="text-xl font-semibold mb-2 mt-5">Top Selling Points</h2>
                  <div class="grid grid-flow-row lg:grid-flow-col gap-4 p-4 border-2 border-secondary-100 rounded-lg grid-cols-1 grid-rows-none !grid-flow-row">
                    <div v-for="(point, index) in insights.topSellingPoints" :key="index" class="flex items-center gap-4">
                      <span class="w-3">{{ index + 1 }}</span>
                      <button class="py-2.5 text-12xl leading-[19.2px] items-center justify-center whitespace-nowrap transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-textPrimary hover:shadow-light-2 hover:bg-secondary-200 disabled:bg-secondary-100 disabled:text-secondary-800 disabled:shadow-none bg-secondary-100 focus:bg-secondary-100 active:bg-secondary-100 h-9 rounded-md px-3 block truncate max-w-full">
                        {{ point }}
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Transcript -->
                <div v-if="insights.transcript" class="mt-5">
                  <h2 class="text-xl font-semibold text-gray-900">Transcript</h2>
                  <p class="mt-3 text-gray-700 whitespace-pre-line">{{ insights.transcript }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 下半部分：Audience Demographics -->
          <div class="mt-16">
            <h2 class="text-2xl font-bold mb-8">Audience Demographics</h2>
            <div class="grid grid-cols-3 gap-8">
              <!-- Gender Distribution -->
              <div class="text-center">
                <h3 class="text-lg font-semibold mb-6">Gender</h3>
                <v-chart 
                  class="h-[250px]" 
                  :option="genderChartOption" 
                  :loading="!demographics?.gender"
                  autoresize 
                />
              </div>

              <!-- Age Distribution -->
              <div class="text-center">
                <h3 class="text-lg font-semibold mb-6">Age</h3>
                <v-chart 
                  class="h-[250px]" 
                  :option="ageChartOption" 
                  :loading="!demographics?.age"
                  autoresize 
                />
              </div>

              <!-- Top Locations -->
              <div class="text-center">
                <h3 class="text-lg font-semibold mb-6">Top 5 Locations</h3>
                <v-chart 
                  class="h-[250px]" 
                  :option="locationChartOption" 
                  :loading="!demographics?.locations"
                  autoresize 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { use } from 'echarts/core'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import VChart from 'vue-echarts'
import videoAPI from '../services/videoAPI'

// 注册必要的组件
use([
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer
])

export default defineComponent({
  name: 'VideoDetail',
  components: {
    VChart
  },
  data() {
    return {
      video: null,
      insights: {
        keyIdea: '',
        topHooks: [],
        topSellingPoints: [],
        transcript: ''
      },
      loading: true,
      error: null,
      demographics: null
    }
  },
  computed: {
    // 性别分布图表配置
    genderChartOption() {
      if (!this.demographics?.gender) return {}
      
      const data = [
        { name: 'Female', value: this.demographics.gender.female },
        { name: 'Male', value: this.demographics.gender.male }
      ]
      
      return {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%'
        },
        legend: {
          orient: 'horizontal',
          bottom: '0',
          icon: 'circle',
          textStyle: { color: '#666' }
        },
        series: [{
          type: 'pie',
          radius: ['40%', '60%'],
          center: ['50%', '40%'],
          data: data.map(item => ({
            ...item,
            itemStyle: {
              color: item.name === 'Female' ? '#FF85C0' : '#5B8FF9',
              borderWidth: 0
            }
          })),
          label: { show: false }
        }]
      }
    },
    
    // 年龄分布图表配置
    ageChartOption() {
      if (!this.demographics?.age) return {}
      
      const ageOrder = ['18-24', '25-34', '35-44', '45-54', '55+']
      const colors = ['#5B8FF9', '#FFD666', '#5AD8A6', '#8B7CE1', '#FF9F7F']
      
      const data = ageOrder.map((age, index) => ({
        name: age,
        value: Number(this.demographics.age[age] || 0),
        itemStyle: { 
          color: colors[index],
          borderWidth: 0
        }
      }))
      
      return {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%'
        },
        legend: {
          orient: 'horizontal',
          bottom: '0',
          icon: 'circle',
          textStyle: { color: '#666' }
        },
        series: [{
          type: 'pie',
          radius: ['40%', '60%'],
          center: ['50%', '40%'],
          data: data,
          label: { show: false }
        }]
      }
    },
    
    // 地区分布图表配置
    locationChartOption() {
      if (!this.demographics?.locations) return {}
      
      const locationData = Object.entries(this.demographics.locations)
        .sort((a, b) => Number(b[1]) - Number(a[1]))
        .slice(0, 5)
      
      return {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        grid: {
          top: '5%',
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLabel: { 
            formatter: '{value}%',
            color: '#666'
          },
          splitLine: { show: false },
          axisLine: { show: false }
        },
        yAxis: {
          type: 'category',
          data: locationData.map(([name]) => name),
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: { color: '#666' }
        },
        series: [{
          type: 'bar',
          data: locationData.map(([_, value]) => ({
            value: Number(value),
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#1890FF' },
                { offset: 1, color: '#36CBCB' }
              ]),
              borderWidth: 0
            }
          })),
          barWidth: '60%'
        }]
      }
    },
    hasContentInsights() {
      return !!(this.insights.keyIdea || 
                this.insights.topHooks?.length || 
                this.insights.topSellingPoints?.length)
    }
  },
  methods: {
    formatNumber(num) {
      if (!num) return '0'
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    },
    getTimeAgo(date) {
      if (!date) return 'Unknown date'
      const now = new Date()
      const postedDate = new Date(date)
      const diffTime = Math.abs(now - postedDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      const months = Math.floor(diffDays / 30)
      
      if (months > 0) {
        return months === 1 ? 'a month ago' : `${months} months ago`
      } else {
        return diffDays === 1 ? '1 day ago' : `${diffDays} days ago`
      }
    },
    async fetchVideoDetails() {
      try {
        this.loading = true
        this.error = null
        
        const videoId = this.$route.params.id
        if (!videoId) {
          throw new Error('Video ID is required')
        }

        // 获取视频详情
        const response = await videoAPI.getVideoDetails(videoId)
        
        if (response && response.data) {
          this.video = {
            id: response.data.id || response.data.video_id,
            thumbnail: response.data.thumbnail_url || response.data.cover_image_url,
            creator: response.data.creators?.handle || 'Unknown Creator',
            creatorAvatar: response.data.creator_profile_url,
            views: response.data.views_count || response.data.stats?.play_count || 0,
            likes: response.data.likes_count || response.data.stats?.digg_count || 0,
            description: response.data.description || 'No description',
            postedTime: this.getTimeAgo(response.data.posted_date || response.data.create_time || response.data.created_at),
            product: response.data.seller_products?.title || 'Unknown Product',
            productImage: response.data.seller_product_photo_url,
            brand: response.data.seller_products?.sellers?.name || 'Unknown Brand',
            brandImage: response.data.seller_photo_url,
            follower_genders: response.data.follower_genders || {},
            follower_ages: response.data.follower_ages || {},
            follower_locations: response.data.follower_locations || {}
          }

          // 处理 insights 数据
          if (response.data.analysis_json) {
            this.insights = {
              keyIdea: response.data.analysis_json.key_idea || '',
              topHooks: response.data.analysis_json.hooks || [],
              topSellingPoints: response.data.analysis_json.selling_points || [],
              transcript: response.data.analysis_json.transcript || ''
            }
          }

          // 获取人口统计数据
          try {
            const demographicsResponse = await videoAPI.getVideoDemographics(videoId)
            console.log('Demographics response:', demographicsResponse)
            
            if (demographicsResponse && demographicsResponse.data) {
              this.demographics = {
                gender: {
                  female: Number(demographicsResponse.data.follower_genders?.female || 0),
                  male: Number(demographicsResponse.data.follower_genders?.male || 0)
                },
                age: demographicsResponse.data.follower_ages || {},
                locations: demographicsResponse.data.follower_locations || {}
              }
            }
          } catch (demoError) {
            console.error('Error fetching demographics:', demoError)
            this.demographics = null
          }
        }
      } catch (error) {
        console.error('Error fetching video details:', error)
        this.error = error.message || 'Failed to load video details'
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    this.fetchVideoDetails()
  }
})
</script>

<style scoped>
.v-chart {
  width: 100%;
  height: 100%;
  background-color: transparent;
}
</style> 