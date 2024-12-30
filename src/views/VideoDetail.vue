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
                  <span class="text-gray-900">{{ video.product }}</span>
                </div>
              </div>
            </div>

            <!-- Content Insights 部分 -->
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
                <div v-if="insights.topHooks?.length" class="mt-5">
                  <h2 class="text-xl font-semibold mb-2">Top Hooks</h2>
                  <div class="grid grid-flow-row gap-4">
                    <div v-for="(hook, index) in insights.topHooks" :key="index" class="flex items-center gap-4">
                      <span class="w-3">{{ index + 1 }}</span>
                      <div class="py-2.5 px-3 bg-secondary-100 rounded-md text-sm">
                        {{ hook }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Top Selling Points -->
                <div v-if="insights.topSellingPoints?.length" class="mt-5">
                  <h2 class="text-xl font-semibold mb-2">Top Selling Points</h2>
                  <div class="grid grid-flow-row gap-4">
                    <div v-for="(point, index) in insights.topSellingPoints" :key="index" class="flex items-center gap-4">
                      <span class="w-3">{{ index + 1 }}</span>
                      <div class="py-2.5 px-3 bg-secondary-100 rounded-md text-sm">
                        {{ point }}
                      </div>
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
      if (!this.demographics?.gender) return {};
      
      const data = [
        { name: 'Female', value: this.demographics.gender.female },
        { name: 'Male', value: this.demographics.gender.male }
      ];
      
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
      };
    },
    
    // 年龄分布图表配置
    ageChartOption() {
      if (!this.demographics?.age) return {};
      
      const ageOrder = ['18-24', '25-34', '35-44', '45-54', '55+'];
      const colors = ['#5B8FF9', '#FFD666', '#5AD8A6', '#8B7CE1', '#FF9F7F'];
      
      const data = ageOrder.map((age, index) => ({
        name: age,
        value: Number(this.demographics.age[age] || 0),
        itemStyle: { 
          color: colors[index],
          borderWidth: 0
        }
      }));
      
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
      };
    },
    
    // 地区分布图表配置
    locationChartOption() {
      if (!this.demographics?.locations) return {};
      
      const locationData = Object.entries(this.demographics.locations)
        .sort((a, b) => Number(b[1]) - Number(a[1]))
        .slice(0, 5);
      
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
      };
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
    getTimeAgo(dateString) {
      if (!dateString) return 'Unknown date';
      
      const now = new Date();
      const date = new Date(dateString);
      const diffTime = now - date;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) {
        return '1 day ago';
      } else if (diffDays < 30) {
        return `${diffDays} days ago`;
      } else {
        const months = Math.floor(diffDays / 30);
        if (months === 1) {
          return 'a month ago';
        }
        return `${months} months ago`;
      }
    },
    async fetchVideoDetails() {
      try {
        this.loading = true;
        this.error = null;
        
        const videoId = this.$route.params.id;
        if (!videoId) {
          throw new Error('Video ID is required');
        }

        // 获取视频详情
        const response = await videoAPI.getVideoDetails(videoId);
        
        if (response && response.data) {
          const data = response.data;
          
          this.video = {
            id: data.video_id,
            thumbnail: data.thumbnail_url,
            creator: data.creators?.handle || 'Unknown Creator',
            views: data.views_count || 0,
            likes: data.likes_count || 0,
            postedTime: this.getTimeAgo(data.posted_date),
            product: data.seller_products?.sellers?.name || 'Unknown Product'
          };

          // 只有当 analysis_json 存在且有数据时才设置 insights
          if (data.analysis_json) {
            const hasKeyIdea = !!data.analysis_json.key_idea;
            const hasHooks = Array.isArray(data.analysis_json.hooks) && data.analysis_json.hooks.length > 0;
            const hasSellingPoints = Array.isArray(data.analysis_json.selling_points) && data.analysis_json.selling_points.length > 0;
            const hasTranscript = !!data.analysis_json.transcript;

            // 只添加有数据的字段
            this.insights = {
              ...(hasKeyIdea && { keyIdea: data.analysis_json.key_idea }),
              ...(hasHooks && { topHooks: data.analysis_json.hooks }),
              ...(hasSellingPoints && { topSellingPoints: data.analysis_json.selling_points }),
              ...(hasTranscript && { transcript: data.analysis_json.transcript })
            };
          } else {
            this.insights = {};
          }
        }

        // 获取人口统计数据
        try {
          const demographicsResponse = await videoAPI.getVideoDemographics(videoId);
          if (demographicsResponse && demographicsResponse.data) {
            const demoData = demographicsResponse.data;
            this.demographics = {
              gender: {
                female: Number(demoData.follower_genders?.female || 0),
                male: Number(demoData.follower_genders?.male || 0)
              },
              age: {
                '18-24': Number(demoData.follower_ages?.['18-24'] || 0),
                '25-34': Number(demoData.follower_ages?.['25-34'] || 0),
                '35-44': Number(demoData.follower_ages?.['35-44'] || 0),
                '45-54': Number(demoData.follower_ages?.['45-54'] || 0),
                '55+': Number(demoData.follower_ages?.['55+'] || 0)
              },
              locations: demoData.follower_locations || {}
            };
          }
        } catch (demoError) {
          console.error('Error fetching demographics:', demoError);
          this.demographics = null;
        }
      } catch (error) {
        console.error('Error fetching video details:', error);
        this.error = error.message || 'Failed to load video details';
      } finally {
        this.loading = false;
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