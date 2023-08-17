import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 导入路由配置
import store from './store'; // 导入 Vuex store


const app = createApp(App);
app.use(router); // 将路由实例添加到 app 实例

app.use(store); // 使用 Vuex store
app.mount('#app');