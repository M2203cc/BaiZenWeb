<template>
  <div class="px-8 py-4">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">{{ list.name }}</h2>
      <button 
        @click="$router.push('/lists')"
        class="text-primary-600 hover:underline flex items-center gap-2"
      >
        <span class="text-sm">‹</span>
        Back to Lists
      </button>
    </div>

    <div class="mb-6 space-y-4">
      <div>
        <h3 class="text-sm font-medium text-gray-700">List Type</h3>
        <p class="mt-1">{{ list.type }}</p>
      </div>
      
      <div>
        <h3 class="text-sm font-medium text-gray-700">Description</h3>
        <p class="mt-1">{{ list.description }}</p>
      </div>
      
      <div>
        <h3 class="text-sm font-medium text-gray-700">Created On</h3>
        <p class="mt-1">{{ list.createdOn }}</p>
      </div>
    </div>

    <div class="relative overflow-x-auto rounded-sm border border-secondary-100 bg-white">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b">
            <th class="p-3 text-left">Handle</th>
            <th class="p-3 text-left">Bio</th>
            <th class="p-3 text-left">Product Category</th>
            <th class="p-3 text-left">Follower Count</th>
            <th class="p-3 text-left">GMV (Last 30 Days)</th>
            <th class="p-3 text-left">Email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="influencer in list.influencers" :key="influencer.handle" class="border-b hover:bg-secondary-100">
            <td class="p-3">
              <div class="flex items-center">
                <img 
                  :src="`https://api.dicebear.com/7.x/pixel-art/svg?seed=${influencer.handle}`" 
                  class="w-10 h-10 rounded-full mr-3 bg-gray-100 object-cover"
                  :alt="influencer.handle"
                />
                <div>{{ influencer.handle }}</div>
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
            <td class="p-3">{{ influencer.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    list() {
      const id = parseInt(this.$route.params.id);
      return this.$store.state.lists.find(list => list.id === id) || {
        name: '',
        type: '',
        description: '',
        createdOn: '',
        influencers: []
      };
    }
  }
}
</script> 