<template>
  <div class="px-[50px] py-4">
    <!-- 标题部分 -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-gray-900">Products</h2>
    </div>

    <!-- 产品列表表格 -->
    <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
      <table class="w-full caption-bottom text-sm">
        <!-- 表头 -->
        <thead class="[&_tr]:border-b">
          <tr class="border-b transition-colors hover:bg-white">
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800 min-w-64">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Product</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Price</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Sold Count</div>
            </th>
          </tr>
        </thead>

        <!-- 表格内容 -->
        <tbody class="[&_tr:last-child]:border-0">
          <tr 
            v-for="product in getCurrentPageProducts" 
            :key="product.id"
            class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
            @click="viewProductDetail(product)"
          >
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000 max-w-64">
              <div class="flex items-center gap-2">
                <img 
                  :src="product.image" 
                  :alt="product.name"
                  class="rounded-md object-cover w-10 h-10"
                >
                <button class="!ring-0 text-left truncate w-auto">
                  {{ product.name }}
                </button>
              </div>
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              ${{ product.price }}
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              {{ product.soldCount }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页部分 - 移到表格外面 -->
    <div class="mt-4 flex justify-between items-center">
      <!-- 显示数量信息 -->
      <div class="text-secondary-500 text-sm leading-[19.2px] w-[35%]">
        Showing {{ startIndex }} to {{ Math.min(endIndex, totalProducts) }} of {{ totalProducts }}
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
</template>

<script>
export default {
  name: 'Products',
  data() {
    return {
      products: [
        {
          id: 1,
          name: '15 Day Cleanse - Gut and Colon Support | Caffeine Free | Advanced Formula with Senna, Cascara Sagrada, & Psyllium Husk | Non-GMO | 30 capsules',
          price: 13.99,
          soldCount: 2309886,
          image: 'https://picsum.photos/200/200?random=1'
        },
        {
          id: 2,
          name: 'GuruNanda Cocomint Pulling Oil with 7 Essential Oils & Vitamins D, E & K2 - 8 oz',
          price: 10.99,
          soldCount: 1853174,
          image: 'https://picsum.photos/200/200?random=2'
        },
        {
          id: 3,
          name: 'Car Air Freshener Diffusers',
          price: 3.99,
          soldCount: 1091222,
          image: 'https://picsum.photos/200/200?random=3'
        },
        {
          id: 4,
          name: 'LIP LINER STAY-N - Peel-Off Lip Liner Stain - Lasts All Day & Night Eyeliner Lipliner',
          price: 8.96,
          soldCount: 1041933,
          image: 'https://picsum.photos/200/200?random=4'
        },
        {
          id: 5,
          name: 'Micro Ingredients Multi Collagen Peptides Powder',
          price: 30.02,
          soldCount: 966853,
          image: 'https://picsum.photos/200/200?random=5'
        },
        {
          id: 6,
          name: 'Scented Car Air Freshener - Long Lasting Car Diffuser',
          price: 3.60,
          soldCount: 960335,
          image: 'https://picsum.photos/200/200?random=6'
        },
        {
          id: 7,
          name: '(NEW) BODY GLAZE: Pick your favorite scent!',
          price: 25.00,
          soldCount: 933760,
          image: 'https://picsum.photos/200/200?random=7'
        },
        {
          id: 8,
          name: 'Unbrush Detangling Hair Brush by FHI Heat',
          price: 13.50,
          soldCount: 927477,
          image: 'https://picsum.photos/200/200?random=8'
        },
        {
          id: 9,
          name: 'Goli Ashwagandha & Vitamin D Gummy',
          price: 13.96,
          soldCount: 910377,
          image: 'https://picsum.photos/200/200?random=9'
        },
        {
          id: 10,
          name: 'Upholstery Deodorizer (16 oz.) Household Scented',
          price: 6.00,
          soldCount: 900436,
          image: 'https://picsum.photos/200/200?random=10'
        },
        {
          id: 11,
          name: 'Premium Essential Oil Diffuser Set',
          price: 29.99,
          soldCount: 895420,
          image: 'https://picsum.photos/200/200?random=11'
        }
      ],
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    totalProducts() {
      return this.products.length
    },
    totalPages() {
      return Math.ceil(this.totalProducts / this.pageSize)
    },
    getCurrentPageProducts() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.products.slice(start, end)
    },
    startIndex() {
      return (this.currentPage - 1) * this.pageSize + 1
    },
    endIndex() {
      return Math.min(this.currentPage * this.pageSize, this.totalProducts)
    },
    displayedPages() {
      const total = this.totalPages
      const current = this.currentPage
      const delta = 1

      let pages = []
      const left = current - delta
      const right = current + delta

      for (let i = 1; i <= total; i++) {
        if (
          i === 1 ||
          i === total ||
          (i >= left && i <= right)
        ) {
          pages.push(i)
        } else if (pages[pages.length - 1] !== '...') {
          pages.push('...')
        }
      }

      return pages
    }
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
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
    viewProductDetail(product) {
      this.$router.push(`/products/${product.id}`)
    }
  }
}
</script>

<style scoped>
.min-w-64 {
  min-width: 16rem;
}
</style> 