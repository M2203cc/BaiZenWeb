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

    <!-- Format详情模态框 -->
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
  </div>
</template>

<script>
export default {
  name: 'ProductDetail',
  data() {
    return {
      product: null,
      videoFormats: [],
      showFormatModal: false,
      selectedFormat: null,
    }
  },
  async created() {
    const productId = this.$route.params.id;
    try {
      const response = await fetch(`http://192.168.0.170:8000/products/${productId}`);
      const data = await response.json();
      
      this.product = {
        id: productId,
        title: data.title
      };
      
      // 设置视频格式数据
      this.videoFormats = data.video_formats_analysis_json;
    } catch (error) {
      console.error('Failed to fetch product data:', error);
    }
  },
  methods: {
    openFormatModal(format) {
      this.selectedFormat = format;
      this.showFormatModal = true;
    }
  }
}
</script>