<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <!-- 背景遮罩 -->
    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>

    <!-- 模态框内容 -->
    <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
      <div class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
        <!-- 模态框头部 -->
        <div class="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
              <h3 class="text-lg font-semibold leading-6 text-gray-900 mb-4">
                Create New List
              </h3>
              
              <!-- 表单内容 -->
              <div class="mt-2">
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    List Name
                  </label>
                  <input 
                    v-model="formData.name"
                    type="text"
                    class="w-full rounded-md border border-gray-300 px-3 py-2"
                    placeholder="Enter list name"
                  />
                </div>

                <!-- 选中的创建者列表 -->
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Selected Creators ({{ influencers.length }})
                  </label>
                  <div class="max-h-40 overflow-y-auto border border-gray-200 rounded-md p-2">
                    <div 
                      v-for="creator in influencers" 
                      :key="creator"
                      class="py-1 px-2 text-sm text-gray-700"
                    >
                      {{ creator }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 模态框底部按钮 -->
        <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
          <button
            type="button"
            class="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 sm:ml-3 sm:w-auto"
            @click="handleCreate"
          >
            Create List
          </button>
          <button
            type="button"
            class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
            @click="close"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExportModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
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
      this.$emit('close')
      this.formData.name = ''
    },
    async handleCreate() {
      try {
        if (!this.formData.name) {
          alert('Please enter a list name')
          return
        }

        const listData = {
          name: this.formData.name,
          type: 'Video List',
          description: 'Created from videos page',
          creators: this.influencers
        }
        
        await this.$store.dispatch('createList', listData)
        this.close()
        this.$router.push({ 
          path: '/lists',
          query: { keepFilters: 'true' }
        })
      } catch (error) {
        console.error('Failed to create list:', error)
        alert('Failed to create list. Please try again.')
      }
    }
  }
}
</script>

<style scoped>
/* 自定义滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 