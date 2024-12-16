<template>
  <div class="px-[50px] py-4">
    <!-- Brand Header -->
    <div class="flex flex-col items-center justify-center mb-8">
      <div class="w-[128px] h-[128px] mb-4">
        <img 
          :src="brand.image" 
          :alt="brand.name"
          class="w-full h-full rounded-lg object-cover"
        >
      </div>
      <h1 class="text-2xl font-bold">{{ brand.name }}</h1>
    </div>

    <!-- Products Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold mb-4">Products</h2>
      <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
        <table class="w-full caption-bottom text-sm">
          <thead class="[&_tr]:border-b">
            <tr class="border-b">
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Product</th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Price</th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Sold Count</th>
            </tr>
          </thead>
          <tbody class="[&_tr:last-child]:border-0">
            <tr 
              v-for="product in paginatedProducts" 
              :key="product.id"
              class="border-b transition-colors duration-200 ease-curve hover:bg-secondary-100 cursor-pointer"
              @click="goToProductDetail(product.id)"
            >
              <td class="min-h-16 py-3 px-2 align-middle">
                <div class="flex items-center gap-3">
                  <img 
                    :src="product.image" 
                    :alt="product.name"
                    class="w-10 h-10 rounded-md object-cover"
                  >
                  <span>{{ product.name }}</span>
                </div>
              </td>
              <td class="min-h-16 py-3 px-2 align-middle">${{ product.price }}</td>
              <td class="min-h-16 py-3 px-2 align-middle">{{ product.soldCount }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Products Pagination -->
        <div class="mt-4 flex justify-between items-center">
          <div class="text-secondary-500 text-sm leading-[19.2px] w-[35%]">
            Showing {{ productsStartIndex }} to {{ Math.min(productsEndIndex, totalProducts) }} of {{ totalProducts }}
          </div>

          <nav role="navigation" aria-label="pagination" class="mx-auto flex w-full justify-center">
            <div class="flex items-center space-x-1">
              <button 
                @click="prevProductsPage"
                :disabled="productsCurrentPage === 1"
                class="px-2 py-1 text-secondary-500 hover:text-primary-600"
              >
                <span class="text-sm">‹</span>
              </button>

              <template v-for="n in productsDisplayedPages" :key="n">
                <button 
                  v-if="n !== '...'"
                  @click="changeProductsPage(n)"
                  :class="[
                    'px-3 py-1 rounded',
                    productsCurrentPage === n ? 'bg-[#6366F1] text-white' : 'text-secondary-500 hover:text-primary-600'
                  ]"
                >
                  {{ n }}
                </button>
                <span v-else class="px-2 text-secondary-500">...</span>
              </template>

              <button 
                @click="nextProductsPage"
                :disabled="productsCurrentPage === productsTotalPages"
                class="px-2 py-1 text-secondary-500 hover:text-primary-600"
              >
                <span class="text-sm">›</span>
              </button>
            </div>
          </nav>

          <div class="w-[35%]"></div>
        </div>
      </div>
    </div>

    <!-- Videos Section -->
    <div>
      <div class="flex justify-between">
        <h2 class="text-2xl font-bold text-gray-900">Videos featuring this product</h2>
        <div class="flex items-center gap-4">
          <button 
            @click="showCreateListModal = true" 
            class="py-2.5 px-6 text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-white focus:opacity-[0.88] disabled:bg-secondary-200 disabled:text-secondary-1000 bg-primary-500 hover:bg-primary-400 active:bg-primary-600 h-[46px]"
          >
            Add creators to list
          </button>
        </div>
      </div>
      <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white mt-4">
        <table class="w-full caption-bottom text-sm">
          <thead class="[&_tr]:border-b">
            <tr class="border-b">
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Video</th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Creator</th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Posted Time</th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Views</th>
              <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">Likes</th>
            </tr>
          </thead>
          <tbody class="[&_tr:last-child]:border-0">
            <tr 
              v-for="video in paginatedVideos" 
              :key="video.id"
              class="border-b transition-colors duration-200 ease-curve hover:bg-secondary-100 cursor-pointer"
              @click="goToVideoDetail(video.id)"
            >
              <td class="min-h-16 py-3 px-2 align-middle">
                <div class="flex items-center gap-3">
                  <img 
                    :src="video.thumbnail" 
                    :alt="video.title"
                    class="w-20 h-12 rounded-md object-cover"
                  >
                  <span>{{ video.title }}</span>
                </div>
              </td>
              <td class="min-h-16 py-3 px-2 align-middle">
                <div class="flex items-center gap-2">
                  <img 
                    :src="video.creatorAvatar" 
                    :alt="video.creator"
                    class="w-8 h-8 rounded-full object-cover"
                  >
                  <span>{{ video.creator }}</span>
                </div>
              </td>
              <td class="min-h-16 py-3 px-2 align-middle">{{ video.postedTime }}</td>
              <td class="min-h-16 py-3 px-2 align-middle">{{ formatNumber(video.views) }}</td>
              <td class="min-h-16 py-3 px-2 align-middle">{{ formatNumber(video.likes) }}</td>
            </tr>
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
    </div>

    <!-- 添加创建列表模态框 -->
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
  </div>
