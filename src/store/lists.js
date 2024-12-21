export default {
  namespaced: true,
  
  state: {
    lists: []
  },
  
  mutations: {
    ADD_LIST(state, list) {
      state.lists.push(list);
    },
    SET_LISTS(state, lists) {
      state.lists = lists;
    }
  },
  
  actions: {
    addList({ commit, state }, list) {
      // 修改这里，使用当前 state 中的 lists
      const currentLists = [...state.lists, list];
      localStorage.setItem('influencer_lists', JSON.stringify(currentLists));
      commit('ADD_LIST', list);
    }
  },
  
  getters: {
    getAllLists: state => state.lists
  }
}; 