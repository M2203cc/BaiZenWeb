<template>
  <div class="px-[50px] py-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Brands</h2>
        </div>
      </div>
    </div>

    <!-- Search and Favorite Bar -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex gap-5">
        <input 
          class="flex min-h-10 rounded-md border border-secondary-300 bg-white px-4 py-3 text-[16px] leading-[19.2px] !ring-0 transition-all ease-curve placeholder:text-[#A0AEC0] focus:border-secondary-300 focus-visible:outline-none w-full"
          placeholder="Search brands"
          type="text"
          v-model="searchQuery"
        >
        <button 
          class="text-12xl leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 ease-curve !ring-0 !ring-offset-0 text-white bg-[#6366F1] hover:bg-[#5558E7] active:bg-[#4F51D6] h-[46px] py-2 px-4 mr-2"
          @click="searchBrands"
        >
          Search
        </button>
      </div>
    </div>

    <!-- Brands Table -->
    <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
      <table class="w-full caption-bottom text-sm">
        <thead class="[&_tr]:border-b">
          <tr class="border-b transition-colors duration-200 ease-curve hover:bg-white">
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 min-w-64">
              <div class="flex items-center">Brand</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center">Number of products</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center">Total sales</div>
            </th>
          </tr>
        </thead>
        <tbody class="[&_tr:last-child]:border-0">
          <tr 
            v-for="brand in paginatedBrands" 
            :key="brand.id"
            class="border-b transition-colors duration-200 ease-curve hover:bg-secondary-100 cursor-pointer"
            @click="goToBrandDetail(brand)"
          >
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000 max-w-64">
              <div class="flex items-center gap-2">
                <img 
                  :alt="brand.name"
                  :src="brand.image"
                  class="rounded-md object-cover"
                  width="40"
                  height="40"
                >
                <button class="!ring-0 text-left truncate w-auto">{{ brand.name }}</button>
              </div>
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              {{ brand.products }}
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              {{ formatCurrency(brand.sales) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 修改分页器部分 -->
    <div class="mt-4 flex justify-between items-center">
      <!-- 显示结果数量 -->
      <div class="text-sm text-gray-700">
        Showing {{ startIndex }} to {{ Math.min(endIndex, totalItems) }} of {{ totalItems }}
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
              class="px-3 py-1 rounded"
              :class="[
                currentPage === n 
                  ? 'bg-primary-500 text-white' 
                  : 'text-gray-600 hover:text-primary-600'
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
            <span class="text-sm">›</span>
          </button>
        </div>
      </div>

      <!-- 空的 div 用于保持布局��衡 -->
      <div class="invisible text-sm text-gray-700">
        Showing {{ startIndex }} to {{ Math.min(endIndex, totalItems) }} of {{ totalItems }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Brands',
  data() {
    return {
      searchQuery: '',
      brands: [
        {
          id: 1,
          name: 'Halara US',
          image: 'https://btsplwsgjvpilxywmaba.supabase.co/storage/v1/object/public/sellers_photos/7495304734897637668.png',
          products: 918,
          sales: 76915900
        },
        {
          id: 2,
          name: 'Micro Ingredients',
          image: 'https://btsplwsgjvpilxywmaba.supabase.co/storage/v1/object/public/sellers_photos/7494949083499694765.png',
          products: 180,
          sales: 73037300
        },
        {
          id: 3,
          name: 'Tarte Cosmetics',
          image: 'https://picsum.photos/40/40?random=1',
          products: 97,
          sales: 65476100
        },
        {
          id: 4,
          name: 'The Beachwaver',
          image: 'https://picsum.photos/40/40?random=2',
          products: 90,
          sales: 58936500
        },
        {
          id: 5,
          name: 'Wavytalk',
          image: 'https://picsum.photos/40/40?random=3',
          products: 32,
          sales: 48898800
        },
        {
          id: 6,
          name: 'O QQ',
          image: 'https://picsum.photos/40/40?random=4',
          products: 84,
          sales: 43574400
        },
        {
          id: 7,
          name: 'GuruNanda LLC',
          image: 'https://picsum.photos/40/40?random=5',
          products: 97,
          sales: 39630200
        },
        {
          id: 8,
          name: 'CANVAS BEAUTY BRAND',
          image: 'https://picsum.photos/40/40?random=6',
          products: 16,
          sales: 37973100
        },
        {
          id: 9,
          name: 'Sweet Furniture',
          image: 'https://picsum.photos/40/40?random=7',
          products: 122,
          sales: 37493500
        },
        {
          id: 10,
          name: 'Goli Nutrition',
          image: 'https://picsum.photos/40/40?random=8',
          products: 19,
          sales: 35083000
        },
        {
          id: 11,
          name: 'Eco Friendly',
          image: 'https://picsum.photos/40/40?random=9',
          products: 45,
          sales: 32150000
        }
      ],
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    filteredBrands() {
      if (!this.searchQuery) return this.brands;
      const query = this.searchQuery.toLowerCase();
      return this.brands.filter(brand => 
        brand.name.toLowerCase().includes(query)
      );
    },
    paginatedBrands() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredBrands.slice(start, end);
    },
    totalItems() {
      return this.filteredBrands.length;
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      
      let pages = [];
      
      // 由于总页数很少，我们可以直接显示所有页码
      for (let i = 1; i <= total; i++) {
        pages.push(i);
      }
      
      return pages;
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage - 1, this.totalItems);
    }
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value)
    },
    searchBrands() {
      this.currentPage = 1; // 搜索时重置页码到第一页
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
    },
    goToBrandDetail(brand) {
      this.$router.push(`/brands/${brand.id}`);
    }
  },
  watch: {
    searchQuery() {
      this.currentPage = 1; // 搜索条件改变时重置页码
    }
  }
}
</script>

<style scoped>
/* 分页器样式 */
.text-primary-600 {
  color: #6366F1;
}

.bg-primary-500 {
  background-color: #6366F1;
}

.hover\:text-primary-600:hover {
  color: #6366F1;
}

/* 禁用状态的按钮样式 */
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 分页按钮的过渡效果 */
button {
  transition: all 0.2s ease-in-out;
}

/* 添加 placeholder 样式 */
input::placeholder {
  color: #A0AEC0;
}
</style> 