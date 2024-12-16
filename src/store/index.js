import { createStore } from 'vuex'

export default createStore({
  state: {
    lists: [],
    influencers: []
  },
  mutations: {
    ADD_LIST(state, list) {
      state.lists.push(list)
    },
    SET_INFLUENCERS(state, influencers) {
      state.influencers = influencers
    }
  },
  actions: {
    createList({ commit }, listData) {
      const newList = {
        id: Date.now(),
        name: listData.name,
        type: listData.type || 'Filters',
        description: listData.description || '',
        creators: listData.creators || [],
        creatorUrls: listData.creatorUrls || {},
        createdOn: new Date().toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      }
      commit('ADD_LIST', newList)
      return newList
    },
    setInfluencers({ commit }, influencers) {
      commit('SET_INFLUENCERS', influencers)
    }
  }
}) 