<template>
  <div class="px-[50px] py-4">
    <!-- 返回按钮 -->
    <div class="at-btnholder mb-4">
      <button 
        class="text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed border bg-transparent border-secondary-400 hover:bg-secondary-100 disabled:bg-transparent disabled:text-secondary-400 disabled:border-secondary-600 text-primary-500 focus:bg-primary-100 focus:border-primary-500 active:bg-primary-100 p-2 mr-2 h-auto"
        @click="$router.go(-1)"
      >
        Back
      </button>
    </div>

    <div class="flex gap-x-[60px]">
      <!-- 左侧视频信息 -->
      <div class="flex flex-col md:flex-row gap-3">
        <div class="w-full max-w-2xl m-auto my-8 rounded-[12px] border-secondary-300 flex h-auto flex-col border-0 mt-0">
          <!-- 视频缩略图 -->
          <div class="relative group">
            <div class="absolute w-full h-full flex items-center justify-center bg-secondary-100/40 opacity-0 transition-all duration-300 ease-curve group-hover:opacity-100">
              <a 
                target="_blank" 
                class="flex items-center justify-center p-4 rounded-full bg-black/60 !ring-0"
                :href="`https://tiktok.com/@${video.creator}/video/${video.id}`"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-play text-white">
                  <polygon points="6 3 20 12 6 21 6 3"></polygon>
                </svg>
              </a>
            </div>
            <img 
              :src="video.thumbnail" 
              :alt="video.description"
              class="h-full rounded-l-[12px] w-full min-w-[320px] aspect-[9/16] rounded-r-[12px]"
            >
          </div>

          <!-- 视频详情 -->
          <div class="w-full py-4">
            <div class="w-full h-full flex flex-col justify-center">
              <div class="detail flex flex-col sm:flex-row justify-between">
                <div class="flex flex-col sm:w-1/2">
                  <h2 class="font-semibold text-textPrimary text-lg mb-[5px]">Creator</h2>
                  <h2 class="font-semibold text-textPrimary text-lg mb-[5px]">Posted Time</h2>
                  <h2 class="font-semibold text-textPrimary text-lg mb-[5px]">Views</h2>
                  <h2 class="font-semibold text-textPrimary text-lg mb-[5px]">Likes</h2>
                  <h2 class="font-semibold text-textPrimary text-lg mb-[5px]">Product</h2>
                  <h2 class="font-semibold text-textPrimary text-lg">Brand</h2>
                </div>
                <div class="flex flex-col sm:w-1/2 text-left sm:text-right">
                  <p class="text-secondary-800 text-lg mb-[5px]">{{ video.creator }}</p>
                  <p class="text-secondary-800 text-lg mb-[5px]">{{ video.postedTime }}</p>
                  <p class="text-secondary-800 text-lg mb-[5px]">{{ formatNumber(video.views) }}</p>
                  <p class="text-secondary-800 text-lg mb-[5px]">{{ formatNumber(video.likes) }}</p>
                  <div class="max-w-52 mb-[5px]">
                    <p class="text-secondary-800 text-lg truncate">{{ video.product }}</p>
                  </div>
                  <p class="text-secondary-800 text-lg cursor-pointer">{{ video.brand }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧 Content Insights -->
      <div class="flex flex-col">
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

    <!-- Audience Demographics 部分 -->
    <div class="mt-12">
      <h2 class="text-2xl font-bold mb-8 text-gray-900 px-2">Audience Demographics</h2>
      <div class="grid grid-cols-3 gap-8">
        <!-- Gender Distribution -->
        <div class="bg-white p-6 rounded-xl border border-secondary-200 shadow-sm hover:shadow-md transition-shadow duration-300">
          <h3 class="text-lg font-semibold mb-6 text-center text-gray-800">Gender Distribution</h3>
          <v-chart class="h-[300px]" :option="genderChartOption" autoresize />
        </div>

        <!-- Age Distribution -->
        <div class="bg-white p-6 rounded-xl border border-secondary-200 shadow-sm hover:shadow-md transition-shadow duration-300">
          <h3 class="text-lg font-semibold mb-6 text-center text-gray-800">Age Distribution</h3>
          <v-chart class="h-[300px]" :option="ageChartOption" autoresize />
        </div>

        <!-- Top Locations -->
        <div class="bg-white p-6 rounded-xl border border-secondary-200 shadow-sm hover:shadow-md transition-shadow duration-300">
          <h3 class="text-lg font-semibold mb-6 text-center text-gray-800">Top 5 Locations</h3>
          <v-chart class="h-[300px]" :option="locationChartOption" autoresize />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts'

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
      
      // 添加图表数据
      demographics: {
        gender: {
          female: 65,
          male: 35
        },
        age: {
          '18-24': 30,
          '25-34': 25,
          '35-44': 20,
          '45-54': 15,
          '55+': 10
        },
        locations: {
          'California': 28,
          'Texas': 26,
          'Florida': 20,
          'New York': 18,
          'Illinois': 8
        }
      }
    }
  },
  computed: {
    // 性别分布图表配置
    genderChartOption() {
      return {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#eee',
          borderWidth: 1,
          padding: [8, 12]
        },
        legend: {
          orient: 'horizontal',
          bottom: '0%',
          icon: 'circle',
          itemWidth: 8,
          itemHeight: 8,
          itemGap: 20,
          textStyle: {
            fontSize: 12,
            color: '#666'
          }
        },
        series: [{
          name: 'Gender',
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '40%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderWidth: 0
          },
          label: {
            show: true,
            position: 'inside',
            formatter: '{c}%',
            fontSize: 16,
            fontWeight: 'bold',
            color: '#333',
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            padding: [4, 8],
            borderRadius: 4
          },
          data: [
            { 
              value: this.demographics.gender.female, 
              name: 'Female',
              itemStyle: { color: '#FF85C0' }
            },
            { 
              value: this.demographics.gender.male, 
              name: 'Male',
              itemStyle: { color: '#5B8FF9' }
            }
          ]
        }]
      }
    },
    
    // 年龄分布图表配置
    ageChartOption() {
      const colors = ['#5B8FF9', '#5AD8A6', '#FFD666', '#FF9F7F', '#8B7CE1']
      return {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#eee',
          borderWidth: 1,
          padding: [8, 12]
        },
        legend: {
          orient: 'horizontal',
          bottom: '0%',
          icon: 'circle',
          itemWidth: 8,
          itemHeight: 8,
          itemGap: 15,
          textStyle: {
            fontSize: 12,
            color: '#666'
          }
        },
        series: [{
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '40%'],
          itemStyle: {
            borderWidth: 0
          },
          label: {
            show: true,
            position: 'inside',
            formatter: '{c}%',
            fontSize: 16,
            fontWeight: 'bold',
            color: '#333',
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            padding: [4, 8],
            borderRadius: 4
          },
          data: Object.entries(this.demographics.age).map(([key, value], index) => ({
            name: key,
            value: value,
            itemStyle: { color: colors[index] }
          }))
        }]
      }
    },
    
    // 地区分布图配置
    locationChartOption() {
      const locationData = Object.entries(this.demographics.locations)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
      
      return {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c}%',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#eee',
          borderWidth: 1,
          padding: [8, 12],
          position: function (point, params, dom, rect, size) {
            // 根据鼠标位置返回 tooltip 的位置
            return [point[0] + 10, point[1]];
          }
        },
        grid: {
          top: '5%',
          left: '15%',    // 减小左边距
          right: '15%',
          bottom: '5%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}%',
            color: '#666',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: '#eee',
              type: 'dashed'
            }
          },
          axisTick: {
            show: false
          },
          axisLine: {
            show: false
          }
        },
        yAxis: {
          type: 'category',
          data: locationData.map(item => item[0]),
          axisLabel: {
            color: '#333',
            fontSize: 13,
            margin: 16,
            width: 60,      // 控制标签宽度
            overflow: 'break'  // 文字过长时换行
          },
          axisTick: {
            show: false
          },
          axisLine: {
            show: false
          }
        },
        series: [{
          type: 'bar',
          barWidth: '60%',
          label: {
            show: true,
            position: 'insideRight', // 改为在柱子内部右侧显示
            formatter: '{c}%',
            fontSize: 14,
            fontWeight: 'bold',
            color: '#fff',  // 改为白色，更容易看清
            offset: [0, 0]  // 调整标签偏移量
          },
          data: locationData.map(item => ({
            value: item[1],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#1890FF' },
                { offset: 1, color: '#36CBCB' }
              ])
            }
          }))
        }]
      }
    }
  },
  methods: {
    formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    },
    async fetchVideoDetails() {
      this.video = JSON.parse(localStorage.getItem('selectedVideo'))
      
      // 模拟获取 insights 和 demographics 数据
      this.insights = {
        keyIdea: "This TikTok video uses a \"day in the life\" format to explain why a male CEO has long nails and to promote his company's nail growth oil.",
        topHooks: [
          "Intriguing Question Hook: \"Huh question why do you have long nails?\"",
          "Unexpected Answer Hook: \"The reason I grew out my natural nails might shock you.\""
        ],
        topSellingPoints: [
          "Problem/Solution Hook: \"If you've been struggling with damaged nails...\"",
          "Viral Success Selling Point: \"...it's been going absolutely viral on TikTok Shop. We just sold over 10,000 units.\""
        ],
        transcript: "Reply to user#1loving5u's question:\n\nHuh question why do you have long nails?\n\nI didn't know that having long nails as a guy would cause so much backlash..."
      }
      
      // 模拟获取人口统计数据
      // 实际项目中这些数据应该从后端获取
      this.demographics = {
        gender: {
          female: 65,
          male: 35
        },
        age: {
          '18-24': 30,
          '25-34': 25,
          '35-44': 20,
          '45-54': 15,
          '55+': 10
        },
        locations: {
          'California': 28,
          'Texas': 26,
          'Florida': 20,
          'New York': 18,
          'Illinois': 8
        }
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
}
</style> 