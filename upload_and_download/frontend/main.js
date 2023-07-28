import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

createApp(App).use(ElementPlus).mount('#app')

// import { createApp } from 'vue'
// import App from './App.vue'
// import ElementPlus from 'element-plus'
// import 'element-plus/dist/index.css'
// import router from './router/index.js'  //引入定义好的路由

import CryptoJS from 'crypto-js';
Vue.prototype.CryptoJS = CryptoJS;


// createApp(App).use(ElementPlus).use(router).mount('#app') //使用路由

