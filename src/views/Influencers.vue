<template>
  <div class="px-8 py-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-gray-900">Find TikTok Shop Influencers</h2>
      <div class="flex items-center gap-2">
        <button class="export-button" @click="showExportModal = true">
          Export Results
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="rounded-lg">
      <div class="mb-6">
        <h3 class="font-semibold mb-2">Target Influencers</h3>
        <div class="grid grid-cols-3 gap-4 items-center mb-4">
          <!-- Search Input -->
          <input 
            type="text"
            placeholder="Search by topic/keywords, handle, or email"
            class="search-input"
            v-model="searchQuery"
          >
          
          <!-- Category Dropdown -->
          <div class="relative" v-click-outside="closeCategoryDropdown">
            <button 
              @click="toggleCategoryDropdown"
              class="filter-select flex justify-between items-center w-full appearance-none bg-no-repeat bg-right pr-8"
              style="background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2220%22%20height%3D%2220%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22%236B7280%22%3E%3Cpath%20fill-rule%3D%22evenodd%22%20d%3D%22M5.293%207.293a1%201%200%20011.414%200L10%2010.586l3.293-3.293a1%201%200%20111.414%201.414l-4%204a1%201%200%2001-1.414%200l-4-4a1%201%200%20010-1.414z%22%20clip-rule%3D%22evenodd%22%2F%3E%3C%2Fsvg%3E'); background-position: right 0.5rem center;"
            >
              <span v-if="selectedCategories.length === 0" class="text-secondary-500">Category</span>
              <span v-else>{{ selectedCategories.length }} categories selected</span>
            </button>

            <div v-if="showCategoryDropdown" class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg">
              <div class="p-2">
                <input 
                  type="text"
                  placeholder="Search..."
                  class="search-input mb-2"
                  v-model="categorySearchQuery"
                >
                
                <div class="max-h-60 overflow-y-auto">
                  <label class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllCategories"
                      @change="toggleAllCategories"
                      class="mr-2"
                    >
                    <span>(Select All)</span>
                  </label>
                  
                  <label 
                    v-for="category in filteredCategories" 
                    :key="category"
                    class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer"
                  >
                    <input 
                      type="checkbox"
                      v-model="selectedCategories"
                      :value="category"
                      class="mr-2"
                    >
                    <span>{{ category }}</span>
                  </label>
                </div>
              </div>
              
              <div class="border-t p-2 flex justify-center">
                <button 
                  @click="closeCategoryDropdown"
                  class="px-4 py-2 text-sm text-primary-600 hover:bg-secondary-100 rounded"
                >
                  Close
                </button>
              </div>
            </div>
          </div>

          <!-- Followers Dropdown -->
          <div class="relative" v-click-outside="closeFollowersDropdown">
            <button 
              @click="toggleFollowersDropdown"
              class="filter-select flex justify-between items-center w-full appearance-none bg-no-repeat bg-right pr-8"
              style="background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2220%22%20height%3D%2220%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22%236B7280%22%3E%3Cpath%20fill-rule%3D%22evenodd%22%20d%3D%22M5.293%207.293a1%201%200%20011.414%200L10%2010.586l3.293-3.293a1%201%200%20111.414%201.414l-4%204a1%201%200%2001-1.414%200l-4-4a1%201%200%20010-1.414z%22%20clip-rule%3D%22evenodd%22%2F%3E%3C%2Fsvg%3E'); background-position: right 0.5rem center;"
            >
              <span v-if="selectedFollowerRanges.length === 0" class="text-secondary-500">Followers</span>
              <span v-else>{{ selectedFollowerRanges.length }} ranges selected</span>
            </button>

            <div v-if="showFollowersDropdown" class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg">
              <div class="p-2">
                <input 
                  type="text"
                  placeholder="Search..."
                  class="search-input mb-2"
                  v-model="followersSearchQuery"
                >
                
                <div class="max-h-60 overflow-y-auto">
                  <label class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllFollowers"
                      @change="toggleAllFollowers"
                      class="mr-2"
                    >
                    <span>(Select All)</span>
                  </label>
                  
                  <label 
                    v-for="range in filteredFollowerRanges" 
                    :key="range"
                    class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer"
                  >
                    <input 
                      type="checkbox"
                      v-model="selectedFollowerRanges"
                      :value="range"
                      class="mr-2"
                    >
                    <span>{{ range }}</span>
                  </label>
                </div>
              </div>
              
              <div class="border-t p-2 flex justify-center">
                <button 
                  @click="closeFollowersDropdown"
                  class="px-4 py-2 text-sm text-primary-600 hover:bg-secondary-100 rounded"
                >
                  Close
                </button>
              </div>
            </div>
          </div>

          <!-- GMV Dropdown -->
          <div class="relative" v-click-outside="closeGMVDropdown">
            <button 
              @click="toggleGMVDropdown"
              class="filter-select flex justify-between items-center w-full appearance-none bg-no-repeat bg-right pr-8"
              style="background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2220%22%20height%3D%2220%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22%236B7280%22%3E%3Cpath%20fill-rule%3D%22evenodd%22%20d%3D%22M5.293%207.293a1%201%200%20011.414%200L10%2010.586l3.293-3.293a1%201%200%20111.414%201.414l-4%204a1%201%200%2001-1.414%200l-4-4a1%201%200%20010-1.414z%22%20clip-rule%3D%22evenodd%22%2F%3E%3C%2Fsvg%3E'); background-position: right 0.5rem center;"
            >
              <span v-if="selectedGMVs.length === 0" class="text-secondary-500">GMV</span>
              <span v-else>{{ selectedGMVs.length }} ranges selected</span>
            </button>

            <div v-if="showGMVDropdown" class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg">
              <div class="p-2">
                <input 
                  type="text"
                  placeholder="Search..."
                  class="search-input mb-2"
                  v-model="gmvSearchQuery"
                >
                
                <div class="max-h-60 overflow-y-auto">
                  <label class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllGMV"
                      @change="toggleAllGMV"
                      class="mr-2"
                    >
                    <span>(Select All)</span>
                  </label>
                  
                  <label 
                    v-for="range in filteredGMVRanges" 
                    :key="range"
                    class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer"
                  >
                    <input 
                      type="checkbox"
                      v-model="selectedGMVs"
                      :value="range"
                      class="mr-2"
                    >
                    <span>{{ range }}</span>
                  </label>
                </div>
              </div>
              
              <div class="border-t p-2 flex justify-center">
                <button 
                  @click="closeGMVDropdown"
                  class="px-4 py-2 text-sm text-primary-600 hover:bg-secondary-100 rounded"
                >
                  Close
                </button>
              </div>
            </div>
          </div>

          <!-- Gender Dropdown -->
          <select v-model="selectedGender" class="filter-select text-secondary-500">
            <option value="" class="text-secondary-500">Gender</option>
            <option value="all" class="text-secondary-500">All</option>
            <option value="male" class="text-secondary-500">Male</option>
            <option value="female" class="text-secondary-500">Female</option>
            <option value="unknown" class="text-secondary-500">Unknown</option>
          </select>

          <!-- Creator Language Dropdown -->
          <div class="relative" v-click-outside="closeLanguageDropdown">
            <button 
              @click="toggleLanguageDropdown"
              class="filter-select flex justify-between items-center w-full appearance-none bg-no-repeat bg-right pr-8"
              style="background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2220%22%20height%3D%2220%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22%236B7280%22%3E%3Cpath%20fill-rule%3D%22evenodd%22%20d%3D%22M5.293%207.293a1%201%200%20011.414%200L10%2010.586l3.293-3.293a1%201%200%20111.414%201.414l-4%204a1%201%200%2001-1.414%200l-4-4a1%201%200%20010-1.414z%22%20clip-rule%3D%22evenodd%22%2F%3E%3C%2Fsvg%3E'); background-position: right 0.5rem center;"
            >
              <span v-if="selectedLanguages.length === 0" class="text-secondary-500">Creator Language</span>
              <span v-else>{{ selectedLanguages.length }} languages selected</span>
            </button>

            <div v-if="showLanguageDropdown" class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-md shadow-lg">
              <div class="p-2">
                <input 
                  type="text"
                  placeholder="Search..."
                  class="search-input mb-2"
                  v-model="languageSearchQuery"
                >
                
                <div class="max-h-60 overflow-y-auto">
                  <label class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllLanguages"
                      @change="toggleAllLanguages"
                      class="mr-2"
                    >
                    <span>(Select All)</span>
                  </label>
                  
                  <label 
                    v-for="lang in filteredLanguages" 
                    :key="lang"
                    class="flex items-center p-2 hover:bg-secondary-100 cursor-pointer"
                  >
                    <input 
                      type="checkbox"
                      v-model="selectedLanguages"
                      :value="lang"
                      class="mr-2"
                    >
                    <span>{{ lang }}</span>
                  </label>
                </div>
              </div>
              
              <div class="border-t p-2 flex justify-center">
                <button 
                  @click="closeLanguageDropdown"
                  class="px-4 py-2 text-sm text-primary-600 hover:bg-secondary-100 rounded"
                >
                  Close
                </button>
              </div>
            </div>
          </div>

          <!-- Email Checkbox -->
          <div class="flex items-center">
            <div class="relative flex items-center">
              <input 
                type="checkbox" 
                id="withEmail" 
                v-model="onlyWithEmail"
                class="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500"
              >
              <label for="withEmail" class="ml-2 text-sm text-gray-700">
                Only show creators with an email
              </label>
            </div>
          </div>

          <!-- Empty div for spacing -->
          <div></div>

          <!-- Reset Button -->
          <div class="flex justify-end">
            <button 
              @click="resetFilters"
              class="reset-button flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-600 bg-white border border-primary-600 rounded-md hover:bg-primary-50 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Reset
            </button>
          </div>
        </div>
      </div>

      <!-- Results Table -->
      <div class="relative w-full overflow-x-auto rounded-sm border border-secondary-100 bg-white">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b">
              <th class="p-3 text-left">Handle</th>
              <th class="p-3 text-left">Bio</th>
              <th class="p-3 text-left">Product Category</th>
              <th class="p-3 text-left">Follower Count</th>
              <th class="p-3 text-left">GMV (Last 30 Days)</th>
              <th class="p-3 text-left">Profile</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="influencer in paginatedInfluencers" :key="influencer.handle" class="border-b hover:bg-secondary-100">
              <td class="p-3">
                <div class="flex items-center">
                  <img 
                    :src="`https://api.dicebear.com/7.x/pixel-art/svg?seed=${influencer.handle}`" 
                    class="w-10 h-10 rounded-full mr-3 bg-gray-100 object-cover"
                    :alt="influencer.handle"
                  />
                  <div>
                    <div>{{ influencer.handle }}</div>
                    <div class="text-xs text-gray-500">{{ influencer.email }}</div>
                  </div>
                </div>
              </td>
              <td class="p-3">{{ influencer.bio }}</td>
              <td class="p-3">
                <div class="flex flex-wrap gap-1">
                  <span v-for="cat in influencer.categories" :key="cat" 
                    class="px-2 py-1 text-xs bg-secondary-100 rounded-md border">
                    {{ cat }}
                  </span>
                </div>
              </td>
              <td class="p-3">{{ influencer.followers }}</td>
              <td class="p-3">{{ influencer.gmv }}</td>
              <td class="p-3">
                <a 
                  :href="influencer.profileUrl" 
                  target="_blank" 
                  class="text-blue-600 hover:text-blue-800 hover:underline"
                >
                  {{ influencer.profile }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页部分 -->
      <div class="mt-4 flex justify-between items-center">
        <!-- 显示结果数量 -->
        <div class="text-sm text-gray-700">
          Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, filteredInfluencers.length) }} of {{ filteredInfluencers.length }}
        </div>

        <!-- 分页按钮容器 - 居中 -->
        <div class="flex-1 flex justify-center">
          <div class="flex items-center space-x-1">
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
                @click="handlePageChange(n)"
                :class="[
                  'px-3 py-1 rounded',
                  currentPage === n ? 'bg-primary-500 text-white' : 'text-gray-600 hover:text-primary-600'
                ]"
              >
                {{ n }}
              </button>
              <span v-else class="px-2">...</span>
            </template>

            <button 
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="px-2 py-1 text-gray-600 hover:text-primary-600"
            >
              <span class="text-sm">›</span>
            </button>
          </div>
        </div>

        <!-- 空的 div 用于保持布局平衡 -->
        <div class="invisible text-sm text-gray-700">
          Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, filteredInfluencers.length) }} of {{ filteredInfluencers.length }}
        </div>
      </div>
    </div>

    <!-- 添加导出弹窗 -->
    <ExportModal
      :show="showExportModal"
      :filters="{
        categories: selectedCategories,
        gmv: selectedGMVs,
        followers: selectedFollowerRanges,
        gender: selectedGender,
        languages: selectedLanguages,
        onlyWithEmail: onlyWithEmail
      }"
      :influencers="filteredInfluencers"
      @close="showExportModal = false"
      @create="handleCreateList"
    />
  </div>
