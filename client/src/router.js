import { createRouter, createWebHistory } from 'vue-router';
import AppHome from './views/AppHome.vue';
import AppAbout from './views/AppAbout.vue';
import AuthPage from './views/AuthPage.vue';
import Login from './components/LogIn.vue';
import Signup from './components/SignUp.vue';


const routes = [
  { path: '/home', component: AppHome },
  { path: '/about', component: AppAbout },
  {
    path: '/',
    component: AuthPage,
    children: [
      { path: 'signup', component: Signup },
      { path: 'login', component: Login },
    ],
  },
  // 添加其他路由
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;