<template>
  <div class="px-[50px] py-4">
    <!-- 标题部分 -->
    <h2 class="text-[40px] leading-[48px] font-bold text-textPrimary">{{ categoryName }}</h2>

    <!-- 品牌列表部分 -->
    <div class="mt-10">
      <h2 class="text-2xl font-bold text-gray-900">Brands featuring this category</h2>
      <div class="my-4">
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
                v-for="brand in paginatedBrands" 
                :key="brand.name"
                class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
                @click="goToProductDetail(brand)"
              >
                <td class="min-h-16 py-2 px-2 align-middle text-md leading-[19.2px] text-secondary-1000 max-w-64">
                  <div class="flex items-center gap-2">
                    <img 
                      :src="brand.image" 
                      :alt="brand.name"
                      class="rounded-md object-cover w-10 h-10"
                    >
                    <button class="!ring-0 text-left truncate w-auto" @click.stop="goToProductDetail(brand)">{{ brand.name }}</button>
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
  data() {
    return {
      categoryName: '',
      brands: [],
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    paginatedBrands() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.brands.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.brands.length / this.itemsPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      return Math.min(this.currentPage * this.itemsPerPage, this.totalBrands);
    },
    totalBrands() {
      return this.brands.length;
    },
    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
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
    }
  },
  methods: {
    goToProductDetail(brand) {
      // 假设每个品牌都有一个默认的产品ID，这里使用1作为示例
      // 实际应用中可能需要根据具体业务逻辑来确定产品ID
      this.$router.push(`/products/${brand.id || 1}`);
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
  },
  created() {
    this.categoryName = decodeURIComponent(this.$route.params.name)
    
    // 模拟数据
    this.brands = [
      {
        id: 1,
        name: 'Halara US',
        productCount: 920,
        totalSales: 75297300,
        image: 'https://picsum.photos/40/40?random=1'
      },
      {
        id: 2,
        name: 'O QQ',
        productCount: 84,
        totalSales: 45656000,
        image: 'https://picsum.photos/40/40?random=2'
      },
      {
        name: 'FeelinGirl LLC',
        productCount: 262,
        totalSales: 33027600,
        image: 'https://picsum.photos/40/40?random=3'
      },
      {
        name: 'Cider',
        productCount: 8174,
        totalSales: 24670300,
        image: 'https://picsum.photos/40/40?random=4'
      },
      {
        name: 'NcmRyu',
        productCount: 207,
        totalSales: 24666400,
        image: 'https://picsum.photos/40/40?random=5'
      },
      {
        name: 'YOZY',
        productCount: 4491,
        totalSales: 22133800,
        image: 'https://picsum.photos/40/40?random=6'
      },
      {
        name: 'OQQfitness',
        productCount: 45,
        totalSales: 19720900,
        image: 'https://picsum.photos/40/40?random=7'
      },
      {
        name: 'Comfrt',
        productCount: 36,
        totalSales: 18809100,
        image: 'https://picsum.photos/40/40?random=8'
      },
      {
        name: 'CAKES body',
        productCount: 6,
        totalSales: 16796900,
        image: 'https://picsum.photos/40/40?random=9'
      },
      {
        name: 'Kali Rose Boutique',
        productCount: 1103,
        totalSales: 15846900,
        image: 'https://picsum.photos/40/40?random=10'
      },
      {
        name: 'Fashion Brand 11',
        productCount: 850,
        totalSales: 14500000,
        image: 'https://picsum.photos/40/40?random=11'
      },
      {
        name: 'Style Co. 12',
        productCount: 720,
        totalSales: 13800000,
        image: 'https://picsum.photos/40/40?random=12'
      }
    ]
  }
}
</script> 