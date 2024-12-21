<template>
  <div class="px-[50px] py-4">
    <!-- 产品卡片部分 -->
    <div class="w-full max-w-2xl m-auto my-8 border rounded-[12px] border-secondary-300 flex">
      <div class="relative group">
        <img 
          :src="product.image" 
          :alt="product.name"
          class="h-full rounded-l-[12px] min-w-[250px]"
        >
      </div>
      <div class="w-full py-4">
        <h2 class="text-[40px] leading-[48px] font-bold text-textPrimary px-4">
          <button class="w-fit !ring-0 text-left line-clamp-4">
            {{ product.name }}
          </button>
        </h2>
        <h3 class="text-[#637381] text-12xl leading-5 tracking-[0.25px] px-4">
          {{ product.brand }}
        </h3>
      </div>
    </div>

    <!-- 视频格式部分 -->
    <h2 class="text-xl font-semibold mt-10 mb-2">Top Video Formats</h2>
    <div class="flex gap-4 flex-wrap">
      <button 
        v-for="format in videoFormats" 
        :key="format"
        class="py-2.5 px-6 text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed border bg-transparent border-secondary-400 hover:bg-secondary-100 disabled:bg-transparent disabled:text-secondary-400 disabled:border-secondary-600 text-primary-500 focus:bg-primary-100 focus:border-primary-500 active:bg-primary-100 h-[46px]"
      >
        {{ format }}
      </button>
    </div>

    <!-- Top Selling Points 部分 -->
    <div class="flex gap-2 flex-col">
      <h2 class="text-xl font-semibold mt-10 mb-2">Top Selling Points</h2>
      <div class="grid grid-rows-5 grid-flow-row lg:grid-flow-col gap-4 p-4 border-2 border-secondary-100 rounded-lg">
        <div 
          v-for="(point, index) in sellingPoints" 
          :key="index"
          class="flex items-center gap-4"
        >
          <span class="w-3">{{ index + 1 }}</span>
          <button 
            @click="goToVideoDetail(point.videoId)"
            class="py-2.5 text-12xl leading-[19.2px] items-center justify-center whitespace-nowrap transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-textPrimary hover:shadow-light-2 hover:bg-secondary-200 disabled:bg-secondary-100 disabled:text-secondary-800 disabled:shadow-none bg-secondary-100 focus:bg-secondary-100 active:bg-secondary-100 h-9 rounded-md px-3 block truncate max-w-[450px]"
          >
            <div class="w-fit !ring-0 text-left truncate max-w-[420px]">
              {{ point.text }}
            </div>
          </button>
          <p class="flex items-center gap-1.5 text-neutral-400 text-[12px]">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trending-up text-primary w-4">
              <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
              <polyline points="16 7 22 7 22 13"></polyline>
            </svg>
            <span>{{ point.views }} views | {{ point.time }}</span>
          </p>
        </div>
      </div>
    </div>

    <!-- Top Hooks 部分 -->
    <div class="flex gap-2 flex-col">
      <h2 class="text-xl font-semibold mt-10 mb-2">Top Hooks</h2>
      <div class="p-4 border-2 border-secondary-100 rounded-lg">
        <div class="grid grid-cols-2 gap-x-8 gap-y-4">
          <div 
            v-for="(hook, index) in topHooks" 
            :key="index" 
            @click="goToVideoDetail(hook.videoId)"
            class="bg-secondary-100 rounded-md p-3 cursor-pointer hover:bg-secondary-200"
          >
            <div class="flex items-center gap-2">
              <span class="text-gray-500">{{ index + 1 }}</span>
              <div class="text-sm text-gray-900 flex-1">{{ hook.text }}</div>
            </div>
            <div class="flex items-center gap-1.5 mt-2 text-neutral-400 text-[11px]">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                <polyline points="16 7 22 7 22 13"></polyline>
              </svg>
              <span>{{ hook.views }} views | {{ hook.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 视频列表部分 -->
    <div class="mt-10">
      <div class="flex justify-between">
        <h2 class="text-2xl font-bold text-gray-900">Videos featuring this product</h2>
        <div class="flex items-center gap-4">
          <!-- 添加创建者列表按钮 -->
          <button 
            @click="showCreateListModal = true" 
            class="py-2.5 px-6 text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-white focus:opacity-[0.88] disabled:bg-secondary-200 disabled:text-secondary-1000 bg-primary-500 hover:bg-primary-400 active:bg-primary-600 h-[46px]"
          >
            Add creators to list
          </button>
        </div>
      </div>

      <!-- 视频表格部分 -->
      <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white mt-4">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b">
              <th class="min-h-16 py-3 px-2 text-left align-middle text-[#6C7381] font-bold text-sm">
                <div class="flex items-center">Thumbnail</div>
              </th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-[#6C7381] font-bold text-sm">
                <div class="flex items-center">Creator</div>
              </th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-[#6C7381] font-bold text-sm">
                <div class="flex items-center">Posted Time</div>
              </th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-[#6C7381] font-bold text-sm">
                <div class="flex items-center">Views</div>
              </th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-[#6C7381] font-bold text-sm">
                <div class="flex items-center">Likes</div>
              </th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-[#6C7381] font-bold text-sm">
                <div class="flex items-center">Description</div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="video in paginatedVideos" 
              :key="video.id" 
              @click="goToVideoDetail(video.id)"
              class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
            >
              <td class="min-h-16 py-3 px-2">
                <img :src="video.thumbnail" class="w-16 h-16 rounded-md object-cover" :alt="video.description">
              </td>
              <td class="min-h-16 py-3 px-2">
                <div class="flex items-center gap-2">
                  <img :src="video.creatorAvatar" class="w-8 h-8 rounded-full" :alt="video.creator">
                  <span>{{ video.creator }}</span>
                </div>
              </td>
              <td class="min-h-16 py-3 px-2">{{ video.postedTime }}</td>
              <td class="min-h-16 py-3 px-2">{{ video.views }}</td>
              <td class="min-h-16 py-3 px-2">{{ video.likes }}</td>
              <td class="min-h-16 py-3 px-2 max-w-md">
                <div class="truncate">{{ video.description }}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页部分 - 移到表格外面 -->
      <div class="mt-4 flex justify-between items-center">
        <!-- 显示数量信息 -->
        <div class="text-secondary-500 text-sm leading-[19.2px] w-[35%]">
          Showing {{ startIndex }} to {{ Math.min(endIndex, totalVideos) }} of {{ totalVideos }}
        </div>

        <!-- 分页按钮 -->
        <nav role="navigation" aria-label="pagination" class="mx-auto flex w-full justify-center">
          <div class="flex items-center space-x-1">
            <!-- 上一页按钮 -->
            <button 
              @click="prevPage"
              :disabled="currentPage === 1"
              class="px-2 py-1 text-secondary-500 hover:text-primary-600"
            >
              <span class="text-sm">‹</span>
            </button>

            <!-- 页码按钮 -->
            <template v-for="n in displayedPages" :key="n">
              <button 
                v-if="n !== '...'"
                @click="changePage(n)"
                :class="[
                  'px-3 py-1 rounded',
                  currentPage === n ? 'bg-[#6366F1] text-white' : 'text-secondary-500 hover:text-primary-600'
                ]"
              >
                {{ n }}
              </button>
              <span v-else class="px-2 text-secondary-500">...</span>
            </template>

            <!-- 下一页按钮 -->
            <button 
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="px-2 py-1 text-secondary-500 hover:text-primary-600"
            >
              <span class="text-sm">›</span>
            </button>
          </div>
        </nav>

        <!-- 为了保持布局平衡的空div -->
        <div class="w-[35%]"></div>
      </div>
    </div>

    <!-- 人口统计部分 -->
    <div class="container mx-auto mt-8">
      <!-- Creator Demographics -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold mb-8">Creator Demographics</h2>
        <div class="flex flex-wrap justify-center gap-20">
          <div class="chart-container">
            <h3 class="text-lg mb-4 text-center">Gender</h3>
            <v-chart class="chart" :option="creatorGenderOption" />
          </div>
          <div class="chart-container">
            <h3 class="text-lg mb-4 text-center">Language</h3>
            <v-chart class="chart" :option="creatorLanguageOption" />
          </div>
        </div>
      </div>

      <!-- Audience Demographics -->
      <div class="mb-32">
        <h2 class="text-2xl font-bold mb-8">Audience Demographics</h2>
        <div class="flex flex-wrap justify-center gap-20">
          <div class="chart-container">
            <h3 class="text-lg mb-4 text-center">Gender</h3>
            <v-chart class="chart" :option="audienceGenderOption" />
          </div>
          <div class="chart-container">
            <h3 class="text-lg mb-4 text-center">Age</h3>
            <v-chart class="chart" :option="audienceAgeOption" />
          </div>
          <div class="chart-container">
            <h3 class="text-lg mb-4 text-center">Top 5 Locations</h3>
            <v-chart class="chart-wide" :option="locationOption" />
          </div>
        </div>
      </div>
    </div>

    <!-- 添加创建列表模态框 -->
    <div v-if="showCreateListModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-[500px]">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Create a new List</h3>
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
  </div>
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer,
  PieChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent
])

export default {
  name: 'ProductDetail',
  components: {
    VChart
  },
  data() {
    return {
      videoFormats: [
        'Transformation Showcase',
        'Problem/Solution Spotlight',
        'Humorous/Relatable Situations',
        'FOMO & Limited-Time Offers',
        'Social Proof Drives Trust'
      ],
      sellingPoints: [
        {
          videoId: 1,
          text: '"That\'s a sign of a healthy digestive system and gut."',
          views: '648K',
          time: 'a month ago'
        },
        {
          videoId: 2,
          text: '"By the end of the night, these meals will be deleted from my system."',
          views: '45K',
          time: '13 days ago'
        },
        {
          videoId: 3,
          text: '"This cleanse has helped so many people get their gut health back on track!"',
          views: '372K',
          time: '15 days ago'
        },
        {
          videoId: 4,
          text: '"The results speak for themselves - over 2 million units sold and counting!"',
          views: '245K',
          time: '20 days ago'
        },
        {
          videoId: 5,
          text: '"Natural ingredients, proven results, and thousands of happy customers."',
          views: '156K',
          time: '25 days ago'
        },
        {
          videoId: 6,
          text: '"Join the thousands who have transformed their gut health with this cleanse."',
          views: '128K',
          time: '28 days ago'
        },
        {
          videoId: 7,
          text: '"Clinical studies show improved digestion in just 15 days!"',
          views: '98K',
          time: 'a month ago'
        },
        {
          videoId: 8,
          text: '"Safe, effective, and backed by science - that\'s why it\'s #1 in the market."',
          views: '86K',
          time: 'a month ago'
        }
      ],
      product: null,
      topHooks: [
        {
          videoId: 7,
          text: '"Why are you only pooping one time a day?"',
          views: '648K',
          time: 'a month ago'
        },
        {
          videoId: 8,
          text: '"Why is it 2.3 million sold?"',
          views: '372K',
          time: '17 days ago'
        },
        {
          videoId: 9,
          text: '"You\'re not ugly, you just keep eating gut clean step required."',
          views: '648K',
          time: 'a month ago'
        },
        {
          videoId: 10,
          text: '"Getting rid of that chub for less than a Starbucks drink is insane work."',
          views: '6.7K',
          time: '18 days ago'
        },
        {
          videoId: 11,
          text: '"This is me just three months ago before I started taking the 15-day gut cleanse."',
          views: '53K',
          time: 'a month ago'
        },
        {
          videoId: 12,
          text: '"The significant weight difference following the cleanse is immediately revealed and is striking."',
          views: '14K',
          time: 'a month ago'
        }
      ],
      productVideos: [],
      showCreateListModal: false,
      listName: '',
      itemsPerPage: 10,
      currentPage: 1
    }
  },
  created() {
    // 获取路由参数中的产品ID
    const productId = this.$route.params.id
    // 这里应该从API获取产品详情
    // 暂模拟数据
    this.product = {
      id: productId,
      name: '15 Day Cleanse - Gut and Colon Support | Caffeine Free | Advanced Formula with Senna, Cascara Sagrada, & Psyllium Husk | Non-GMO | 30 capsules',
      brand: 'Milamiamor',
      image: 'https://picsum.photos/200/200?random=1'
    }

    // 初始化视频数据
    this.productVideos = [
      {
        id: 13,
        thumbnail: 'https://picsum.photos/200/200?random=1',
        creator: 'healthylifestyle',
        creatorAvatar: 'https://picsum.photos/50/50?random=1',
        postedTime: '4 months ago',
        views: '3.9M',
        likes: '2.7M',
        description: 'Im so glad they put me on to this cleanse i was...',
        profileUrl: '/videos/13'
      },
      {
        id: 14,
        thumbnail: 'https://picsum.photos/200/200?random=2',
        creator: 'wellnessjourney',
        creatorAvatar: 'https://picsum.photos/50/50?random=2',
        postedTime: 'a month ago',
        views: '1.1M',
        likes: '4.5M',
        description: 'This skincare routine saved my oily, acne prone...',
        profileUrl: '/videos/14'
      },
      {
        id: 15,
        thumbnail: 'https://picsum.photos/200/200?random=3',
        creator: 'fitnessguru',
        creatorAvatar: 'https://picsum.photos/50/50?random=3',
        postedTime: 'a year ago',
        views: '461.3K',
        likes: '2.2M',
        description: 'Im so glad they put me on to this cleanse i was...',
        profileUrl: '/videos/15'
      },
      {
        id: 16,
        thumbnail: 'https://picsum.photos/200/200?random=4',
        creator: 'healthcoach',
        creatorAvatar: 'https://picsum.photos/50/50?random=4',
        postedTime: '4 months ago',
        views: '974.8K',
        likes: '2.9M',
        description: 'This skincare routine saved my oily, acne prone...',
        profileUrl: '/videos/16'
      }
    ]
  },
  computed: {
    creatorGenderOption() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {d}%'
        },
        legend: {
          orient: 'horizontal',
          bottom: -5,
          left: 'center',
          itemWidth: 12,
          itemHeight: 12,
          icon: 'circle',
          textStyle: {
            fontSize: 12,
            padding: [0, 4, 0, 4]
          }
        },
        color: ['#FF9F9F', '#7CC5FF'],
        series: [{
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '40%'],
          avoidLabelOverlap: false,
          label: {
            show: false
          },
          data: [
            { value: 65, name: 'Female' },
            { value: 35, name: 'Male' }
          ]
        }]
      }
    },

    creatorLanguageOption() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {d}%'
        },
        legend: {
          orient: 'horizontal',
          bottom: -5,
          left: 'center',
          itemWidth: 12,
          itemHeight: 12,
          icon: 'circle',
          textStyle: {
            fontSize: 12,
            padding: [0, 4, 0, 4]
          }
        },
        color: [
          '#FF9F9F',
          '#7CC5FF',
          '#FFD88D',
          '#98E4D0',
          '#C5A3FF',
          '#FFB7A0',
          '#B4B4B4'
        ],
        series: [{
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '40%'],
          avoidLabelOverlap: false,
          label: {
            show: false
          },
          data: [
            { value: 45, name: 'English' },
            { value: 25, name: 'Spanish' },
            { value: 10, name: 'Other' },
            { value: 8, name: 'Other' },
            { value: 5, name: 'Other' },
            { value: 4, name: 'French' },
            { value: 3, name: 'Other' }
          ]
        }]
      }
    },

    // Audience Demographics 部分
    audienceGenderOption() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {d}%'
        },
        legend: {
          orient: 'horizontal',
          bottom: -5,
          left: 'center',
          itemWidth: 12,
          itemHeight: 12,
          icon: 'circle',
          textStyle: {
            fontSize: 12,
            padding: [0, 4, 0, 4]
          }
        },
        color: ['#FF9F9F', '#7CC5FF'],
        series: [{
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '40%'],
          avoidLabelOverlap: false,
          label: {
            show: false
          },
          data: [
            { value: 60, name: 'Female' },
            { value: 40, name: 'Male' }
          ]
        }]
      }
    },

    audienceAgeOption() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {d}%'
        },
        legend: {
          orient: 'horizontal',
          bottom: -5,
          left: 'center',
          itemWidth: 12,
          itemHeight: 12,
          icon: 'circle',
          textStyle: {
            fontSize: 12,
            padding: [0, 4, 0, 4]
          }
        },
        color: [
          '#FF9F9F',
          '#7CC5FF',
          '#FFD88D',
          '#C5A3FF',
          '#98E4D0'
        ],
        series: [{
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '40%'],
          avoidLabelOverlap: false,
          label: {
            show: false
          },
          data: [
            { value: 25, name: '55+' },
            { value: 20, name: '18-24' },
            { value: 25, name: '25-34' },
            { value: 15, name: '35-44' },
            { value: 15, name: '45-54' }
          ]
        }]
      }
    },

    locationOption() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '15%',
          bottom: '3%',
          top: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false }
        },
        yAxis: {
          type: 'category',
          data: ['Georgia', 'New York', 'Florida', 'California', 'Texas'],
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: {
            fontSize: 12,
            margin: 20,
            color: '#666'
          }
        },
        series: [{
          type: 'bar',
          data: [
            { value: 5, itemStyle: { color: '#C5A3FF' } },
            { value: 12, itemStyle: { color: '#98E4D0' } },
            { value: 20, itemStyle: { color: '#FFD88D' } },
            { value: 28, itemStyle: { color: '#7CC5FF' } },
            { value: 30, itemStyle: { color: '#FF9F9F' } }
          ],
          label: {
            show: true,
            position: 'right',
            formatter: '{c}%',
            fontSize: 12,
            color: '#666'
          },
          barWidth: '40%'
        }]
      }
    },

    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      const delta = 1; // 当前页码左右显示的页码数
    
      let pages = [];
      const left = current - delta;
      const right = current + delta;
    
      // 总页数小于等于5时，显示所有页码
      if (total <= 5) {
        for (let i = 1; i <= total; i++) {
          pages.push(i);
        }
        return pages;
      }
    
      // 总页数大于5时，显示部分页码和省略号
      for (let i = 1; i <= total; i++) {
        if (
          i === 1 || // 第一页
          i === total || // 最后一页
          (i >= left && i <= right) || // 当前页码附近
          (i <= 2 && current <= 3) || // 靠近开始
          (i >= total - 1 && current >= total - 2) // 靠近结束
        ) {
          pages.push(i);
        } else if (pages[pages.length - 1] !== '...') {
          pages.push('...');
        }
      }
      return pages;
    },

    paginatedVideos() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.productVideos.slice(start, end);
    },

    totalPages() {
      return Math.ceil(this.productVideos.length / this.itemsPerPage);
    },

    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(this.currentPage * this.itemsPerPage, this.totalVideos);
    },

    totalVideos() {
      return this.productVideos.length;
    }
  },
  methods: {
    goToVideoDetail(videoId) {
      this.$router.push(`/videos/${videoId}`)
    },
    async handleCreateList() {
      try {
        // 从视频列表中提取创建者信息
        const creators = this.productVideos.map(video => ({
          handle: video.creator,
          profileUrl: `https://www.tiktok.com/@${video.creator}`,
          avatar: video.creatorAvatar || '',
          bio: video.description || ''
        }));
        
        const listData = {
          name: this.listName,
          type: 'Product List',
          description: 'Created from product page',
          creators: creators.map(c => c.handle) // 只传递 handle
        };
        
        await this.$store.dispatch('createList', listData);
        this.showCreateListModal = false;
        this.listName = '';
        this.$router.push('/lists');
      } catch (error) {
        console.error('Failed to create list:', error);
        alert('Failed to create list. Please try again.');
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  }
}
</script>

<style scoped>
.chart {
  width: 200px;
  height: 240px;
  margin-bottom: 30px;
}
.chart-wide {
  width: 300px;
  height: 240px;
}

.chart-container {
  margin: 0 40px;
  margin-bottom: 40px;
}

.text-primary {
  color: #6366f1;
}

.cursor-pointer {
  cursor: pointer;
}
</style>