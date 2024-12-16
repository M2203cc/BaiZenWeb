<template>
  <div class="px-[50px] py-4">
    <!-- 标题部分 -->
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Videos</h2>
        </div>
      </div>
    </div>

    <!-- 搜索框部分 -->
    <div class="w-1/2 mb-4">
      <div class="flex gap-5">
        <input 
          class="flex min-h-10 rounded-md border border-secondary-300 bg-white px-4 py-2 text-[16px] leading-[19.2px] !ring-0 transition-all ease-curve placeholder:text-[#A0AEC0] focus:border-secondary-300 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 w-full" 
          placeholder="Search videos" 
          type="text"
          v-model="searchQuery"
        >
        <button 
          class="text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-white focus:opacity-[0.88] disabled:bg-secondary-200 disabled:text-secondary-1000 bg-primary-500 hover:bg-primary-400 active:bg-primary-600 h-[42px] px-4"
          @click="searchVideos"
        >
          Search
        </button>
      </div>
    </div>

    <!-- 筛选器部分 -->
    <div class="grid grid-cols-3 gap-4">
      <!-- Brand 筛选 -->
      <div class="space-y-2">
        <h4 class="mb-2 text-sm font-bold leading-[16.8px] text-[#6C7381]">Brand</h4>
        <div class="brand-dropdown relative">
          <div 
            class="flex h-[42px] w-full rounded-md border border-secondary-300 bg-white px-4 items-center cursor-pointer"
            @click="toggleBrandDropdown"
          >
            <input 
              v-model="brandSearch"
              class="flex-1 bg-transparent border-none outline-none cursor-pointer"
              placeholder="Filter by brands"
              @focus="showBrandDropdown = true"
              @click.stop
            >
            <!-- 添加清除按钮 -->
            <button 
              v-if="brandSearch"
              class="ml-2 mr-3 text-gray-400 hover:text-gray-600"
              @click.stop="clearBrand"
            >
              ×
            </button>
            <span 
              class="ml-3 transform transition-transform duration-200"
              :class="{ 'rotate-180': showBrandDropdown }"
            >
              ▼
            </span>
          </div>
          <!-- Brand 下拉列表 -->
          <div 
            v-show="showBrandDropdown" 
            class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg max-h-60 overflow-y-auto"
          >
            <div 
              v-for="brand in filteredBrands" 
              :key="brand.name"
              class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
              @click="selectBrand(brand)"
            >
              <div class="flex items-center gap-2">
                <img :src="brand.image" class="w-8 h-8 rounded-full" :alt="brand.name">
                <span>{{ brand.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Product 筛选 -->
      <div class="space-y-2">
        <h4 class="mb-2 text-sm font-bold leading-[16.8px] text-[#6C7381]">Product</h4>
        <div class="product-dropdown relative">
          <div 
            class="flex h-[42px] w-full rounded-md border border-secondary-300 bg-white px-4 items-center cursor-pointer"
            @click="toggleProductDropdown"
          >
            <input 
              v-model="productSearch"
              class="flex-1 bg-transparent border-none outline-none cursor-pointer"
              placeholder="Filter by products"
              @focus="showProductDropdown = true"
              @click.stop
            >
            <!-- 清除按钮 -->
            <button 
              v-if="productSearch"
              class="ml-2 mr-3 text-gray-400 hover:text-gray-600"
              @click.stop="clearProduct"
            >
              ×
            </button>
            <span 
              class="ml-3 transform transition-transform duration-200"
              :class="{ 'rotate-180': showProductDropdown }"
            >
              ▼
            </span>
          </div>
          <!-- Product 下拉列表 -->
          <div 
            v-show="showProductDropdown" 
            class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg max-h-60 overflow-y-auto"
          >
            <div 
              v-for="product in filteredProducts" 
              :key="product.name"
              class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
              @click="selectProduct(product)"
            >
              <div class="flex items-center gap-2">
                <img :src="product.image" class="w-8 h-8 rounded-full" :alt="product.name">
                <span>{{ product.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- View Count 筛选 -->
      <div class="space-y-2">
        <h4 class="mb-2 text-sm font-bold leading-[16.8px] text-[#6C7381]">View Count</h4>
        <div class="view-count-dropdown relative">
          <div 
            class="flex h-[42px] w-full rounded-md border border-secondary-300 bg-white px-4 items-center cursor-pointer"
            @click="toggleViewCountDropdown"
          >
            <div class="flex flex-wrap gap-1 items-center flex-1 py-1">
              <template v-if="selectedViewRanges.length">
                <div 
                  v-for="range in selectedViewRanges" 
                  :key="range"
                  class="flex items-center bg-gray-100 rounded px-2 py-1 text-sm"
                >
                  {{ range }}
                  <button 
                    class="ml-1 text-gray-500 hover:text-gray-700"
                    @click.stop="removeViewRange(range)"
                  >
                    ×
                  </button>
                </div>
              </template>
              <span v-else class="text-[#A0AEC0]">Filter by video views</span>
            </div>
            <!-- 清除按钮 -->
            <button 
              v-if="selectedViewRanges.length"
              class="ml-2 mr-3 text-gray-400 hover:text-gray-600"
              @click.stop="clearViewRanges"
            >
              ×
            </button>
            <span 
              class="ml-3 transform transition-transform duration-200" 
              :class="{ 'rotate-180': isViewCountOpen }"
            >
              ▼
            </span>
          </div>
          
          <!-- 下拉选项 -->
          <div 
            v-show="isViewCountOpen" 
            class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg"
          >
            <div class="py-1">
              <div 
                v-for="range in unselectedRanges" 
                :key="range.value"
                class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
                @click="selectViewRange(range.value)"
              >
                <span class="text-gray-700">{{ range.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add creators to list 按钮 -->
    <div>
      <div class="flex justify-end mt-4">
        <button 
          class="py-2.5 px-6 text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 disabled:cursor-not-allowed text-white focus:opacity-[0.88] disabled:bg-secondary-200 disabled:text-secondary-1000 bg-primary-500 hover:bg-primary-400 active:bg-primary-600 h-[46px]"
          @click="addCreatorsToList"
        >
          Add creators to list
        </button>
      </div>
    </div>

    <!-- 视频列表表格 -->
    <div class="my-4">
      <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
        <table class="w-full caption-bottom text-sm">
          <!-- 表头 -->
          <thead class="[&_tr]:border-b">
            <tr class="border-b transition-colors hover:bg-white">
              <th v-for="header in tableHeaders" 
                  :key="header"
                  class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800"
              >
                <div class="flex items-center">{{ header }}</div>
              </th>
            </tr>
          </thead>
          
          <!-- 表格内容 -->
          <tbody class="[&_tr:last-child]:border-0">
            <tr v-for="video in getCurrentPageVideos" 
                :key="video.id" 
                class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
                @click="viewVideoDetail(video)"
            >
              <td class="min-h-16 py-3 px-2 align-middle">
                <img :src="video.thumbnail" class="w-16 h-16 rounded-md" :alt="video.title">
              </td>
              <td class="min-h-16 py-3 px-2 align-middle">
                <div class="flex items-center gap-2">
                  <img :src="video.creatorAvatar" class="w-10 h-10 rounded-full mr-3" :alt="video.creator">
                  <span>{{ video.creator }}</span>
                </div>
              </td>
              <td>{{ video.postedTime }}</td>
              <td>{{ formatNumber(video.views) }}</td>
              <td>{{ formatNumber(video.likes) }}</td>
              <td>{{ video.description }}</td>
              <td>
                <div class="flex items-center gap-2">
                  <img :src="video.productImage" class="w-10 h-10 rounded-full mr-3" :alt="video.product">
                  <span>{{ video.product }}</span>
                </div>
              </td>
              <td>
                <div class="flex items-center gap-2">
                  <img :src="video.brandImage" class="w-10 h-10 rounded-full mr-3" :alt="video.brand">
                  <span>{{ video.brand }}</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 分页部分 -->
    <div class="mt-4 flex justify-between items-center">
      <!-- 显示结果数量 -->
      <div class="text-sm text-gray-700">
        Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, totalVideos) }} of {{ totalVideos }}
      </div>

      <!-- 分页按钮容器 - 居中 -->
      <div class="flex-1 flex justify-center">
        <div class="flex items-center space-x-1">
          <!-- 上一页按钮 -->
          <button 
            @click="prevPage"
            :disabled="currentPage === 1"
            class="px-2 py-1 text-gray-600 hover:text-primary-600"
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
                currentPage === n ? 'bg-primary-500 text-white' : 'text-gray-600 hover:text-primary-600'
              ]"
            >
              {{ n }}
            </button>
            <span v-else class="px-2">...</span>
          </template>

          <!-- 下一页按钮 -->
          <button 
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-2 py-1 text-gray-600 hover:text-primary-600"
          >
            <span class="text-sm">></span>
          </button>
        </div>
      </div>

      <!-- 空的 div 用于保持布局平衡 -->
      <div class="invisible text-sm text-gray-700">
        Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, totalVideos) }} of {{ totalVideos }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Videos',
  data() {
    return {
      searchQuery: '',
      selectedBrand: null,
      selectedProduct: null,
      selectedViewRanges: [],
      viewRanges: [
        { label: '0-100', value: '0-100' },
        { label: '100-500', value: '100-500' },
        { label: '500-2K', value: '500-2k' },
        { label: '2K+', value: '2k+' }
      ],
      tableHeaders: [
        'Thumbnail',
        'Creator',
        'Posted Time',
        'Views',
        'Likes',
        'Description',
        'Product',
        'Brand'
      ],
      videos: [], // 将从API获取
      isViewCountOpen: false,
      brandSearch: '',
      showBrandDropdown: false,
      productSearch: '',
      showProductDropdown: false,
      filteredBrands: [],
      filteredProducts: [],
      currentPage: 1,
      pageSize: 10,
      allVideos: [], // ���储所有视频数据
      filteredVideos: [], // 只在 data 中定义
    }
  },
  computed: {
    unselectedRanges() {
      return this.viewRanges.filter(range => !this.selectedViewRanges.includes(range.value))
    },
    // 从视频数据中取唯一的品牌列表
    uniqueBrands() {
      if (!this.allVideos.length) return [];
      // 使用 Set 去重，然后转换为所需的格式
      const brandsSet = new Set(this.allVideos.map(video => JSON.stringify({
        name: video.brand,
        image: video.brandImage
      })));
      return Array.from(brandsSet).map(brand => JSON.parse(brand));
    },
    filteredBrands() {
      if (!this.brandSearch) return this.uniqueBrands;
      const search = this.brandSearch.toLowerCase();
      return this.uniqueBrands.filter(brand => 
        brand.name.toLowerCase().includes(search)
      );
    },
    
    uniqueProducts() {
      if (!this.allVideos.length) return [];
      // 使用 Set 去重，然后转换为所需的格式
      const productsSet = new Set(this.allVideos.map(video => JSON.stringify({
        name: video.product,
        image: video.productImage
      })));
      return Array.from(productsSet).map(product => JSON.parse(product));
    },
    
    filteredProducts() {
      if (!this.productSearch) return this.uniqueProducts;
      const search = this.productSearch.toLowerCase();
      return this.uniqueProducts.filter(product => 
        product.name.toLowerCase().includes(search)
      );
    },

    // 计算页数
    totalPages() {
      return Math.ceil(this.filteredVideos.length / this.pageSize);
    },

    // 计算当前页显示的视频
    getCurrentPageVideos() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredVideos.slice(start, end);
    },

    // 计算显示的页码范围
    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      const delta = 1; // 当前页码前后显示的页码数

      // 如果当前页超过了总页数，自动调整到最后一页
      if (current > total && total > 0) {
        this.$nextTick(() => {
          this.currentPage = total;
        });
      }

      let pages = [];
      const left = current - delta;
      const right = current + delta;

      for (let i = 1; i <= total; i++) {
        if (
          i === 1 || // 第一页
          i === total || // 最后一页
          (i >= left && i <= right) // 当前页码附近页码
        ) {
          pages.push(i);
        } else if (pages[pages.length - 1] !== '...') {
          pages.push('...');
        }
      }

      return pages;
    },

    // 计算当前显示的数据范围
    startIndex() {
      return (this.currentPage - 1) * this.pageSize + 1
    },

    endIndex() {
      return Math.min(this.currentPage * this.pageSize, this.totalVideos)
    },

    // 总数据量
    totalVideos() {
      return this.filteredVideos.length;
    },
  },
  methods: {
    searchVideos() {
      this.applyFilters();
    },
    addCreatorsToList() {
      // 实现添加创作到列表的逻辑
      console.log('Adding creators to list')
    },
    formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num
    },
    async fetchData() {
      // 生成随机数据
      const creators = [
        { name: 'brothernailtech', avatar: 'https://picsum.photos/50' },
        { name: 'pcosjourneyic', avatar: 'https://picsum.photos/51' },
        { name: 'bsv_xo', avatar: 'https://picsum.photos/52' },
        { name: 'actualreviewsfr', avatar: 'https://picsum.photos/53' },
        { name: 'tanicha_rose', avatar: 'https://picsum.photos/54' }
      ];

      const descriptions = [
        'Replying to @user#loving5u we appreciate the q...',
        'Im so glad they put me on to this cleanse i was...',
        'He gave it a 10/10 so i do too 🥰🥰���� #fyp',
        'Somehow where gonna get there #fyp #viral #sho...',
        'This skincare routine saved my oily, acne prone...'
      ];

      const products = [
        { name: 'Brother Cosmetics Nail Growth Oil', image: 'https://picsum.photos/60' },
        { name: 'Candida Cleanse - Gut and Colon', image: 'https://picsum.photos/61' },
        { name: 'Chicme Lace Trim Slit Bowknot', image: 'https://picsum.photos/62' },
        { name: 'USB-C Fast ChargingCable, Li...', image: 'https://picsum.photos/63' }
      ];

      const brands = [
        { name: 'Brother Cosmetics', image: 'https://picsum.photos/70' },
        { name: 'Pure Peak', image: 'https://picsum.photos/71' },
        { name: 'chicme.us', image: 'https://picsum.photos/72' },
        { name: 'KLSMYHOK! shop', image: 'https://picsum.photos/73' }
      ];

      const getRandomItem = (array) => array[Math.floor(Math.random() * array.length)];
      const getRandomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
      const getRandomDate = () => {
        const periods = ['a month ago', '4 months ago', '17 days ago', 'a year ago'];
        return getRandomItem(periods);
      };

      this.allVideos = Array.from({ length: 20 }, (_, index) => {
        const creator = getRandomItem(creators);
        const product = getRandomItem(products);
        const brand = getRandomItem(brands);
        
        // 生成随机视图数
        const views = getRandomNumber(1000, 5000000); // 生成 1K 到 5M 之间的数字
        
        return {
          id: index + 1,
          thumbnail: `https://picsum.photos/200/200?random=${index}`,
          creator: creator.name,
          creatorAvatar: creator.avatar,
          postedTime: getRandomDate(),
          views: this.formatNumber(views), // 使用 formatNumber 格式化视图数
          likes: getRandomNumber(10000, 5000000),
          description: getRandomItem(descriptions),
          product: product.name,
          productImage: product.image,
          brand: brand.name,
          brandImage: brand.image
        };
      });
      
      // 初始化 filteredVideos
      this.filteredVideos = [...this.allVideos];
    },
    toggleViewCountDropdown() {
      this.isViewCountOpen = !this.isViewCountOpen
    },
    removeViewRange(range) {
      this.selectedViewRanges = this.selectedViewRanges.filter(r => r !== range)
      this.applyFilters();
    },
    handleClickOutside(event) {
      const brandDropdown = this.$el.querySelector('.brand-dropdown')
      const productDropdown = this.$el.querySelector('.product-dropdown')
      const viewCountDropdown = this.$el.querySelector('.view-count-dropdown')

      if (!event.target.closest('.brand-dropdown')) {
        this.showBrandDropdown = false
      }
      if (!event.target.closest('.product-dropdown')) {
        this.showProductDropdown = false
      }
      if (!event.target.closest('.view-count-dropdown')) {
        this.isViewCountOpen = false
      }
    },
    selectViewRange(value) {
      if (!this.selectedViewRanges.includes(value)) {
        this.selectedViewRanges.push(value);
        this.applyFilters();
      }
      this.isViewCountOpen = false;
    },
    clearViewRanges() {
      this.selectedViewRanges = []
      this.applyFilters();
    },
    selectBrand(brand) {
      this.selectedBrand = brand;
      this.brandSearch = brand.name;
      this.showBrandDropdown = false;
      this.applyFilters();
    },
    selectProduct(product) {
      this.selectedProduct = product;
      this.productSearch = product.name;
      this.showProductDropdown = false;
      this.applyFilters();
    },
    // 切换页码
    changePage(page) {
      const totalPages = this.totalPages;
      if (page >= 1 && page <= totalPages) {
        this.currentPage = page;
      } else if (page > totalPages && totalPages > 0) {
        // 如果目标页码超过总页数，跳转到最后一页
        this.currentPage = totalPages;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    viewVideoDetail(video) {
      // 将选中的视频数据存储到 localStorage
      localStorage.setItem('selectedVideo', JSON.stringify(video))
      // 跳转到详情页
      this.$router.push(`/videos/${video.id}`)
    },
    // 添加清除方法
    clearBrand() {
      this.brandSearch = '';
      this.selectedBrand = null;
      this.applyFilters();
    },
    clearProduct() {
      this.productSearch = '';
      this.selectedProduct = null;
      this.applyFilters();
    },
    toggleBrandDropdown() {
      this.showBrandDropdown = !this.showBrandDropdown;
    },
    toggleProductDropdown() {
      this.showProductDropdown = !this.showProductDropdown;
    },
    parseViewCount(viewStr) {
      // 移除所有逗号
      viewStr = viewStr.replace(/,/g, '');
      
      // 处理 K、M 单位
      if (viewStr.includes('K')) {
        return parseFloat(viewStr) * 1000;
      } else if (viewStr.includes('M')) {
        return parseFloat(viewStr) * 1000000;
      }
      
      return parseFloat(viewStr);
    },
    applyFilters() {
      let result = [...this.allVideos];

      // 搜索关键词筛选
      if (this.searchQuery.trim()) {
        const searchTerm = this.searchQuery.toLowerCase().trim();
        result = result.filter(video => 
          video.description.toLowerCase().includes(searchTerm)
        );
      }

      // Brand 筛选
      if (this.selectedBrand) {
        result = result.filter(video => 
          video.brand === this.selectedBrand.name
        );
      }

      // Product 筛选
      if (this.selectedProduct) {
        result = result.filter(video => 
          video.product === this.selectedProduct.name
        );
      }

      // View Count 筛选
      if (this.selectedViewRanges.length > 0) {
        result = result.filter(video => {
          const viewCount = this.parseViewCount(video.views);
          return this.selectedViewRanges.some(range => {
            switch(range) {
              case '0-100':
                return viewCount < 100;
              case '100-500':
                return viewCount >= 100 && viewCount < 500;
              case '500-2k':
                return viewCount >= 500 && viewCount < 2000;
              case '2k+':
                return viewCount >= 2000;
              default:
                return true;
            }
          });
        });
      }

      this.filteredVideos = result;
      this.currentPage = 1; // 重置页码
    },
  },
  mounted() {
    this.fetchData()
    document.addEventListener('click', this.handleClickOutside)
    this.applyFilters() // 初始应用筛选
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  watch: {
    // 添加监听器，当筛选条件改变时重置页码
    selectedBrand() {
      this.currentPage = 1;
    },
    selectedProduct() {
      this.currentPage = 1;
    },
    selectedViewRanges: {
      handler() {
        this.currentPage = 1;
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.form-checkbox {
  @apply rounded border-gray-300;
}

.form-checkbox:checked {
  @apply bg-primary-500 border-primary-500;
}

/* 确保所有筛选器高度一致 */
.css-13cymwt-control {
  height: 42px;
  display: flex;
  align-items: center;
}

/* 下拉箭头式 */
.transform {
  font-size: 10px;
  color: #6C7381;
}

/* 下拉面板样式 */
.shadow-lg {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* 选中项样式 */
.bg-gray-100 {
  background-color: #f3f4f6;
}

/* 确保下拉面板在其他元素之上 */
.z-50 {
  z-index: 50;
}

/* 选中标签的样式 */
.bg-primary-50 {
  background-color: #e6f7ff;
}

.text-primary-600 {
  color: #1890ff;
}

/* 已选择项的样式 */
.opacity-50 {
  opacity: 0.5;
}

/* 调整下拉内容的样式 */
.css-13cymwt-control {
  min-height: 42px;
  height: auto;
  padding-top: 4px;
  padding-bottom: 4px;
}

/* 标签容器样式 */
.flex-wrap {
  margin: -2px;
}

.flex-wrap > * {
  margin: 2px;
}

.view-count-dropdown .selected-range {
  background-color: #f3f4f6;
  border-radius: 4px;
  padding: 2px 8px;
  margin: 2px;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
}

.view-count-dropdown .remove-btn {
  margin-left: 4px;
  color: #666;
  font-size: 16px;
  line-height: 1;
  padding: 0 2px;
}

.view-count-dropdown .remove-btn:hover {
  color: #333;
}

.view-count-dropdown button.ml-2 {
  margin-right: 12px;  /* 增加清除按钮右侧间距 */
}

.view-count-dropdown span {
  margin-left: 12px;  /* 增加下拉箭头左侧间距 */
}

/* 统一所有下拉框的清除按钮和箭头样式 */
.brand-dropdown button,
.product-dropdown button,
.view-count-dropdown button {
  margin-right: 12px;
}

.brand-dropdown span,
.product-dropdown span,
.view-count-dropdown span {
  margin-left: 12px;
}

/* 修改输入框样式以适应新布局 */
.brand-dropdown input,
.product-dropdown input {
  @apply text-[16px] leading-[19.2px];
  padding: 0;
}
</style> 