</template>

<script>
export default {
  name: 'BrandDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      itemsPerPage: 10,
      productsCurrentPage: 1,
      videosCurrentPage: 1,
      brand: null,
      products: [],
      videos: [],
      showCreateListModal: false,
      listName: ''
    }
  },
  created() {
    this.fetchBrandData()
  },
  computed: {
    // Products pagination
    paginatedProducts() {
      const start = (this.productsCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.products.slice(start, end);
    },
    totalProducts() {
      return this.products.length;
    },
    productsTotalPages() {
      return Math.ceil(this.totalProducts / this.itemsPerPage);
    },
    productsStartIndex() {
      return (this.productsCurrentPage - 1) * this.itemsPerPage + 1;
    },
    productsEndIndex() {
      return Math.min(this.productsStartIndex + this.itemsPerPage - 1, this.totalProducts);
    },
    productsDisplayedPages() {
      const total = this.productsTotalPages;
      const current = this.productsCurrentPage;
      const delta = 1;

      let pages = [];
      const left = current - delta;
      const right = current + delta;

      if (total <= 5) {
        for (let i = 1; i <= total; i++) {
          pages.push(i);
        }
        return pages;
      }

      for (let i = 1; i <= total; i++) {
        if (
          i === 1 ||
          i === total ||
          (i >= left && i <= right) ||
          (i <= 2 && current <= 3) ||
          (i >= total - 1 && current >= total - 2)
        ) {
          pages.push(i);
        } else if (pages[pages.length - 1] !== '...') {
          pages.push('...');
        }
      }
      return pages;
    },

    // Videos pagination
    paginatedVideos() {
      const start = (this.videosCurrentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.videos.slice(start, end);
    },
    totalVideos() {
      return this.videos.length;
    },
    videosTotalPages() {
      return Math.ceil(this.totalVideos / this.itemsPerPage);
    },
    videosStartIndex() {
      return (this.videosCurrentPage - 1) * this.itemsPerPage + 1;
    },
    videosEndIndex() {
      return Math.min(this.videosStartIndex + this.itemsPerPage - 1, this.totalVideos);
    },
    videosDisplayedPages() {
      return this.getDisplayedPages(this.videosCurrentPage, this.videosTotalPages);
    }
  },
  methods: {
    formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      return num.toString();
    },
    getDisplayedPages(currentPage, totalPages) {
      let pages = [];
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
      return pages;
    },
    // Products pagination methods
    changeProductsPage(page) {
      this.productsCurrentPage = page;
    },
    prevProductsPage() {
      if (this.productsCurrentPage > 1) {
        this.productsCurrentPage--;
      }
    },
    nextProductsPage() {
      if (this.productsCurrentPage < this.productsTotalPages) {
        this.productsCurrentPage++;
      }
    },
    // Videos pagination methods
    changeVideosPage(page) {
      this.videosCurrentPage = page;
    },
    prevVideosPage() {
      if (this.videosCurrentPage > 1) {
        this.videosCurrentPage--;
      }
    },
    nextVideosPage() {
      if (this.videosCurrentPage < this.videosTotalPages) {
        this.videosCurrentPage++;
      }
    },
    fetchBrandData() {
      const brandId = parseInt(this.id)
      
      this.brand = {
        id: brandId,
        name: 'Tarte Cosmetics',
        image: 'https://picsum.photos/128/128'
      }

      this.products = [
        {
          id: 1,
          name: 'tarte best-sellers trending trio - lip plump gloss, mascara & eye pencil set',
          image: 'https://picsum.photos/40/40?random=1',
          price: 39,
          soldCount: 303637
        },
        {
          id: 2,
          name: 'tarte maracuja juicy lip balm - buildable coverage & a glossy balm finish',
          image: 'https://picsum.photos/40/40?random=2',
          price: 26,
          soldCount: 104218
        },
        {
          id: 3,
          name: 'tarte™ shape tape™ concealer',
          image: 'https://picsum.photos/40/40?random=3',
          price: 32,
          soldCount: 102709
        },
        {
          id: 4,
          name: 'tarte tubing mascara black & brown duo for lash makeup',
          image: 'https://picsum.photos/40/40?random=4',
          price: 27,
          soldCount: 91262
        },
        {
          id: 5,
          name: 'tarte mini mini lip plump trio - 3x high shine glosses set',
          image: 'https://picsum.photos/40/40?random=5',
          price: 39,
          soldCount: 73373
        },
        {
          id: 6,
          name: 'tarte viral shimmer glass lip plump & tubing mascara duo',
          image: 'https://picsum.photos/40/40?random=6',
          price: 25,
          soldCount: 71451
        },
        {
          id: 7,
          name: 'tarte maracuja juicy lip plump - glossy plump finish',
          image: 'https://picsum.photos/40/40?random=7',
          price: 26,
          soldCount: 69421
        },
        {
          id: 8,
          name: 'tarte face tape foundation - 12h longwear matte finish',
          image: 'https://picsum.photos/40/40?random=8',
          price: 42,
          soldCount: 58234
        },
        {
          id: 9,
          name: 'tarte amazonian clay 12-hour blush',
          image: 'https://picsum.photos/40/40?random=9',
          price: 29,
          soldCount: 52187
        },
        {
          id: 10,
          name: 'tarte lights camera lashes™ 4-in-1 mascara',
          image: 'https://picsum.photos/40/40?random=10',
          price: 24,
          soldCount: 48965
        },
        {
          id: 11,
          name: 'tarte sugar rush lip butter balm',
          image: 'https://picsum.photos/40/40?random=11',
          price: 18,
          soldCount: 45723
        }
      ]

      this.videos = [
        {
          id: 1,
          thumbnail: 'https://picsum.photos/320/180?random=1',
          title: 'Best Tarte Products Review 2024',
          creator: 'BeautyGuru',
          creatorAvatar: 'https://picsum.photos/32/32?random=1',
          postedTime: '2 days ago',
          views: 150000,
          likes: 12000
        },
        {
          id: 2,
          thumbnail: 'https://picsum.photos/320/180?random=2',
          title: 'Tarte Shape Tape Concealer Review',
          creator: 'MakeupPro',
          creatorAvatar: 'https://picsum.photos/32/32?random=2',
          postedTime: '1 week ago',
          views: 89000,
          likes: 7500
        },
        {
          id: 3,
          thumbnail: 'https://picsum.photos/320/180?random=3',
          title: 'Full Face Using Only Tarte Cosmetics',
          creator: 'BeautyExpert',
          creatorAvatar: 'https://picsum.photos/32/32?random=3',
          postedTime: '2 weeks ago',
          views: 76500,
          likes: 6800
        },
        {
          id: 4,
          thumbnail: 'https://picsum.photos/320/180?random=4',
          title: 'Tarte Maracuja Juicy Lip Collection',
          creator: 'GlamGuru',
          creatorAvatar: 'https://picsum.photos/32/32?random=4',
          postedTime: '3 weeks ago',
          views: 65000,
          likes: 5200
        },
        {
          id: 5,
          thumbnail: 'https://picsum.photos/320/180?random=5',
          title: 'New Tarte Foundation First Impressions',
          creator: 'BeautyReviewer',
          creatorAvatar: 'https://picsum.photos/32/32?random=5',
          postedTime: '1 month ago',
          views: 54000,
          likes: 4300
        },
        {
          id: 6,
          thumbnail: 'https://picsum.photos/320/180?random=6',
          title: 'Tarte Mascara Comparison',
          creator: 'LashLover',
          creatorAvatar: 'https://picsum.photos/32/32?random=6',
          postedTime: '1 month ago',
          views: 48000,
          likes: 3900
        },
        {
          id: 7,
          thumbnail: 'https://picsum.photos/320/180?random=7',
          title: 'Tarte Holiday Collection Unboxing',
          creator: 'MakeupMaven',
          creatorAvatar: 'https://picsum.photos/32/32?random=7',
          postedTime: '2 months ago',
          views: 42000,
          likes: 3500
        },
        {
          id: 8,
          thumbnail: 'https://picsum.photos/320/180?random=8',
          title: 'Testing Viral Tarte Products',
          creator: 'TrendTester',
          creatorAvatar: 'https://picsum.photos/32/32?random=8',
          postedTime: '2 months ago',
          views: 38000,
          likes: 3100
        },
        {
          id: 9,
          thumbnail: 'https://picsum.photos/320/180?random=9',
          title: 'Tarte Blush Collection Review',
          creator: 'BlushBabe',
          creatorAvatar: 'https://picsum.photos/32/32?random=9',
          postedTime: '3 months ago',
          views: 35000,
          likes: 2800
        },
        {
          id: 10,
          thumbnail: 'https://picsum.photos/320/180?random=10',
          title: 'Affordable Tarte Dupes',
          creator: 'BudgetBeauty',
          creatorAvatar: 'https://picsum.photos/32/32?random=10',
          postedTime: '3 months ago',
          views: 32000,
          likes: 2600
        },
        {
          id: 11,
          thumbnail: 'https://picsum.photos/320/180?random=11',
          title: 'Tarte Lip Products Ranking',
          creator: 'LipstickLover',
          creatorAvatar: 'https://picsum.photos/32/32?random=11',
          postedTime: '3 months ago',
          views: 29000,
          likes: 2400
        }
      ]
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
</style> 