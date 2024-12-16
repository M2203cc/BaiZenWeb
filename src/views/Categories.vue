<template>
  <div class="px-[50px] py-4">
    <!-- 标题部分 -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-gray-900">Categories</h2>
    </div>

    <!-- 分类列表表格 -->
    <div class="relative w-full overflow-x-auto overflow-y-hidden rounded-sm border border-secondary-100 bg-white">
      <table class="w-full caption-bottom text-sm">
        <!-- 表头 -->
        <thead class="[&_tr]:border-b">
          <tr class="border-b transition-colors hover:bg-white">
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Category name</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Number of products</div>
            </th>
            <th class="min-h-16 py-3 px-2 text-left align-middle text-md leading-[19.2px] text-secondary-800">
              <div class="flex items-center text-[#6C7381] font-bold text-sm">Selling points</div>
            </th>
          </tr>
        </thead>

        <!-- 表格内容 -->
        <tbody class="[&_tr:last-child]:border-0">
          <tr 
            v-for="category in categories" 
            :key="category.name"
            class="border-b transition-colors hover:bg-secondary-100 cursor-pointer"
            @click="goToCategoryDetail(category.name)"
          >
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              {{ category.name }}
            </td>
            <td class="min-h-16 py-3 px-2 align-middle text-md leading-[19.2px] text-secondary-1000">
              {{ category.productCount }}
            </td>
            <td class="min-h-16 py-3 px-2 align-middle">
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="point in category.sellingPoints" 
                  :key="point"
                  class="inline-flex items-center rounded-md border border-transparent px-2.5 py-1 text-xs font-medium text-[#6366F1]"
                >
                  {{ point }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Categories',
  methods: {
    goToCategoryDetail(categoryName) {
      // 使用 encodeURIComponent 处理可能包含特殊字符的分类名
      const encodedName = encodeURIComponent(categoryName)
      this.$router.push(`/categories/${encodedName}`)
    }
  },
  data() {
    return {
      categories: [
        {
          name: 'Womenswear & Underwear',
          productCount: 47384,
          sellingPoints: ['Emotional Connection', 'Feminist Messaging', 'Style & Versatility']
        },
        {
          name: 'Beauty & Personal Care',
          productCount: 43692,
          sellingPoints: ['Novel consumption method', 'Comedic and memorable presentation', 'Immediate visual efficacy']
        },
        {
          name: 'Home Supplies',
          productCount: 16666,
          sellingPoints: ['Novelty', 'Ease of Use', 'Affordability']
        },
        {
          name: 'Menswear & Underwear',
          productCount: 14001,
          sellingPoints: ['Limited Availability', 'Unique Design', 'Affordability']
        },
        {
          name: 'Fashion Accessories',
          productCount: 13314,
          sellingPoints: ['AirTag Compatibility', 'Unique & Fun Design', 'Sense of Urgency']
        },
        {
          name: 'Phones & Electronics',
          productCount: 11959,
          sellingPoints: ['Real-time Translation', 'Uniquely Compact and Portable', 'Unique Design & Conversation Starter']
        },
        {
          name: 'Toys & Hobbies',
          productCount: 11803,
          sellingPoints: ['Color-Changing Technology', 'Handcrafted Quality', 'Limited-Time Sale']
        },
        {
          name: 'Health',
          productCount: 9874,
          sellingPoints: ['Visual Proof of Effectiveness', 'Ingredient Transparency', 'Relatability']
        },
        {
          name: 'Sports & Outdoor',
          productCount: 9369,
          sellingPoints: ['Scarcity', 'Brand Recognition', 'Versatility']
        },
        {
          name: 'Kitchenware',
          productCount: 9265,
          sellingPoints: ['Nostalgia & Charm Design', 'Hands-Free Convenience', 'Space-Saving & Efficiency']
        },
        {
          name: 'Jewelry Accessories & Derivatives',
          productCount: 8763,
          sellingPoints: ['Self-Commitment Through Symbols', 'Cultural and Personal Customization', 'Problem-Solving Elegance']
        },
        {
          name: 'Shoes',
          productCount: 8311,
          sellingPoints: ['TikTok Shop Exclusivity', 'Fun and Relatable Presentation', 'Customizability']
        },
        {
          name: 'Food & Beverages',
          productCount: 7809,
          sellingPoints: ['Novelty and Exclusivity', 'Ease and Convenience', 'Taste and Sensory Appeal']
        },
        {
          name: 'Textiles & Soft Furnishings',
          productCount: 6337,
          sellingPoints: ['Cute and Themed Designs', 'Softness and Comfort', 'Affordability and Promotions']
        },
        {
          name: 'Books, Magazines & Audio',
          productCount: 6039,
          sellingPoints: ['Bilingual Content', 'Unique Story and Inspiration', 'Mystery and Surprise Elements']
        },
        {
          name: 'Automotive & Motorcycle',
          productCount: 5363,
          sellingPoints: ['Portability and Convenience', 'Ease of Use', 'Affordability and Value']
        },
        {
          name: 'Collectibles',
          productCount: 4781,
          sellingPoints: ['Surprise Element', 'Community Engagement', 'Nostalgia Factor']
        },
        {
          name: 'Pet Supplies',
          productCount: 4502,
          sellingPoints: ['Emotional Connection', 'Hands-Free Convenience', 'Affordability']
        },
        {
          name: 'Tools & Hardware',
          productCount: 4372,
          sellingPoints: ['Nostalgia', 'Scarcity', 'High Lumen Output']
        },
        {
          name: 'Luggage & Bags',
          productCount: 4059,
          sellingPoints: ['Emotional Relatability', 'Unique and Novel Design', 'Versatile Functionality']
        },
        {
          name: 'Furniture',
          productCount: 3675,
          sellingPoints: ['Creative Design Integration', 'Multi-Functionality', 'Urgency through Scarcity and Limited-Time Offers']
        },
        {
          name: 'Household Appliances',
          productCount: 3124,
          sellingPoints: ['Affordability', 'Convenience and Efficiency', 'Technological Features']
        },
        {
          name: 'Baby & Maternity',
          productCount: 1979,
          sellingPoints: ['Indirect Marketing', 'Relatability and Problem-Solution', 'Cuteness Overload']
        },
        {
          name: 'Computers & Office Equipment',
          productCount: 1774,
          sellingPoints: ['Stackability and Versatility', 'Educational Value', 'Affordability with Value']
        },
        {
          name: 'Home Improvement',
          productCount: 1387,
          sellingPoints: ['Transformation Capabilities', 'Multiple Access Methods', 'Easy Installation']
        }
      ]
    }
  }
}
</script> 