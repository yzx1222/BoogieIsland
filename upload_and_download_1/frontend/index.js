import Vue from 'vue'
import Router from 'vue-router'

import Fileupload from '@/components/Fileupload'
import FileDownload from '@/components/FileDownload'
 
Vue.use(Router)
 
export default new Router({
  routes: [
    {
      path: '/Fileupload',
      name: 'Fileupload',
      component: Fileupload
    },
    {
      path: '/FileDownload',
      name: 'FileDownload',
      component: FileDownload
    }
  ],
  mode: 'history'
})
