<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-[500px]">
      <!-- 标题和关闭按钮 -->
      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center gap-2">
          <h3 class="text-xl font-semibold">Add Creators to List</h3>
          <span class="text-sm text-gray-500">({{ influencers.length }} creators)</span>
        </div>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 创作者列表 -->
      <div class="space-y-2 max-h-[300px] overflow-y-auto custom-scrollbar">
        <div 
          v-for="creator in influencers" 
          :key="creator.id"
          class="flex items-center gap-2 p-2 bg-[#F8F9FA] rounded-md"
        >
          <img 
            :src="creator.avatar" 
            :alt="creator.name"
            class="w-8 h-8 rounded-full object-cover"
          >
          <span class="text-sm text-gray-900">{{ creator.name }}</span>
        </div>
      </div>

      <!-- 输入框 -->
      <div class="mt-4">
        <input
          v-model="listName"
          type="text"
          placeholder="Enter list name"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-[#27AE60] focus:border-[#27AE60]"
        />
      </div>

      <!-- 底部按钮 -->
      <div class="mt-6 flex justify-end gap-3">
        <button 
          @click="$emit('close')"
          class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
        >
          Cancel
        </button>
        <button 
          @click="handleExport"
          class="px-4 py-2 bg-[#27AE60] text-white rounded-md hover:bg-[#219653] text-sm"
          :disabled="!listName"
        >
          Add to List
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  influencers: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['close', 'export'])
const listName = ref('')

const handleExport = () => {
  if (!listName.value) return
  emit('export', { creators: props.influencers, name: listName.value })
  listName.value = ''
  emit('close')
}
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #CBD5E1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #94A3B8;
}
</style> 