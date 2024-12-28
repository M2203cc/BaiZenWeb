<template>
  <div class="px-[50px] py-4">
    <!-- 标题部分 -->
    <h2 class="text-[40px] leading-[48px] font-bold text-textPrimary">{{ categoryName }}</h2>

    <!-- 品牌列表部分 -->
    <div class="mt-10">
      <h2 class="text-2xl font-bold text-gray-900">Brands featuring this category</h2>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center min-h-[200px]">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="flex flex-col items-center justify-center min-h-[200px]">
        <p class="text-red-500 mb-4">{{ error }}</p>
        <button 
          @click="fetchBrandsByCategoryId"
          class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-500"
        >
          Retry
        </button>
      </div>

      <!-- 数据展示 -->
      <div v-else class="my-4">
        <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
          <table class="w-full caption-bottom text-sm">
            <thead class="[&_tr]:border-b">
              <tr class="border-b transition-colors hover:bg-white">
                <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
                  <div class="flex items-center text-[#6C7381] font-bold text-sm">Brand</div>
                </th>
                <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
                  <div class="flex items-center text-[#6C7381] font-bold text-sm">Number of products</div>
                </th>
                <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
                  <div class="flex items-center text-[#6C7381] font-bold text-sm">Total sales</div>
                </th>
              </tr>
            </thead>
            <tbody class="[&_tr:last-child]:border-0">
              <tr 
                v-for="brand in brands"
                :key="brand.name"
                class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
                @click="goToBrandDetail(brand)"
              >
                <td class="min-h-16 py-2 px-2 align-middle text-md leading-[19.2px] text-secondary-1000 max-w-64">
                  <div class="flex items-center gap-2">
                    <img 
                      :src="brand.image" 
                      :alt="brand.name"
                      class="rounded-md object-cover w-10 h-10"
                    >
                    <button 
                      class="!ring-0 text-left truncate w-auto" 
                      @click.stop="goToBrandDetail(brand)"
                    >
                      {{ brand.name }}
                    </button>
                  </div>
                </td>
                <td class="min-h-16 py-2 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
                  {{ brand.productCount }}
                </td>
                <td class="min-h-16 py-2 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
                  ${{ brand.totalSales.toLocaleString() }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页部分 -->
        <div class="mt-4 flex justify-between items-center">
          <!-- 显示数量信息 -->
          <div class="text-secondary-500 text-sm leading-[19.2px] w-[35%]">
            Showing {{ startIndex }} to {{ Math.min(endIndex, totalBrands) }} of {{ totalBrands }}
          </div>

          <!-- 分页按钮 -->
          <nav role="navigation" aria-label="pagination" class="mx-auto flex w-full justify-center">
            <div class="flex items-center space-x-1">
              <button 
                @click="prevPage"
                :disabled="currentPage === 1"
                class="px-2 py-1 text-secondary-500 hover:text-primary-600"
              >
                <span class="text-sm">‹</span>
              </button>

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
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      categoryId: '',
      categoryName: '',
      brands: [],
      currentPage: 1,
      itemsPerPage: 10,
      loading: false,
      error: null,
      totalItems: 0
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      return Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
    },
    totalBrands() {
      return this.totalItems;
    },
    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      
      // 如果总页数小于等于7，显示所有页码
      if (total <= 7) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }
      
      let pages = [];
      
      // 当前页小于等于3的情况：显示1-5 ... 最后页
      if (current <= 3) {
        pages = [1, 2, 3, 4, 5, '...', total];
      }
      // 当前页接近末尾的情况：显示1 ... 最后5页
      else if (current >= total - 2) {
        pages = [1, '...', total - 4, total - 3, total - 2, total - 1, total];
      }
      // 当前页在中间的情况：显示1 ... 当前页前后各2页 ... 最后页
      else {
        pages = [
          1,
          '...',
          current - 2,
          current - 1,
          current,
          current + 1,
          current + 2,
          '...',
          total
        ];
      }
      
      return pages;
    }
  },
  methods: {
    async fetchBrandsByCategoryId(page = 1) {
      this.loading = true;
      this.error = null;
      
      try {
        if (!this.categoryId) {
          throw new Error('Category ID is required');
        }
        
        console.log('Fetching brands for category ID:', this.categoryId, 'Page:', page);
        
        const response = await fetch(
          `http://localhost:8000/categories/${this.categoryId}/brands?page=${page}&per_page=${this.itemsPerPage}`
        );
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Brands API response data:', result);
        
        if (result && result.data) {
          this.brands = result.data.map(brand => ({
            id: brand.seller_id,
            name: brand.name,
            productCount: brand.num_products,
            totalSales: brand.total_sales,
            image: brand.brand_url || 'https://picsum.photos/40/40'
          }));
          
          this.totalItems = result.total || 0;
        } else {
          throw new Error('Invalid response format');
        }
      } catch (error) {
        console.error('Error fetching brands:', error);
        this.error = `Failed to load brands data: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    goToBrandDetail(brand) {
      this.$router.push({
        name: 'BrandDetail',
        params: { 
          id: brand.id
        }
      });
    },
    async changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        await this.fetchBrandsByCategoryId(page);
      }
    },
    async prevPage() {
      if (this.currentPage > 1) {
        await this.changePage(this.currentPage - 1);
      }
    },
    async nextPage() {
      if (this.currentPage < this.totalPages) {
        await this.changePage(this.currentPage + 1);
      }
    }
  },
  created() {
    console.log('Route params:', this.$route.params);
    console.log('Route query:', this.$route.query);
    
    this.categoryId = this.id || this.$route.params.id;
    this.categoryName = this.$route.query.name || '';
    
    console.log('Extracted categoryId:', this.categoryId);
    console.log('Extracted categoryName:', this.categoryName);
    
    if (!this.categoryId) {
      console.error('No category ID in route params');
      this.error = 'Invalid category ID';
      return;
    }

    // 确保 categoryId 是数字
    const numericId = parseInt(this.categoryId);
    if (isNaN(numericId)) {
      console.error('Category ID is not a number:', this.categoryId);
      this.error = 'Invalid category ID format';
      return;
    }

    this.categoryId = numericId;
    this.fetchBrandsByCategoryId(1);
  }
}
</script> 