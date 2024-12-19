import { createStore } from 'vuex'

export default createStore({
  state: {
    influencers: []
  },
  mutations: {
    setInfluencers(state, data) {
      state.influencers = data
    }
  },
  actions: {
    // 如果需要异步操作可以添加 actions
  }
}) 