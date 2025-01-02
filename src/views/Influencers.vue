<template>
  <div class="px-8 py-4">
    <!-- Header 确定-->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-gray-900">搜寻 TikTok Shop 中的达人</h2>
      <div class="flex items-center gap-2">
        <button 
          @click="showExportModal = true"
          class="py-2.5 px-6 text-sm leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap rounded-[10px] transition-all duration-200 bg-[#6366F1] text-white hover:bg-[#5558E7]"
        >
          导出数据
        </button>
      </div>
    </div>

    <!-- Filters  搜索框 -->
    <div class="rounded-lg">
      <div class="mb-6">
        <h3 class="font-semibold mb-2">指定条件搜寻达人</h3>
        <div class="grid grid-cols-3 gap-4 items-center mb-4">

          <!-- Search Input  确定-->
          <input 
            type="text"
            placeholder="根据输入 昵称、邮箱、产品类别 搜寻"
            class="search-input"
            v-model="searchQuery"
          >
          
          <!-- Category Dropdown  确定-->
          <div class="relative" v-click-outside="closeCategoryDropdown">
            <!-- 类别选择按钮 -->
            <div 
              @click="toggleCategoryDropdown"
              class="filter-select flex items-center min-h-[45px] cursor-pointer px-3"
            >
              <!-- 已选类别 -->
              <div class="flex flex-wrap gap-1.5 flex-1 py-2">
                <span v-if="selectedCategories.length === 0" class="text-gray-500">类别</span>
                <span v-else>{{ selectedCategories.length }} categories selected</span>
              </div>

              <!-- 右侧按钮组 -->
              <div class="flex items-center gap-2 pl-3 border-l border-gray-200">
                <button 
                  v-if="selectedCategories.length" 
                  @click.stop="clearCategories"
                  class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Clear all"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>

            <!-- 下拉面板 -->
            <div v-if="showCategoryDropdown" class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
              <div class="p-2">
                <input 
                  type="text"
                  placeholder="Search..."
                  class="search-input mb-2"
                  v-model="categorySearchQuery"
                >
                
                <div class="max-h-60 overflow-y-auto">
                  <label class="flex items-center p-2 hover:bg-gray-100 cursor-pointer">
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
                    class="flex items-center p-2 hover:bg-gray-100 cursor-pointer"
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
                  class="px-4 py-2 text-sm text-blue-600 hover:bg-gray-100 rounded"
                >
                  Close
                </button>
              </div>
            </div>
          </div>

          <!-- Followers Dropdown  确定-->
          <div class="relative" v-click-outside="closeFollowersDropdown">
            <div 
              @click="toggleFollowersDropdown"
              class="filter-select flex items-center min-h-[45px] cursor-pointer px-3"
            >
              <!-- 已选标签区域 -->
              <div class="flex flex-wrap gap-1.5 flex-1 py-2">
                <template v-if="selectedFollowerRanges.length">
                  <span v-for="range in selectedFollowerRanges" 
                    :key="range" 
                    class="inline-flex items-center px-2 py-0.5 text-sm bg-blue-50 text-blue-700 rounded-md"
                  >
                    {{ range }}
                    <button 
                      @click.stop="removeFollowerRange(range)" 
                      class="ml-1.5 text-blue-400 hover:text-blue-600 transition-colors"
                    >
                      ×
                    </button>
                  </span>
                </template>
                <span v-else class="text-gray-500">粉丝数量</span>
              </div>

              <!-- 右侧按钮组 -->
              <div class="flex items-center gap-2 pl-3 border-l border-gray-200">
                <button 
                  v-if="selectedFollowerRanges.length" 
                  @click.stop="clearFollowerRanges"
                  class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Clear all"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>

            <!-- 下拉面板 -->
            <div v-if="showFollowersDropdown" 
              class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg overflow-hidden"
            >
              <!-- 选项列表 -->
              <div class="max-h-60 overflow-y-auto py-1">
                <!-- 添加 Select All 选项 -->
                <div class="px-3 py-2 hover:bg-gray-50 cursor-pointer">
                  <label class="flex items-center cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllFollowers"
                      @change="toggleAllFollowers"
                      class="mr-2"
                    >
                    <span>Select All</span>
                  </label>
                </div>
                <!-- 其他选项 -->
                <div v-for="range in followerRanges.filter(r => r !== 'Select All')" 
                  :key="range"
                  @click="toggleFollowerRange(range)"
                  class="px-3 py-2 hover:bg-gray-50 cursor-pointer text-sm flex items-center space-x-2"
                  :class="{'text-blue-600': selectedFollowerRanges.includes(range)}"
                >
                  <span v-if="selectedFollowerRanges.includes(range)" class="text-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                  <span v-else class="w-4"></span>
                  <span>{{ range }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- GMV Dropdown  确定-->
          <div class="relative" v-click-outside="closeGMVDropdown">
            <div 
              @click="toggleGMVDropdown"
              class="filter-select flex items-center min-h-[45px] cursor-pointer px-3"
            >
              <!-- 已选标签区域 -->
              <div class="flex flex-wrap gap-1.5 flex-1 py-2">
                <template v-if="selectedGMVs.length">
                  <span v-for="range in selectedGMVs" 
                    :key="range" 
                    class="inline-flex items-center px-2 py-0.5 text-sm bg-blue-50 text-blue-700 rounded-md"
                  >
                    {{ range }}
                    <button 
                      @click.stop="removeGMV(range)" 
                      class="ml-1.5 text-blue-400 hover:text-blue-600 transition-colors"
                    >
                      ×
                    </button>
                  </span>
                </template>
                <span v-else class="text-gray-500">商品交易总额</span>
              </div>

              <!-- 右侧按钮组 -->
              <div class="flex items-center gap-2 pl-3 border-l border-gray-200">
                <button 
                  v-if="selectedGMVs.length" 
                  @click.stop="clearGMV"
                  class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Clear all"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>

            <!-- 下拉面板 -->
            <div v-if="showGMVDropdown" 
              class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg overflow-hidden"
            >
              <!-- 选项列表 -->
              <div class="max-h-60 overflow-y-auto py-1">
                <!-- 添加 Select All 选项 -->
                <div class="px-3 py-2 hover:bg-gray-50 cursor-pointer">
                  <label class="flex items-center cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllGMV"
                      @change="toggleAllGMV"
                      class="mr-2"
                    >
                    <span>Select All</span>
                  </label>
                </div>
                <!-- 其他选项 -->
                <div v-for="range in gmvRanges.filter(r => r !== 'Select All')" 
                  :key="range"
                  @click="toggleGMV(range)"
                  class="px-3 py-2 hover:bg-gray-50 cursor-pointer text-sm flex items-center space-x-2"
                  :class="{'text-blue-600': selectedGMVs.includes(range)}"
                >
                  <span v-if="selectedGMVs.includes(range)" class="text-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                  <span v-else class="w-4"></span>
                  <span>{{ range }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Gender Dropdown  确定-->
          <div class="relative" v-click-outside="closeGenderDropdown">
            <div 
              @click="toggleGenderDropdown"
              class="filter-select flex items-center min-h-[45px] cursor-pointer px-3"
            >
              <div class="flex flex-wrap gap-1.5 flex-1 py-2">
                <span v-if="!selectedGender" class="text-gray-500">性别</span>
                <span v-else class="text-gray-900">{{ selectedGender.charAt(0).toUpperCase() + selectedGender.slice(1) }}</span>
              </div>

              <!-- 右侧按钮组 -->
              <div class="flex items-center gap-2 pl-3 border-l border-gray-200">
                <button 
                  v-if="selectedGender" 
                  @click.stop="clearGender"
                  class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Clear all"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>

            <!-- 下拉面板 -->
            <div v-if="showGenderDropdown" 
              class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg overflow-hidden"
            >
              <div class="py-1">
                <div v-for="gender in genderOptions" 
                  :key="gender"
                  @click="selectGender(gender)"
                  class="px-3 py-2 hover:bg-gray-50 cursor-pointer text-sm flex items-center space-x-2"
                  :class="{'text-blue-600': selectedGender === gender}"
                >
                  <span v-if="selectedGender === gender" class="text-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                  <span v-else class="w-4"></span>
                  <span>{{ gender.charAt(0).toUpperCase() + gender.slice(1) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Creator Language Dropdown  确定-->
          <div class="relative" v-click-outside="closeLanguageDropdown">
            <div 
              @click="toggleLanguageDropdown"
              class="filter-select flex items-center min-h-[45px] cursor-pointer px-3"
            >
              <!-- 已选标签区域 -->
              <div class="flex flex-wrap gap-1.5 flex-1 py-2">
                <template v-if="selectedLanguages.length">
                  <span v-for="lang in selectedLanguages" 
                    :key="lang" 
                    class="inline-flex items-center px-2 py-0.5 text-sm bg-blue-50 text-blue-700 rounded-md"
                  >
                    {{ lang }}
                    <button 
                      @click.stop="removeLanguage(lang)" 
                      class="ml-1.5 text-blue-400 hover:text-blue-600 transition-colors"
                    >
                      ×
                    </button>
                  </span>
                </template>
                <span v-else class="text-gray-500">语言</span>
              </div>

              <!-- 右侧按钮组 -->
              <div class="flex items-center gap-2 pl-3 border-l border-gray-200">
                <button 
                  v-if="selectedLanguages.length" 
                  @click.stop="clearLanguages"
                  class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Clear all"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>

            <!-- 下拉面板 -->
            <div v-if="showLanguageDropdown" 
              class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg overflow-hidden"
            >
              <!-- 选项列表 -->
              <div class="max-h-60 overflow-y-auto py-1">
                <!-- 添加 Select All 选项 -->
                <div class="px-3 py-2 hover:bg-gray-50 cursor-pointer">
                  <label class="flex items-center cursor-pointer">
                    <input 
                      type="checkbox"
                      v-model="selectAllLanguages"
                      @change="toggleAllLanguages"
                      class="mr-2"
                    >
                    <span>Select All</span>
                  </label>
                </div>
                <!-- 其他选项 -->
                <div v-for="lang in languages.filter(l => l !== 'Select All')" 
                  :key="lang"
                  @click="toggleLanguage(lang)"
                  class="px-3 py-2 hover:bg-gray-50 cursor-pointer text-sm flex items-center space-x-2"
                  :class="{'text-blue-600': selectedLanguages.includes(lang)}"
                >
                  <span v-if="selectedLanguages.includes(lang)" class="text-blue-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                  <span v-else class="w-4"></span>
                  <span>{{ lang }}</span>
                </div>
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
                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              >
              <label for="withEmail" class="ml-2 text-sm text-gray-700">
                显示有设置邮箱的达人
              </label>
            </div>
          </div>

          <!-- Empty div for spacing -->
          <div></div>

          <!-- Reset Button -->
          <div class="flex justify-end">
            <button 
              @click="resetFilters"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-[#6366F1] bg-white border border-[#6366F1] rounded-md hover:bg-gray-50 transition-colors duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              重置条件
            </button>
          </div>
        </div>
      </div>

      <!-- Results Table -->
      <div class="relative w-full overflow-x-auto rounded-sm border border-gray-100 bg-white">
        <!-- 使用骨架屏替换原来的加载动画 -->
        <TableSkeleton v-if="loading" />
        
        <!-- 实际数据表格 -->
        <table v-else class="w-full text-sm">
          <!-- 表头 -->
          <thead>
            <tr class="border-b">
              <th class="p-3 text-left">头像昵称</th>
              <th class="p-3 text-left">简介</th>
              <th class="p-3 text-left">产品分类</th>
              <th class="p-3 text-left">粉丝数量</th>
              <th class="p-3 text-left">商品交易总额 (过去30天)</th>
              <th class="p-3 text-left">视频互动率 (过去30天)</th>
              <th class="p-3 text-left">链接</th>
              
            </tr>
          </thead>
          <!-- 表体 -->
          <tbody>
            <tr v-for="influencer in paginatedInfluencers" :key="influencer.handle" class="border-b hover:bg-gray-100">
              <td class="min-h-16 py-3 px-2 align-middle">
                <div class="flex items-center">
                  <img 
                    :src="influencer.avatar_url" 
                    :alt="influencer.handle"
                    class="w-10 h-10 rounded-full mr-3 object-cover"
                    @error="handleImageError"
                  >
                  <div>
                    <div>{{ influencer.handle }}</div>
                    <div v-if="influencer.email" class="text-xs text-gray-500">
                      {{ influencer.email }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="p-3">{{ influencer.bio }}</td>
              <td class="p-3">
                <div class="flex flex-wrap gap-1">
                  <span v-for="cat in influencer.product_category" :key="cat" 
                    class="px-2 py-1 text-xs bg-gray-100 rounded-md border">
                    {{ cat }}
                  </span>
                </div>
              </td>
              <td class="p-3">{{ formatFollow_table(influencer.follower_count) }}</td>
              <td class="p-3">{{ formatGMV_table(influencer.gmv_30d_num) }}</td>
              <td class="p-3">{{ formatVideo(influencer.avg_video_engagement_30d) }}</td>

              <!-- 添加profile,在后端结果返回中没有profileUrl这个选项，所以暂时不显示 -->
              <td class="p-3">
                <a 
                  :href= "`https://www.tiktok.com/@${influencer.handle}` "
                  target="_blank" 
                  class="text-blue-600 hover:text-blue-800 hover:underline"
                >
                  <img 
                    src="E:\project_03_01\BaiZenWeb\public\tik-tok.svg"
                    alt="TikTok Profile" 
                    class="inline-block w-10 h-10" 
                  />
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
          <!-- 显示结果数量，后端返回的接口有表明，所以可以进行优化掉 -->
           Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ currentPage * pageSize }} of {{ page_all_count }}
        </div>

        <!-- 分页按钮容器 - 居中 -->
        <div class="flex-1 flex justify-center">
          <div class="flex items-center space-x-1">
            <button 
              @click="prevPage"
              :disabled="currentPage === 1"
              class="px-2 py-1 text-gray-600 hover:text-blue-600"
            >
              <span class="text-sm">‹</span>
            </button>

            <!-- 页码按钮 -->
            <template v-for="page in displayPages" :key="page">
              <button 
                v-if="page !== '...'"
                @click="handlePageChange(page)"
                :class="[
                  'px-3 py-1 rounded',
                  currentPage === page ? 'bg-blue-500 text-white' : 'text-gray-600 hover:text-blue-600'
                ]"
              >
                {{ page }}
              </button>
              <span v-else class="px-2">...</span>
            </template>

            <!-- 下一页按钮 -->
            <button 
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="px-2 py-1 text-gray-600 hover:text-blue-600"
            >
              <span class="text-sm">›</span>
            </button>
          </div>
        </div>

        <!-- 空的 div 用于持布平衡 -->
        <div class="invisible text-sm text-gray-700">
          Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, filteredInfluencers.length) }} of {{ filteredInfluencers.length }}
        </div>
      </div>
    </div>

    <!-- 添加导出弹窗 确定-->
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

    <!-- 添加 loading 状态显示 -->
    <!-- <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div> -->

    <!-- 添加错误提示 -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { influencersAPI } from '../services/api'
