import { createStore } from 'vuex'
import router from '../router'

export default createStore({
  state: {
    influencers: [],
    lists: []
  },
  mutations: {
    setInfluencers(state, data) {
      state.influencers = data
    },
    resetInfluencers(state) {
      state.influencers = [];
    },
    ADD_LIST(state, list) {
      const newList = {
        id: Date.now(),
        name: list.name,
        type: list.type || 'Default',
        description: list.description || '',
        creators: Array.isArray(list.creators) ? list.creators : [],
        createdOn: new Date().toLocaleString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false
        })
      };
      state.lists.push(newList);
    },
    UPDATE_LIST(state, updatedList) {
      const index = state.lists.findIndex(l => l.id === updatedList.id);
      if (index !== -1) {
        state.lists.splice(index, 1, updatedList);
      }
    }
  },
  actions: {
    setInfluencers({ commit }, data) {
      commit('setInfluencers', data);
    },
    resetInfluencers({ commit }) {
      commit('resetInfluencers');
    },
    
    async createList({ commit }, listData) {
      try {
        const newList = {
          id: Date.now(),
          ...listData,
          createdOn: new Date().toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
          })
        };
        
        commit('ADD_LIST', newList);
        return newList;
      } catch (error) {
        console.error('Failed to create list:', error);
        throw error;
      }
    },

    async updateList({ commit }, list) {
      try {
        const updatedList = {
          ...list,
          updatedOn: new Date().toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
          })
        };
        
        commit('UPDATE_LIST', updatedList);
        return updatedList;
      } catch (error) {
        console.error('Failed to update list:', error);
        throw error;
      }
    }
  },
  getters: {
    getLists: state => state.lists,
    getInfluencers: state => state.influencers
  }
}) 