<template>
  
    <div class="row">
      <div class="col-xs-offset-2 col-xs-8">
        <div class="page-header"><h1>中传放心传</h1></div>
      </div>
    </div>

    <div class="row">
      <div class="col-xs-2 col-xs-offset-2">
        
          <router-view></router-view>
        
      </div>
          </div>
    <Footer />
</template>

<script>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Footer from './components/AppFooter.vue';

export default {
  
  name: 'App',
  components: {
    Footer,
  },
  setup() {
    const store = useStore();
    const isLoggedIn = computed(() => store.state.token !== '');

    onMounted(() => {
      const savedToken = sessionStorage.getItem('token');
      if (savedToken) {
        store.commit('setToken', savedToken);
      }
    });

    return {
      isLoggedIn
    };
  }
};
</script>