</template>

<script>
import ExportModal from '../components/ExportModal.vue'

export default {
  components: {
    ExportModal
  },
  data() {
    return {
      searchQuery: '',
      showCategoryDropdown: false,
      showGMVDropdown: false,
      showFollowersDropdown: false,
      showLanguageDropdown: false,
      
      categorySearchQuery: '',
      gmvSearchQuery: '',
      followersSearchQuery: '',
      languageSearchQuery: '',
      
      selectedCategories: [],
      selectedGMVs: [],
      selectedFollowerRanges: [],
      selectedLanguages: [],
      selectedGender: '',
      
      onlyWithEmail: false,

      categories: [
        'Home Supplies',
        'Kitchenware',
        'Textiles & Soft Furnishings',
        'Household Appliances',
        'Womenswear & Underwear',
        'Shoes',
        'Beauty & Personal Care',
        'Phones & Electronics',
        'Computers & Office Equipment',
        'Pet Supplies',
        'Baby & Maternity',
        'Sports & Outdoor',
        'Toys & Hobbies',
        'Furniture',
        'Tools & Hardware',
        'Home Improvement',
        'Automotive & Motorcycle',
        'Fashion Accessories',
        'Food & Beverages',
        'Health',
        'Books, Magazines & Audio',
        'Menswear & Underwear',
        'Luggage & Bags',
        'Collectibles',
        'Jewelry Accessories & Derivatives'
      ],

      followerRanges: [
        '0-20K',
        '20K-100K',
        '100K-1M',
        '1M+'
      ],

      gmvRanges: [
        '$0-$100',
        '$100-$1K',
        '$1K-$10K',
        '$10K+'
      ],

      languages: [
        'English',
        'Spanish',
        'French',
        'German',
        'Chinese',
        'Japanese',
        'Korean'
      ],

      influencers: [
        {
          handle: 'techie_sarah',
          email: 'sarah.tech@email.com',
          bio: '📱 Tech Reviews | 🎮 Gaming | 💻 Best Deals | She/Her',
          categories: ['Electronics', 'Phones & Electronics', 'Computers & Office Equipment'],
          followers: '328K',
          gmv: '$2.8M',
          gender: 'female',
          language: 'English',
          engagement: '4.2%',
          profile: '@techie_sarah',
          profileUrl: 'https://example.com/techie_sarah'
        },
        {
          handle: 'beauty_queen_lisa',
          email: 'lisa.beauty@email.com',
          bio: '💄 Beauty Tips | 💅 Skincare | 💋 Lifestyle | DM for collabs',
          categories: ['Beauty & Personal Care', 'Fashion Accessories'],
          followers: '464K',
          gmv: '$3.2M',
          gender: 'female',
          language: 'English',
          engagement: '5.1%',
          profile: '@beauty_queen_lisa',
          profileUrl: 'https://example.com/beauty_queen_lisa'
        },
        {
          handle: 'home_style_master',
          email: '',
          bio: ' 🖼️ Home Decor  |  Interior Design | 🎨 DIY Projects',
          categories: ['Home Supplies', 'Furniture', 'Home Improvement'],
          followers: '223K',
          gmv: '$1.6M',
          gender: 'unknown',
          language: 'English',
          engagement: '3.8%',
          profile: '@home_style_master',
          profileUrl: 'https://example.com/home_style_master'
        },
        {
          handle: 'fitness_mike',
          email: 'mike.fit@email.com',
          bio: '💪 Fitness Coach | 🥗 Nutrition | 🏃‍♂️ Running Tips | He/Him',
          categories: ['Sports & Outdoor', 'Health'],
          followers: '156K',
          gmv: '$980K',
          gender: 'male',
          language: 'English',
          engagement: '4.5%',
          profile: '@fitness_mike',
          profileUrl: 'https://example.com/fitness_mike'
        },
        {
          handle: 'cooking_with_maria',
          email: 'maria.cook@email.com',
          bio: '👩‍🍳 Chef | 🍳 Recipe Creator | 🥘 Kitchen Tips | Español/English',
          categories: ['Kitchenware', 'Food & Beverages'],
          followers: '289K',
          gmv: '$1.9M',
          gender: 'female',
          language: 'Spanish',
          engagement: '6.2%',
          profile: '@cooking_with_maria',
          profileUrl: 'https://example.com/cooking_with_maria'
        },
        {
          handle: 'pet_paradise',
          email: 'pets@email.com',
          bio: '🐶 Pet Care | 🐶 Training Tips | 🦮 Pet Products Reviews',
          categories: ['Pet Supplies', 'Toys & Hobbies'],
          followers: '198K',
          gmv: '$1.1M',
          gender: 'unknown',
          language: 'English',
          engagement: '4.8%',
          profile: '@pet_paradise',
          profileUrl: 'https://example.com/pet_paradise'
        },
        {
          handle: 'fashion_david',
          email: 'david.style@email.com',
          bio: '👔 Men\'s Fashion | 👞 Footwear | 🕶️ Accessories | For Him',
          categories: ['Menswear & Underwear', 'Shoes', 'Fashion Accessories'],
          followers: '175K',
          gmv: '$2.1M',
          gender: 'male',
          language: 'English',
          engagement: '3.9%',
          profile: '@fashion_david',
          profileUrl: 'https://example.com/fashion_david'
        },
        {
          handle: 'baby_expert_anna',
          email: 'anna.baby@email.com',
          bio: '👶 Baby Care | 🍼 Parenting Tips | 🧸 Baby Products | Mom of 2',
          categories: ['Baby & Maternity', 'Toys & Hobbies'],
          followers: '312K',
          gmv: '$2.4M',
          gender: 'female',
          language: 'English',
          engagement: '5.7%',
          profile: '@baby_expert_anna',
          profileUrl: 'https://example.com/baby_expert_anna'
        },
        {
          handle: 'books_and_beyond',
          email: '',
          bio: '📚 Book Reviews | 🎧 Audiobooks | 📖 Reading Lists',
          categories: ['Books, Magazines & Audio', 'Collectibles'],
          followers: '145K',
          gmv: '$670K',
          gender: 'unknown',
          language: 'English',
          engagement: '4.1%',
          profile: '@books_and_beyond',
          profileUrl: 'https://example.com/books_and_beyond'
        },
        {
          handle: 'craft_master_jen',
          email: 'jen.crafts@email.com',
          bio: 'DIY Crafts | ✂️ Art Supplies | 🖼️ Home Decor | She/Her',
          categories: ['Art Supplies', 'Home Improvement', 'Toys & Hobbies'],
          followers: '234K',
          gmv: '$1.5M',
          gender: 'female',
          language: 'English',
          engagement: '5.3%',
          profile: '@craft_master_jen',
          profileUrl: 'https://example.com/craft_master_jen'
        },
        {
          handle: 'auto_expert_tom',
          email: 'tom.auto@email.com',
          bio: '🚗 Car Reviews | 🔧 Auto Tips | 🏍️ Motorcycle Gear | He/Him',
          categories: ['Automotive & Motorcycle', 'Tools & Hardware'],
          followers: '187K',
          gmv: '$1.8M',
          gender: 'male',
          language: 'English',
          engagement: '4.4%',
          profile: '@auto_expert_tom',
          profileUrl: 'https://example.com/auto_expert_tom'
        },
        {
          handle: 'travel_gear_pro',
          email: 'travel.pro@email.com',
          bio: '✈️ Travel Gear | 🎒 Bags | 🧳 Luggage Reviews | Global',
          categories: ['Luggage & Bags', 'Travel Accessories'],
          followers: '256K',
          gmv: '$2.2M',
          gender: 'unknown',
          language: 'English',
          engagement: '4.7%',
          profile: '@travel_gear_pro',
          profileUrl: 'https://example.com/travel_gear_pro'
        },
        {
          handle: 'smart_home_tech',
          email: 'smart.home@email.com',
          bio: '🏠 Smart Home Reviews | 💡 IoT Devices | 🔌 Tech Tips',
          categories: ['Electronics', 'Home Improvement', 'Household Appliances'],
          followers: '167K',
          gmv: '$1.3M',
          gender: 'unknown',
          language: 'English',
          engagement: '3.8%',
          profile: '@smart_home_tech',
          profileUrl: 'https://example.com/smart_home_tech'
        },
        {
          handle: 'garden_guru',
          email: 'garden@email.com',
          bio: '🌺 Garden Design | 🌱 Plant Care | 🏡 Outdoor Living',
          categories: ['Home Supplies', 'Tools & Hardware'],
          followers: '143K',
          gmv: '$890K',
          gender: 'female',
          language: 'English',
          engagement: '4.9%',
          profile: '@garden_guru',
          profileUrl: 'https://example.com/garden_guru'
        },
        {
          handle: 'sports_gear_pro',
          email: 'sports@email.com',
          bio: '⚽ Sports Equipment | 🎒 Reviews | 🏃‍♂️ Fitness Gear',
          categories: ['Sports & Outdoor', 'Shoes'],
          followers: '278K',
          gmv: '$2.5M',
          gender: 'male',
          language: 'English',
          engagement: '5.2%',
          profile: '@sports_gear_pro',
          profileUrl: 'https://example.com/sports_gear_pro'
        },
        {
          handle: 'jewelry_queen',
          email: 'jewelry@email.com',
          bio: '💎 Jewelry Reviews | 💎 Accessories | ✨ Style Tips',
          categories: ['Jewelry Accessories & Derivatives', 'Fashion Accessories'],
          followers: '198K',
          gmv: '$3.1M',
          gender: 'female',
          language: 'English',
          engagement: '6.1%',
          profile: '@jewelry_queen',
          profileUrl: 'https://example.com/jewelry_queen'
        },
        {
          handle: 'office_setup',
          email: 'office.pro@email.com',
          bio: '💼 Office Equipment | 💻 WFH Setup | 🖨️ Tech Reviews',
          categories: ['Computers & Office Equipment', 'Furniture'],
          followers: '134K',
          gmv: '$950K',
          gender: 'unknown',
          language: 'English',
          engagement: '3.7%',
          profile: '@office_setup',
          profileUrl: 'https://example.com/office_setup'
        },
        {
          handle: 'kitchen_master',
          email: 'kitchen.pro@email.com',
          bio: '🍳 Kitchen Gadgets | 🔪 Cookware | 🍽️ Reviews',
          categories: ['Kitchenware', 'Home Supplies'],
          followers: '245K',
          gmv: '$1.7M',
          gender: 'male',
          language: 'English',
          engagement: '4.8%',
          profile: '@kitchen_master',
          profileUrl: 'https://example.com/kitchen_master'
        },
        {
          handle: 'art_supplies_guru',
          email: 'art.guru@email.com',
          bio: '🎨 Art Supplies | ✏️ Drawing Tools | 🖼️ Reviews',
          categories: ['Art Supplies', 'Books, Magazines & Audio'],
          followers: '167K',
          gmv: '$780K',
          gender: 'female',
          language: 'English',
          engagement: '5.4%',
          profile: '@art_supplies_guru',
          profileUrl: 'https://example.com/art_supplies_guru'
        },
        {
          handle: 'baby_fashion',
          email: 'baby.style@email.com',
          bio: '👶 Baby Fashion | 🧸 Kids Wear | 🎀 Accessories',
          categories: ['Baby & Maternity', 'Fashion Accessories'],
          followers: '189K',
          gmv: '$1.4M',
          gender: 'female',
          language: 'English',
          engagement: '4.7%',
          profile: '@baby_fashion',
          profileUrl: 'https://example.com/baby_fashion'
        },
        {
          handle: 'pet_fashion',
          email: 'pet.style@email.com',
          bio: '🐱 Pet Fashion | 🐶 Pet Accessories | 🦮 Reviews',
          categories: ['Pet Supplies', 'Fashion Accessories'],
          followers: '156K',
          gmv: '$920K',
          gender: 'female',
          language: 'English',
          engagement: '5.3%',
          profile: '@pet_fashion',
          profileUrl: 'https://example.com/pet_fashion'
        },
        {
          handle: 'mens_grooming',
          email: 'grooming@email.com',
          bio: '💈 Men\'s Grooming | 🧔 Beard Care | ✨ Style Tips',
          categories: ['Beauty & Personal Care', 'Menswear & Underwear'],
          followers: '212K',
          gmv: '$1.6M',
          gender: 'male',
          language: 'English',
          engagement: '4.6%',
          profile: '@mens_grooming',
          profileUrl: 'https://example.com/mens_grooming'
        }
      ],

      currentPage: 1,
      pageSize: 10,
      showExportModal: false
    }
  },
  computed: {
    filteredCategories() {
      if (!this.categorySearchQuery) return this.categories;
      const query = this.categorySearchQuery.toLowerCase();
      return this.categories.filter(category => 
        category.toLowerCase().includes(query)
      );
    },

    filteredGMVRanges() {
      if (!this.gmvSearchQuery) return this.gmvRanges;
      const query = this.gmvSearchQuery.toLowerCase();
      return this.gmvRanges.filter(range => 
        range.toLowerCase().includes(query)
      );
    },

    filteredFollowerRanges() {
      if (!this.followersSearchQuery) return this.followerRanges;
      const query = this.followersSearchQuery.toLowerCase();
      return this.followerRanges.filter(range => 
        range.toLowerCase().includes(query)
      );
    },

    filteredLanguages() {
      if (!this.languageSearchQuery) return this.languages;
      const query = this.languageSearchQuery.toLowerCase();
      return this.languages.filter(lang => 
        lang.toLowerCase().includes(query)
      );
    },

    selectAllCategories: {
      get() {
        return this.selectedCategories.length === this.categories.length;
      },
      set(value) {
        this.selectedCategories = value ? [...this.categories] : [];
      }
    },

    selectAllGMV: {
      get() {
        return this.selectedGMVs.length === this.gmvRanges.length;
      },
      set(value) {
        this.selectedGMVs = value ? [...this.gmvRanges] : [];
      }
    },

    selectAllFollowers: {
      get() {
        return this.selectedFollowerRanges.length === this.followerRanges.length;
      },
      set(value) {
        this.selectedFollowerRanges = value ? [...this.followerRanges] : [];
      }
    },

    selectAllLanguages: {
      get() {
        return this.selectedLanguages.length === this.languages.length;
      },
      set(value) {
        this.selectedLanguages = value ? [...this.languages] : [];
      }
    },

    filteredInfluencers() {
      return this.influencers.filter(influencer => {
        const searchMatch = !this.searchQuery || 
          influencer.handle.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          influencer.bio.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (influencer.email && influencer.email.toLowerCase().includes(this.searchQuery.toLowerCase()));

        const categoryMatch = this.selectedCategories.length === 0 || 
          influencer.categories.some(cat => this.selectedCategories.includes(cat));

        const followersMatch = this.selectedFollowerRanges.length === 0 || 
          this.selectedFollowerRanges.some(range => 
            this.matchFollowerRange(influencer.followers, range)
          );

        const gmvMatch = this.selectedGMVs.length === 0 || 
          this.selectedGMVs.some(range => 
            this.matchGMVRange(influencer.gmv, range)
          );

        const genderMatch = !this.selectedGender || 
          this.selectedGender === 'all' || 
          influencer.gender === this.selectedGender;

        const languageMatch = this.selectedLanguages.length === 0 || 
          this.selectedLanguages.includes(influencer.language);

        const emailMatch = !this.onlyWithEmail || this.hasValidEmail(influencer.email);

        return searchMatch && categoryMatch && followersMatch && 
               gmvMatch && genderMatch && languageMatch && emailMatch;
      });
    },

    totalPages() {
      return Math.ceil(this.filteredInfluencers.length / this.pageSize);
    },
    
    paginatedInfluencers() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredInfluencers.slice(start, end);
    },

    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      const delta = 1; // 当前页码前后显示的页码数

      let pages = [];
      const left = current - delta;
      const right = current + delta;

      for (let i = 1; i <= total; i++) {
        if (
          i === 1 || // 第一页
          i === total || // 最后一页
          (i >= left && i <= right) // 当前页码附近的页码
        ) {
          pages.push(i);
        } else if (pages[pages.length - 1] !== '...') {
          pages.push('...');
        }
      }

      return pages;
    },

    storeInfluencers() {
      return this.$store.getters.getInfluencers
    }
  },
  methods: {
    matchFollowerRange(followers, range) {
      const count = parseInt(followers.replace(/[K,M]/g, ''))
      switch(range) {
        case '0-20K': return count < 20
        case '20K-100K': return count >= 20 && count < 100
        case '100K-1M': return count >= 100 && count < 1000
        case '1M+': return count >= 1000
        default: return true
      }
    },
    matchGMVRange(gmv, range) {
      const amount = parseFloat(gmv.replace(/[$,M,K]/g, ''))
      switch(range) {
        case '$0-$100': return amount < 0.1
        case '$100-$1K': return amount >= 0.1 && amount < 1
        case '$1K-$10K': return amount >= 1 && amount < 10
        case '$10K+': return amount >= 10
        default: return true
      }
    },
    inferGender(handle, bio) {
      const femaleIndicators = ['she', 'her', 'girl', 'mom', 'mama', 'wife', 'sister', '💄', '👗', '👚'];
      const maleIndicators = ['he', 'his', 'guy', 'dad', 'papa', 'husband', 'brother', '👨'];
      
      const text = (handle + ' ' + bio).toLowerCase();
      
      let femaleScore = 0;
      let maleScore = 0;
      
      femaleIndicators.forEach(indicator => {
        if (text.includes(indicator.toLowerCase())) femaleScore++;
      });
      
      maleIndicators.forEach(indicator => {
        if (text.includes(indicator.toLowerCase())) maleScore++;
      });
      
      if (femaleScore > maleScore) return 'female';
      if (maleScore > femaleScore) return 'male';
      return 'unknown';
    },
    hasValidEmail(email) {
      if (!email) return false;
      if (email.trim().length === 0) return false;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    toggleCategoryDropdown() {
      this.showCategoryDropdown = !this.showCategoryDropdown;
    },
    closeCategoryDropdown() {
      this.showCategoryDropdown = false;
    },
    toggleAllCategories() {
      if (this.selectAllCategories) {
        this.selectedCategories = [...this.categories];
      } else {
        this.selectedCategories = [];
      }
    },
    toggleFollowersDropdown() {
      this.showFollowersDropdown = !this.showFollowersDropdown;
    },
    closeFollowersDropdown() {
      this.showFollowersDropdown = false;
    },
    toggleAllFollowers() {
      if (this.selectAllFollowers) {
        this.selectedFollowerRanges = [...this.followerRanges];
      } else {
        this.selectedFollowerRanges = [];
      }
    },
    toggleGMVDropdown() {
      this.showGMVDropdown = !this.showGMVDropdown;
    },
    closeGMVDropdown() {
      this.showGMVDropdown = false;
    },
    toggleAllGMV() {
      if (this.selectAllGMV) {
        this.selectedGMVs = [...this.gmvRanges];
      } else {
        this.selectedGMVs = [];
      }
    },
    toggleLanguageDropdown() {
      this.showLanguageDropdown = !this.showLanguageDropdown;
    },
    closeLanguageDropdown() {
      this.showLanguageDropdown = false;
    },
    toggleAllLanguages() {
      if (this.selectAllLanguages) {
        this.selectedLanguages = [...this.languages];
      } else {
        this.selectedLanguages = [];
      }
    },
    handlePageChange(page) {
      this.currentPage = page;
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
    resetFilters() {
      this.searchQuery = '';
      this.categorySearchQuery = '';
      this.gmvSearchQuery = '';
      this.followersSearchQuery = '';
      this.languageSearchQuery = '';
      this.selectedCategories = [];
      this.selectedGMVs = [];
      this.selectedFollowerRanges = [];
      this.selectedLanguages = [];
      this.selectedGender = '';
      this.onlyWithEmail = false;
    },
    handleCreateList(listData) {
      this.$store.dispatch('createList', listData);
      this.$router.push('/lists');
    }
  },
  directives: {
    'click-outside': {
      mounted(el, binding) {
        el.clickOutsideEvent = function(event) {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value(event);
          }
        };
        document.addEventListener('click', el.clickOutsideEvent);
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent);
      }
    }
  },
  watch: {
    searchQuery() {
      this.currentPage = 1;
    },
    selectedCategories: {
      handler() {
        this.currentPage = 1;
      },
      deep: true
    },
    selectedFollowerRanges: {
      handler() {
        this.currentPage = 1;
      },
      deep: true
    },
    selectedGMVs: {
      handler() {
        this.currentPage = 1;
      },
      deep: true
    },
    selectedGender() {
      this.currentPage = 1;
    },
    selectedLanguages: {
      handler() {
        this.currentPage = 1;
      },
      deep: true
    },
    onlyWithEmail() {
      this.currentPage = 1;
    }
  },
  created() {
    // 确保初始数据被加载到 store 中
    if (this.influencers.length) {
      this.$store.dispatch('setInfluencers', this.influencers)
    }
  }
}
</script>

