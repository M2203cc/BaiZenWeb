<template>
  <!-- No changes to template section -->
</template>

<script>
import { influencersAPI } from '@/services/api'
import ExportModal from '../components/ExportModal.vue'

export default {
  name: 'Influencers',
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
      showGenderDropdown: false,
      
      categorySearchQuery: '',
      gmvSearchQuery: '',
      followersSearchQuery: '',
      languageSearchQuery: '',
      
      selectedCategories: [],
      selectedGMVs: [],
      selectedFollowerRanges: [],
      selectedLanguages: [],
      selectedGender: '',
      genderOptions: ['male', 'female'],
      
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

      loading: false,
      error: null,

      currentPage: 1,
      pageSize: 12,
      showExportModal: false,
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
    // No changes to computed section
  },
  methods: {
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

        const response = await influencersAPI.getInfluencers(this.currentPage, this.pageSize);
        
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
    // No changes to other methods
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
  }
}
</script>

<style scoped>
/* No changes to style section */
</style> 