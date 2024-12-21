<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-[500px]">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Create a new List</h3>
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
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <button 
          @click="close"
          class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
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
    influencers: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      formData: {
        name: ''
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
      this.formData.name = '';
    },
    async handleCreate() {
      try {
        if (!this.formData.name) {
          alert('Please enter a list name');
          return;
        }

        const creators = this.influencers.map(inf => inf.handle);
        
        const listData = {
          name: this.formData.name,
          type: 'Video List',
          description: 'Created from videos page',
          creators: creators
        };
        
        await this.$store.dispatch('createList', listData);
        this.close();
        this.$router.push({ 
          path: '/lists',
          query: { keepFilters: 'true' }
        });
      } catch (error) {
        console.error('Failed to create list:', error);
        alert('Failed to create list. Please try again.');
      }
    }
  },
  watch: {
    show(newVal) {
      if (!newVal) {
        this.formData.name = '';
      }
    }
  }
}
</script> 