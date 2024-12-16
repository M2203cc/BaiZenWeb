<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-[500px]">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Create New List</h3>
        <button @click="close" class="text-gray-500 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">List Name</label>
          <input 
            v-model="formData.name"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">List Type</label>
          <select 
            v-model="formData.type"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            <option value="Filters">Filters</option>
            <option value="Manual">Manual</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea 
            v-model="formData.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
            readonly
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Created On</label>
          <input 
            :value="formattedDate"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
            readonly
          >
        </div>
      </div>

      <div class="mt-6 flex justify-end">
        <button 
          @click="close"
          class="mr-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
        >
          Cancel
        </button>
        <button 
          @click="handleCreate"
          class="px-4 py-2 text-sm text-white bg-primary-600 hover:bg-primary-700 rounded-md"
        >
          Create
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    show: Boolean,
    filters: Object,
    influencers: Array
  },
  data() {
    return {
      formData: {
        name: '',
        type: 'Filters',
        description: '',
        createdOn: new Date()
      }
    }
  },
  computed: {
    formattedDate() {
      const date = this.formData.createdOn;
      return date.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      });
    },
    filterDescription() {
      const filters = this.filters;
      const parts = [];

      if (filters.categories.length) {
        parts.push(`Categories: ${filters.categories.join(', ')}`);
      }
      if (filters.gmv.length) {
        parts.push(`GMV: ${filters.gmv.join(', ')}`);
      }
      if (filters.followers.length) {
        parts.push(`Followers: ${filters.followers.join(', ')}`);
      }
      if (filters.gender) {
        parts.push(`Gender: ${filters.gender}`);
      }
      if (filters.languages.length) {
        parts.push(`Languages: ${filters.languages.join(', ')}`);
      }
      if (filters.onlyWithEmail) {
        parts.push('Only with email');
      }

      return parts.join(' | ') || 'No filters applied';
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.formData.description = this.filterDescription;
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
      this.formData.name = '';
      this.formData.type = 'Filters';
    },
    async handleCreate() {
      try {
        const creators = this.influencers.map(inf => inf.handle);
        
        this.$store.dispatch('setInfluencers', this.influencers);
        
        const listData = {
          name: this.formData.name,
          type: 'Filters',
          description: `Gender: ${this.filters.gender || 'All'}\n${this.getFiltersDescription()}`,
          creators: creators
        }
        
        await this.$store.dispatch('createList', listData)
        this.$emit('close')
        this.$router.push('/lists')
      } catch (error) {
        console.error('Failed to create list:', error)
      }
    },
    
    getFiltersDescription() {
      const descriptions = []
      if (this.filters.categories?.length) {
        descriptions.push(`Categories: ${this.filters.categories.join(', ')}`)
      }
      if (this.filters.followers?.length) {
        descriptions.push(`Followers: ${this.filters.followers.join(', ')}`)
      }
      if (this.filters.languages?.length) {
        descriptions.push(`Languages: ${this.filters.languages.join(', ')}`)
      }
      return descriptions.join('\n')
    }
  }
}
</script> 