import { InfluencerFilter } from '../services/Influencers'
import ExportModal from '../components/ExportModal.vue'
import TableSkeleton from '../components/TableSkeleton.vue'

export default {
  name: 'Influencers',
  components: {
    ExportModal,
    TableSkeleton
  },
  data() {
    return {
      // 发送搜索数据，对于数据的格式还需再更改
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      selectedCategories: [],  // 已经选择类别，用于Category Dropdown
      selectedGMVs: [],  // 已经的选择GMV，用于GMV Dropdown
      selectedFollowerRanges: [],  // 已经选择的选择粉丝数量，用于Follower Dropdown
      selectedLanguages: [],  // 已经选择语言，用于Language Dropdown
      selectedGender: '',  // 已经选择性别，用于Gender Dropdown
      onlyWithEmail: false,  // 是否只显示有邮箱的达人

      // 下拉框状态
      showCategoryDropdown: false, // 类别下拉框显示状态
      showGMVDropdown: false, // GMV下拉框显示状态
      showFollowersDropdown: false, // 粉丝数量下拉框显示状态
      showLanguageDropdown: false, // 语言下拉框显示状态
      showGenderDropdown: false, // 性别下拉框显示状态

      searchDebounceTimer: null, // 添加用于防抖的定时器
      debounceTimeout: null, // 用于存储setTimeout的ID
      
      // 添加 select all 的状态控制
      selectAllFollowers: false,
      selectAllGMV: false,
      selectAllLanguages: false,

      // 搜索框
      categorySearchQuery: '',  //  搜索类别，用于Category Dropdown
      gmvSearchQuery: '',
      followersSearchQuery: '',
      languageSearchQuery: '',

      // 后端返回的数据
      paginatedInfluencers: [],  // 分页后的数据
      page_count : 0,
      page_all_count : 0,

      displayedPages: [],  // 显示的页码，用于分页
      visibleRange: 2, // 显示当前页前后各2页
      totalPages: 0,  // 添加这个属性

      genderOptions: ['All','Male', 'Female'],  // 性别选项，用于Gender Dropdown
      // 类别选项
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
      // 粉丝数量选项
      followerRanges: [
        '0-20K',
        '20K-100K',
        '100K-1M',
        '1M+'
      ],
      // GMV选项
      gmvRanges: [
        '$0-$100',
        '$100-$1K',
        '$1K-$10K',
        '$10K+'
      ],
      // 语言选项
      languages: [
        
        'English',
        'Spanish',
      ],

      loading: false,
      error: null,

      showExportModal: false,  // 展示出弹窗
      total: 0,
      needRefresh: false,
      isFirstLoad: true,
      originalInfluencers: null,
      filters: {
        gender: '',
        categories: [],
        followers: [],
        languages: [],
        onlyWithEmail: false
      }
    }
  },
  computed: {

    //计算总页数
    computed_totalPages(){
      return Math.ceil(this.page_all_count/this.pageSize)
    },

    //计算显示的页码
    displayPages(){
      const pages_list = [];
      const startPage = Math.max(1, this.currentPage - this.visibleRange);
      const endPage = Math.min(this.computed_totalPages, this.currentPage + this.visibleRange);
      // 添加第一页和前面的省略号
      if (startPage > 1) {
        pages_list.push(1);
        if (startPage > 2) {
          pages_list.push('...');
        }
      }
      // 添加中间的页码
      for (let i = startPage; i <= endPage; i++) {
        pages_list.push(i);
      }
      // 添加最后一页和后面的省略号
      if (endPage < this.computed_totalPages) {
        if (endPage < this.computed_totalPages - 1) {
          pages_list.push('...');
        }
        pages_list.push(this.computed_totalPages);
      }
      return pages_list;
    },
    
    // 过滤出来还没有选中的类别,用于Category Dropdown
    filteredCategories() {
      if (!this.categorySearchQuery) return this.categories;
      const query = this.categorySearchQuery.toLowerCase();
      return this.categories.filter(category => 
        category.toLowerCase().includes(query)
      );
    },

    // 过滤出来还没有选中的GMV,用于GMV Dropdown
    filteredGMVRanges() {
      if (!this.gmvSearchQuery) return this.gmvRanges;
      const query = this.gmvSearchQuery.toLowerCase();
      return this.gmvRanges.filter(range => 
        range.toLowerCase().includes(query)
      );
    },

    // 过滤出来还没有选中的粉丝数量,用于Follower Dropdown
    filteredFollowerRanges() {
      if (!this.followersSearchQuery) return this.followerRanges;
      const query = this.followersSearchQuery.toLowerCase();
      return this.followerRanges.filter(range => 
        range.toLowerCase().includes(query)
      );
    },

    // 过滤出来还没有选中的语言,用于Language Dropdown
    filteredLanguages() {
      if (!this.languageSearchQuery) return this.languages;
      const query = this.languageSearchQuery.toLowerCase();
      return this.languages.filter(lang => 
        lang.toLowerCase().includes(query)
      );
    },

    //  选择所有类别，用于Category Dropdown
    selectAllCategories: {
      get() {
        return this.selectedCategories.length === this.categories.length;
      },
      set(value) {
        this.selectedCategories = value ? [...this.categories] : [];
      }
    },

    //  选择所有GMV，用于GMV Dropdown
    selectAllGMV: {
      get() {
        return this.selectedGMVs.length === this.gmvRanges.length;
      },
      set(value) {
        this.selectedGMVs = value ? [...this.gmvRanges] : [];
      }
    },

    //  选择所有粉丝数量，用于Follower Dropdown
    selectAllFollowers: {
      get() {
        return this.selectedFollowerRanges.length === this.followerRanges.length;
      },
      set(value) {
        this.selectedFollowerRanges = value ? [...this.followerRanges] : [];
      }
    },

    //  选择所有语言，用于Language Dropdown
    selectAllLanguages: {
      get() {
        return this.selectedLanguages.length === this.languages.length;
      },
      set(value) {
        this.selectedLanguages = value ? [...this.languages] : [];
      }
    },

    // 根据条件进行筛选,对结果进行筛选，后续需要将其优化掉，改成是向后端发送请求的
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

        // 性别匹配
        const genderMatch = !this.selectedGender || 
          influencer.gender === this.selectedGender;

        const languageMatch = this.selectedLanguages.length === 0 || 
          this.selectedLanguages.includes(influencer.language);

        const emailMatch = !this.onlyWithEmail || this.hasValidEmail(influencer.email);

        return searchMatch && categoryMatch && followersMatch && 
               gmvMatch && genderMatch && languageMatch && emailMatch;
      });
    },

    // 返回所有的页码，后端返回的数据中有页码表示，后续可以优化掉
    // totalPages() {
    //   return Math.ceil(this.total / this.pageSize);
    // },
    
    // 页码切片，后端返回的数据已经进行切片，每次请求的页码都是参数，所有不需要进行切片 -------------------------------------------------------------------
    // paginatedInfluencers() {
    //   const start = (this.currentPage - 1) * this.pageSize;
    //   const end = start + this.pageSize;
    //   return this.filteredInfluencers.slice(start, end);
    // },

    // 返回所有达人数据,目前搜索好像没用上，后续再进行考察一下
    influencersData() {
      return this.$store.state.influencers || []
    },

    // 过滤出来还没有选中的Category
    availableCategories() {
      const query = this.categorySearchQuery.toLowerCase();
      return this.categories.filter(category => 
        !this.selectedCategories.includes(category) && 
        category.toLowerCase().includes(query)
      );
    },

    // 过滤出来还没有选中的粉丝数量
    availableFollowerRanges() {
      const query = this.followersSearchQuery.toLowerCase();
      return this.followerRanges.filter(range => 
        !this.selectedFollowerRanges.includes(range) && 
        range.toLowerCase().includes(query)
      );
    },

    // 过滤出来还没选中的 GMV
    availableGMVRanges() {
      const query = this.gmvSearchQuery.toLowerCase();
      return this.gmvRanges.filter(range => 
        !this.selectedGMVs.includes(range) && 
        range.toLowerCase().includes(query)
      );
    },
    
    // 过滤出来还没有选中的语言
    availableLanguages() {
      const query = this.languageSearchQuery.toLowerCase();
      return this.languages.filter(lang => 
        !this.selectedLanguages.includes(lang) && 
        lang.toLowerCase().includes(query)
      );
    },

    influencers: {
      get() {
        return this.$store.state.influencers;
      },
      set(value) {
        this.$store.commit('setInfluencers', value);
      }
    },

    currentFilters: {
      get() {
        return this.$store.state.filters;
      },
      set(value) {
        this.$store.commit('setFilters', value);
      }
    }
  },
  
  methods: {

    // 对Follow字段进行处理
    formatFollow_table(gmvStr) {

      // 检查是否成功转换为数字
      if (isNaN(gmvStr)) return 'N/A';
      gmvStr = parseFloat(gmvStr)
      // 格式化为带有 k 或 m 后缀的字符串
      let formattedValue;
      if (gmvStr >= 1000000) {
        // 如果值大于等于一百万，则显示为 x.xxM
        formattedValue = (gmvStr / 1000000).toFixed(1) + 'M';
      } else if (gmvStr >= 1000) {
        // 如果值大于等于一千，则显示为 x.xxK
        formattedValue = (gmvStr / 1000).toFixed(1) + 'K';
      } else {
        // 否则直接显示原始值，保留两位小数
        formattedValue = gmvStr.toFixed(1);
      }
      return formattedValue;
    },

    // 对GMV字段进行处理
    formatGMV_table(gmvStr) {
      // 移除美元符号并将字符串转换为浮点数
      // const cleanedValue = parseFloat(gmvStr.replace('$', ''));
      const cleanedValue = gmvStr
      // 检查是否成功转换为数字
      if (isNaN(cleanedValue)) return 'N/A';

      // 格式化为带有 k 或 m 后缀的字符串
      let formattedValue;
      if (cleanedValue >= 1000000) {
        // 如果值大于等于一百万，则显示为 x.xxM
        formattedValue = '$' + (cleanedValue / 1000000).toFixed(2) + 'M';
      } else if (cleanedValue >= 999) {
        // 如果值大于等于一千，则显示为 x.xxK
        formattedValue = '$' + (cleanedValue / 1000).toFixed(2) + 'K';
      } else {
        // 否则直接显示原始值，保留两位小数
        formattedValue = '$' + cleanedValue.toFixed(2);
      }

      return formattedValue;
    },
    // 对 Video Engagement Rate (Last 30 Days) 字段进行处理
    formatVideo(gmvStr) {
      // 将字符串转换为数字并除以100，然后添加百分号
      const gmvNum = parseFloat(gmvStr);
      return isNaN(gmvNum) ? 'N/A' : (gmvNum / 100).toFixed(2) + '%';
    },

    // 处理页码变化
    handlePageChange(page){
      if(page !== this.currentPage && page > 0 && page <= this.computed_totalPages){
        this.currentPage = page;
        this.fetchInfluencers(); //刷新页面数据
      }
    },

    // 下一页
    nextPage(){
      if(this.currentPage < this.computed_totalPages){
        this.currentPage++;
        this.fetchInfluencers(); //刷新页面数据
      }
    },

    // 上一页
    prevPage(){
      if(this.currentPage > 1){
        this.currentPage--;
        this.fetchInfluencers(); //刷新页面数据
      }
    },

    // 在组件中使用
    async getchInfluencers() {
      try {
        // 创建 InfluencerFilter 实例
        const filter_condition = new InfluencerFilter({
          query: this.searchQuery,
          page: this.currentPage,
          perPage: this.pageSize,
          emailNotNull: this.onlyWithEmail,
          targetCategories: this.selectedCategories,
          targetFollowerCounts: this.selectedFollowerRanges,
          targetGMVs: this.selectedGMVs,
          targetGender: this.selectedGender,
          targetLanguages: this.selectedLanguages
        });
        this.loading = true
        console.log('当前的搜索条件是:', filter_condition.asRequestParams()); // 添加日志输出
        // 调用 API 获取数据
        const response = await influencersAPI.getInfluencers(filter_condition.asRequestParams());  // 传递扁平化对象
        
        console.log('response', response);

        // 更新组件状态或处理响应数据
        this.paginatedInfluencers = response.creators;  // 假设响应数据包含 data 字段
        console.log('paginatedInfluencers', this.paginatedInfluencers)
        this.page_count = response.totalPages
        this.page_all_count = response.totalCreators
        this.loading = false

      } catch (error) {
        console.error('Error fetching influencers:', error);
      }
    },

    matchFollowerRange(followers, range) {
      // 将 followers 字符串转换为数字(以千为单位)
      const value = followers.toLowerCase()
      let count
      if (value.includes('m')) {
        count = parseFloat(value) * 1000 // 将M转换为K
      } else if (value.includes('k')) {
        count = parseFloat(value)
      } else {
        count = parseFloat(value) / 1000 // 将原始数字转换为K
      }

      switch(range) {
        case '0-20K': return count <= 20
        case '20K-100K': return count > 20 && count <= 100
        case '100K-1M': return count > 100 && count <= 1000
        case '1M+': return count > 1000
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
      const femaleIndicators = ['she', 'her', 'girl', 'mom', 'mama', 'wife', 'sister', '👗', ''];
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

    // 打开类别弹窗绑定事件 用在Category Dropdown
    toggleCategoryDropdown() {
      this.showCategoryDropdown = !this.showCategoryDropdown;
    },

    // 关闭类别弹窗绑定事件 用在Category Dropdown
    closeCategoryDropdown() {
      this.showCategoryDropdown = false;
    },

    // 用于Category Dropdown,选择类别
    toggleAllCategories() {
      if (this.selectAllCategories) {
        this.selectedCategories = [...this.categories];
      } else {
        this.selectedCategories = [];
      }
    },

    // 清除类别 用在Category Dropdown
    clearCategories() {
      this.selectedCategories = [];
      this.selectAllCategories = false; // 确保全选复选框也被清除
    },

    // 改变下拉框是否显示下拉框状态，用在Follower Dropdown
    toggleFollowersDropdown() {
      this.showFollowersDropdown = !this.showFollowersDropdown;
    },

    // 关闭下拉框 用在Follower Dropdown
    closeFollowersDropdown() {
      this.showFollowersDropdown = false;
    },

    //  选择所有粉丝数量，用于Follower Dropdown
    toggleAllFollowers() {
      if (!this.selectAllFollowers) {
        // this.selectedFollowerRanges = [...this.followerRanges];
        this.selectedFollowerRanges = this.followerRanges.filter(range => range !== 'Select All');
        this.selectAllFollowers = true;
      } else {
        this.selectedFollowerRanges = [];
        this.selectAllFollowers = false;
      }
    },

    // 改变下拉框是否显示下拉框状态，用在GMV Dropdown
    toggleGMVDropdown() {
      this.showGMVDropdown = !this.showGMVDropdown;
    },

    // 关闭下拉框 用在GMV Dropdown
    closeGMVDropdown() {
      this.showGMVDropdown = false;
    },

    //  选择所有GMV，用于GMV Dropdown
    toggleAllGMV() {
      if (!this.selectAllGMV) {
        // this.selectedGMVs = [...this.gmvRanges];
        this.selectedGMVs = this.gmvRanges.filter(range => range !== 'Select All');
        this.selectAllGMV = true;
      } else {
        this.selectedGMVs = [];
        this.selectAllGMV = false;
      }
    },

    // 改变下拉框是否显示下拉框状态，用在Language Dropdown
    toggleLanguageDropdown() {
      this.showLanguageDropdown = !this.showLanguageDropdown;
    },

    // 关闭下拉框 用在Language Dropdown
    closeLanguageDropdown() {
      this.showLanguageDropdown = false;
    },

    //  选择所有语言，用于Language Dropdown
    toggleAllLanguages() {
      if (!this.selectAllLanguages) {
        // this.selectedLanguages = [...this.languages];
        this.selectedLanguages = this.languages.filter(lang => lang !== 'Select All');
        this.selectAllLanguages = true;
      } else {
        this.selectedLanguages = [];
        this.selectAllLanguages = false;
      }
    },



    // 重置搜索条件
    resetFilters() {
      this.searchQuery = "",
      this.currentPage = 1,
      this.pageSize = 10,
      this.onlyWithEmail = false,
      this.selectedCategories = [],
      this.selectedFollowerRanges = [],
      this.selectedGMVs = [],
      this.selectedGender = "",
      this.selectedLanguages = [],
      this.$store.dispatch('resetFilters');
    },

    handleCreateList(listData) {
      this.$store.dispatch('lists/addList', listData);
      this.$router.push('/lists');
    },

    async fetchInfluencers() {
      if (this.loading) return;
      
      try {
        this.loading = true;
        this.error = null;

        // 如果已经有原始数据，直接使用
        if (this.$store.state.originalInfluencers.length > 0) {
          this.applyCurrentFilters();
          return;
        }
        const filter_condition = new InfluencerFilter({
          query: this.searchQuery,
          page: this.currentPage,
          perPage: this.pageSize,
          emailNotNull: this.onlyWithEmail,
          targetCategories: this.selectedCategories,
          targetFollowerCounts: this.selectedFollowerRanges,
          targetGMVs: this.selectedGMVs,
          targetGender: this.selectedGender,
          targetLanguages: this.selectedLanguages
        });

        // 向后端发送请求，获取达人数据
        const response = await influencersAPI.getInfluencers(filter_condition.asRequestParams());

        // 更新组件状态或处理响应数据
        this.paginatedInfluencers = response.creators;  // 假设响应数据包含 data 字段
        console.log('paginatedInfluencers', this.paginatedInfluencers)
        this.page_count = response.totalPages
        this.page_all_count = response.totalCreators
        
        if (response.code === 0 && response.data) {
          const processedData = await Promise.all(response.data.map(async (item) => {
            // 解析 category
            let categories = [];
            try {
              if (item.category && item.category !== 'None') {
                const categoryArray = JSON.parse(item.category.replace(/'/g, '"'))
                categories = categoryArray.map(cat => cat.name)
              }
            } catch (e) {
              console.error('Error parsing category:', e)
              categories = []
            }

            // 修改邮箱处理逻辑
            let email = null;
            try {
              const emailResponse = await influencersAPI.getEmail(item.handle);
              if (emailResponse.code === 0 && emailResponse.data && emailResponse.data.length > 0) {
                const emailData = emailResponse.data[0].email;
                // 只有当邮箱不是占位符格式时才显示
                if (emailData && !emailData.includes('%XXXX@XXXX.com')) {
                  email = emailData;
                }
              }
            } catch (e) {
              console.warn('Warning: Failed to fetch email for', item.handle);
            }

            // 如果没有有效的邮箱，使用空字符串
            email = email || '';

            return {
              handle: item.handle,
              email: email,
              bio: item.nickname || '',
              categories: categories,
              followers: this.formatFollowers(item.follower_cnt),
              gmv: this.formatGMV(item.med_gmv_revenue, item.med_gmv_revenue_range),
              gender: item.top_follower_gender?.toLowerCase() || 'unknown',
              language: 'English',
              profile: `@${item.handle}`,
              profileUrl: `https://www.tiktok.com/@${item.handle}`,
              avatar: item.avatar || ''
            };
          }));
          
          if (!this.originalInfluencers) {
            this.originalInfluencers = [...processedData];
          }
          
          this.influencers = processedData;
          this.$store.commit('setInfluencers', processedData);
          this.total = response.total || 0;
        }
      } catch (error) {
        this.error = '加载数据失败，请稍后重试';
        console.error('Error fetching influencers:', error);
      } finally {
        this.loading = false;
      }
    },
    // 解析类别符串为数组
    parseCategories(categoryStr) {
      if (!categoryStr) return []
      try {
        // 果已经是数组，直接回
        if (Array.isArray(categoryStr)) {
          return categoryStr.map(cat => cat.name || cat).filter(Boolean)
        }
        
        // 如果是字符串尝试解析
        if (typeof categoryStr === 'string') {
          // 处理可能的特殊字符
          const cleanStr = categoryStr.replace(/[\u0000-\u0019]+/g, '')
          try {
            const categoryData = JSON.parse(cleanStr)
            if (Array.isArray(categoryData)) {
              return categoryData.map(cat => cat.name || cat).filter(Boolean)
            }
            return []
          } catch (e) {
            // 如果解析失败，尝试直接分割字符串
            return categoryStr.split(',').map(cat => cat.trim()).filter(Boolean)
          }
        }
        
        // 如果是其他类型，返回空数组
        return []
      } catch (e) {
        console.error('Failed to parse categories:', e, 'Original value:', categoryStr)
        return []
      }
    },
    // 格式化粉丝数
    formatFollowers(count) {
      if (!count) return '0'
      count = parseInt(count)
      if (count >= 1000000) {
        return `${(count / 1000000).toFixed(1)}M`
      } else if (count >= 1000) {
        return `${(count / 1000).toFixed(1)}K`
      }
      return count.toString()
    },
    // 格式化 GMV
    formatGMV(value, range) {
      // 如果有具体的 GMV 值
      if (value && !isNaN(value)) {
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD'
        }).format(value)
      }
      
      // 如果没有具体值但有范围，则返回范围
      if (range) {
        return range
      }
      
      // 如果既没有具体值也没有范围，返回默认值
      return '$0'
    },
    // 添加图片加载失败的处理方法
    handleImageError(e) {
      e.target.src = 'https://via.placeholder.com/40' // 设置默认头像
    },
    // 手动刷新数据的方法
    refreshData() {
      this.fetchInfluencers()
    },

    // 选择类别，用于Category Dropdown
    toggleCategory(category) {
      const index = this.selectedCategories.indexOf(category);
      if (index === -1) {
        this.selectedCategories.push(category);
      } else {
        this.selectedCategories.splice(index, 1);
      }
    },
    
    // 清除所选的类别 用在Category Dropdown
    removeCategory(category) {
      const index = this.selectedCategories.indexOf(category);
      if (index !== -1) {
        this.selectedCategories.splice(index, 1);
      }
    },

    // 选择粉丝数量，用于Follower Dropdown
    toggleFollowerRange(range) {
      const index = this.selectedFollowerRanges.indexOf(range);
      if (index === -1) {
        this.selectedFollowerRanges.push(range);
      } else {
        this.selectedFollowerRanges.splice(index, 1);
      }
      
    },

    // 清除所选的粉丝数量 用在Follower Dropdown
    removeFollowerRange(range) {
      const index = this.selectedFollowerRanges.indexOf(range);
      if (index !== -1) {
        this.selectedFollowerRanges.splice(index, 1);
      }
    },

    // 选择GMV，用于GMV Dropdown
    toggleGMV(range) {
      const index = this.selectedGMVs.indexOf(range);
      if (index === -1) {
        this.selectedGMVs.push(range);
      } else {
        this.selectedGMVs.splice(index, 1);
      }
    },

    // 清除所选的GMV 用在GMV Dropdown
    removeGMV(range) {
      const index = this.selectedGMVs.indexOf(range);
      if (index !== -1) {
        this.selectedGMVs.splice(index, 1);
      }
    },

    // 选择语言，用于Language Dropdown
    toggleLanguage(lang) {
      const index = this.selectedLanguages.indexOf(lang);
      if (index === -1) {
        this.selectedLanguages.push(lang);
      } else {
        this.selectedLanguages.splice(index, 1);
      }
    },

    // 清除所选的语言 用在Language Dropdown
    removeLanguage(lang) {
      const index = this.selectedLanguages.indexOf(lang);
      if (index !== -1) {
        this.selectedLanguages.splice(index, 1);
      }
    },

    // 清除粉丝数量,清除所有的 用在Follower Dropdown
    clearFollowerRanges() {
      this.selectedFollowerRanges = [];
      this.selectAllFollowers = false;
    },

    // 清除所选的GMV,清除所有的 用在GMV Dropdown
    clearGMV() {
      this.selectedGMVs = [];
      this.selectAllGMVs = false;
    },

    // 清除所选的语言 用在Language Dropdown
    clearLanguages() {
      this.selectedLanguages = [];
      this.selectAllLanguages = false;
    },

    // 改变下拉框是否显示下拉框状态，用在Gender Dropdown
    toggleGenderDropdown() {
      this.showGenderDropdown = !this.showGenderDropdown;
    },

    // 关闭下拉框 用在Gender Dropdown
    closeGenderDropdown() {
      this.showGenderDropdown = false;
    },

    // 选择性别，用于Gender Dropdown
    selectGender(gender) {
      // this.selectedGender = gender;
      // this.closeGenderDropdown();
      if(gender === 'Select All') {
        this.selectedGender = '';
      } else {
        this.selectedGender = gender;
      }
      this.closeGenderDropdown();
    },

    // 清除所选的性别 用在Gender Dropdown
    clearGender() {
      this.selectedGender = '';
      this.closeGenderDropdown();
    },


    async exportResults() {
      const exportData = {
        name: `Exported List ${new Date().toLocaleString()}`,
        data: this.filteredInfluencers,
        createdAt: new Date().toISOString(),
        filters: {
          categories: this.selectedCategories,
          followers: this.selectedFollowerRanges,
          gmv: this.selectedGMVs,
          languages: this.selectedLanguages,
          gender: this.selectedGender,
          searchQuery: this.searchQuery
        }
      };

      try {
        await this.$store.dispatch('lists/addList', exportData);
        this.showExportModal = false; // 关闭导出模态框
        this.$router.push('/lists'); // 导出成功后跳转到列表页面
      } catch (error) {
        console.error('Export failed:', error);
        // 可以添加错误提示
      }
    },

    // 应用当前过滤器，从原始数据开始过滤
    applyCurrentFilters() {
      // 从原始数据开始过滤
      let filtered = [...this.$store.state.originalInfluencers];

      const filters = this.currentFilters;
      
      if (filters.gender) {
        filtered = filtered.filter(inf => inf.gender === filters.gender);
      }
      // ... 其他过滤逻辑

      this.$store.commit('setInfluencers', filtered);
    }
  },

  // 添加 watch 来监听所有搜索条件的变化
  watch: {
    // 监听搜索关键词
    // searchQuery() {
    //   this.currentPage = 1;
    //   this.getchInfluencers();
    // },

    searchQuery: function (newValue) {
      // 清除之前的定时器
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
      }

      // 设置新的定时器，在用户停止输入2秒后触发
      this.debounceTimeout = setTimeout(() => {
        // 在这里放置你想执行的逻辑，例如发起API请求或更新过滤条件
        this.currentPage = 1;
        this.getchInfluencers();
        // 执行你的业务逻辑...
      }, 2000); // 2000 毫秒 = 2 秒
    },

    // 监听分类选择
    selectedCategories: {
      handler() {
        this.currentPage = 1;
        this.getchInfluencers();
      },
      deep: true
    },

    // 监听粉丝数范围
    selectedFollowerRanges: {
      handler() {
        this.currentPage = 1;
        this.getchInfluencers();
      },
      deep: true
    },

    // 监听GMV范围
    selectedGMVs: {
      handler() {
        this.currentPage = 1;
        this.getchInfluencers();
      },
      deep: true
    },

    // 监听语言选择
    selectedLanguages: {
      handler() {
        this.currentPage = 1;
        this.getchInfluencers();
      },
      deep: true
    },

    // 监听性别选择
    selectedGender() {
      this.currentPage = 1;
      this.getchInfluencers();
    },

    // 监听邮箱筛选
    onlyWithEmail() {
      this.currentPage = 1;
      this.getchInfluencers();
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
  created() {
    this.fetchInfluencers();
  },
  activated() {
    // 如果不是从 Lists 页面返回，重置过滤器
    if (!this.$route.query.keepFilters) {
      this.resetFilters();
    }
  },
  deactivated() {
    // 组件被缓存时的处理
  },
  beforeRouteLeave(to, from, next) {
    // 如果不是去 Lists 页面，重置过滤器
    if (to.name !== 'Lists') {
      this.resetFilters();
    }
    next();
  },
  beforeDestroy() {
    if (this.debounceTimeout) {
      clearTimeout(this.debounceTimeout);
    }
  },
}
</script>

<style scoped>
.search-input {
  @apply flex min-h-10 w-full rounded-md border border-gray-300 bg-white px-4 py-3 text-[16px] 
  leading-[19.2px] !ring-0 transition-all;
}

.search-input::placeholder {
  @apply text-gray-500;
}

.filter-select {
  @apply flex w-full rounded-md border border-gray-300 bg-white 
  text-sm transition-all hover:border-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500;
}

/* 自定义滚动条样式 */
.max-h-60 {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E1 #F1F5F9;
}

.max-h-60::-webkit-scrollbar {
  width: 6px;
}

.max-h-60::-webkit-scrollbar-track {
  background: #F1F5F9;
}

.max-h-60::-webkit-scrollbar-thumb {
  background-color: #CBD5E1;
  border-radius: 3px;
}

/* 标签动画 */
.filter-select .inline-flex {
  @apply transition-all duration-200 ease-in-out;
}

/* 下拉面板动画 */
.absolute {
  @apply transition-all duration-200 ease-in-out;
}

.export-button {
  @apply py-2.5 px-6 text-sm leading-[19.2px] inline-flex items-center justify-center whitespace-nowrap 
  rounded-[10px] transition-all !ring-0 !ring-offset-0 border bg-transparent 
  border-gray-400 hover:bg-gray-100 text-blue-500;
}

.info-button {
  @apply p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-all;
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

/* 确保容器足够空间 */
.view-count-dropdown .flex {
  padding-right: 3rem;  /* 增加右内边距，图片留出空间 */
}


/* 加载状态样式 */

.search-input:disabled {

@apply opacity-75;

}


.filter-select.cursor-not-allowed {

@apply opacity-75;

}


/* 加载动画容器 */

.loading-overlay {

@apply absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 z-10;

}


/* 加载动画 */

.loading-spinner {

@apply animate-spin rounded-full border-4 border-gray-200;

border-top-color: #6366F1;

}


/* 禁用状态的下拉框 */

.filter-select.cursor-not-allowed:hover {

@apply border-gray-300;

}


/* 禁用状态的按钮 */

button:disabled {

@apply opacity-50 cursor-not-allowed;

}

.filter-tags {
  @apply flex flex-wrap gap-2;
}

.filter-tag {
  @apply inline-flex items-center px-2 py-1 rounded-md bg-blue-50 text-blue-700 text-sm;
}

.filter-tag button {
  @apply ml-1 text-blue-500 hover:text-blue-700;
}

.dropdown-item {
  @apply px-4 py-2 hover:bg-gray-50 cursor-pointer rounded-md;
}

.dropdown-item.selected {
  @apply text-blue-600;
}
</style> 