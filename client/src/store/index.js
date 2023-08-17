import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      token: '' // 或其他状态
    };
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    }
    // 其他 mutations
  }
  // 其他配置项，如 actions、getters 等
});

export default store;
