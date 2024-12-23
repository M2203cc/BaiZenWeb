<template>
  <div class="px-8 py-4">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">My Lists</h2>
    
    <!-- Lists Table -->
    <div v-if="!selectedList" class="relative overflow-x-auto rounded-sm border border-secondary-100 bg-white">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b">
            <th class="p-3 text-left">Name</th>
            <th class="p-3 text-left">Creators</th>
            <th class="p-3 text-left">Type</th>
            <th class="p-3 text-left">Description</th>
            <th class="p-3 text-left">Created Time</th>
            <th class="p-3 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="list in lists" :key="list.name" class="border-b hover:bg-secondary-100">
            <td class="p-3">{{ list.name }}</td>
            <td class="p-3">{{ list.creators?.length || 0 }}</td>
            <td class="p-3">{{ list.type }}</td>
            <td class="p-3">{{ list.description }}</td>
            <td class="p-3">{{ list.createdOn }}</td>
            <td class="p-3">
              <button 
                @click="viewList(list)"
                class="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-gray-700"
              >
                详情
              </button>
              <button 
                @click="exportToCsv(list)"
                class="ml-2 inline-flex items-center px-4 py-2 bg-green-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-green-500"
              >
                导出为csv文件
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- List Detail View -->
    <div v-else class="bg-white rounded-lg p-6 border border-secondary-100">
      <!-- Header with back button -->
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-xl font-semibold">{{ selectedList.name }}</h3>
        <button 
          @click="selectedList = null"
          class="text-gray-600 hover:text-gray-800 px-3 py-1 rounded hover:bg-gray-100"
        >
          返回上一级
        </button>
      </div>

      <!-- List Details -->
      <div class="space-y-4">
        <div>
          <div class="text-gray-600">List Type</div>
          <div class="text-gray-900">{{ selectedList.type }}</div>
        </div>

        <div>
          <div class="text-gray-600">Description</div>
          <div class="text-gray-900">{{ selectedList.description }}</div>
        </div>

        <div>
          <div class="text-gray-600">Created On</div>
          <div class="text-gray-900">{{ selectedList.createdOn }}</div>
        </div>

        <div>
          <div class="text-gray-600">
            Creators ({{ selectedList.creators?.length || 0 }} total)
          </div>
          
          <!-- Creators List -->
          <div class="mt-2">
            <ul class="space-y-2">
              <li v-for="(creator, index) in selectedList.creators" 
                  :key="index"
                  class="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <div class="flex items-center space-x-4">
                  <span class="text-gray-500">{{ index + 1 }}.</span>
                  <a 
                    :href="`https://www.tiktok.com/@${creator}`"
                    target="_blank"
                    class="text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    {{ creator }}
                  </a>
                </div>
                <button 
                  @click="removeCreator(index)"
                  class="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-50"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    lists() {
      return this.$store.state.lists || [];
    },
    allInfluencers() {
      return this.$store.state.influencers || [];
    }
  },
  data() {
    return {
      selectedList: null,
      notFoundCount: 0
    }
  },
  methods: {
    viewList(list) {
      this.selectedList = list;
    },
    async removeCreator(index) {
      if (this.selectedList) {
        const updatedCreators = [...this.selectedList.creators];
        updatedCreators.splice(index, 1);
        
        const updatedList = {
          ...this.selectedList,
          creators: updatedCreators
        };
        
        try {
          await this.$store.dispatch('updateList', updatedList);
          this.selectedList = updatedList;
        } catch (error) {
          console.error('Failed to update list:', error);
        }
      }
    },
    exportToCsv(list) {
      // 准备CSV数据
      const csvData = [
        ['序号', '达人名称', 'URL'] // CSV 头部
      ];

      // 添加数据行
      list.creators?.forEach((creator, index) => {
        csvData.push([
          index + 1,
          creator,
          `https://www.tiktok.com/@${creator}`
        ]);
      });

      // 将数据转换为CSV格式
      const csvContent = csvData.map(row => row.join(',')).join('\n');

      // 创建Blob对象
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

      // 创建下载链接
      const link = document.createElement('a');
      if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `${list.name}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  }
}
</script>

<style scoped>
.creator-list {
  @apply mt-4 space-y-2;
}

.creator-item {
  @apply flex items-center justify-between py-2 px-3 bg-white rounded-lg hover:bg-gray-50;
}

.creator-number {
  @apply text-gray-500;
}

.creator-handle {
  @apply text-gray-900;
}

.delete-button {
  @apply text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-50;
}
</style>