<style scoped>
.search-input {
  @apply flex min-h-10 w-full rounded-md border border-secondary-300 bg-white px-4 py-3 text-[16px] 
  leading-[19.2px] !ring-0 transition-all;
}

.search-input::placeholder {
  @apply text-secondary-500;
}

.filter-select {
  @apply flex w-full min-h-[45px] rounded-md border border-secondary-300 bg-white px-4 py-1 
  text-[16px] leading-[19.2px] !ring-0 cursor-pointer text-secondary-500 relative;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23374151' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 1rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 4rem;
}

.filter-select::-ms-expand {
  display: none;
}

.filter-select {
  -moz-appearance: none;
  text-indent: 0.01px;
  text-overflow: '';
}

.filter-select {
  -webkit-appearance: none;
}

.export-button {
  @apply py-2.5 px-6 text-sm leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap 
  rounded-[10px] transition-all !ring-0 !ring-offset-0 border bg-transparent 
  border-secondary-400 hover:bg-secondary-100 text-primary-500;
}

.info-button {
  @apply p-2 text-gray-500 hover:bg-secondary-100 rounded-lg transition-all;
}

.clear-button {
  @apply absolute right-12;
}

/* 修改下拉箭头和清除按钮的样式 */
.view-count-dropdown button {
  margin-right: 1rem;  /* 增加清除按钮右侧间距 */
}

/* 调整下拉箭头的位置 */
.view-count-dropdown span {
  margin-left: 0.5rem;  /* 给下拉箭头增加左侧间距 */
}

/* 确保容器有足够空间 */
.view-count-dropdown .flex {
  padding-right: 3rem;  /* 增加右侧内边距，为图标留出空间 */
}
</style> 