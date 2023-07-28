// 该文件是整个项目的入口文件

// 引入vue
import axios from 'axios'
import Vue from 'vue'
import App from './App.vue'
import Router from 'vue-router'
import ElementUI from 'element-ui'; // 引入 Element UI
import 'element-ui/lib/theme-chalk/index.css';

// 引入路由器（一个应用有一个就足够了）
import router from './router'

Vue.config.productionTip = false

Vue.use(Router)
Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.prototype.$axios = axios

new Vue({
  render: h => h(App),
  router:router,
}).$mount('#app')