// 该文件专门用于创建整个应用的路由器
import Router from 'vue-router'


// 引入组件
import LoginForm from '../components/LoginForm'
import SignupForm from '../components/SignupForm'

// 创建并暴露一个路由器
export default new Router({
    routes:[
        {
            path:'/LoginForm',
            component:LoginForm
        },
        {
            path:'/SignupForm',
            component:SignupForm
        }
    ]
})



