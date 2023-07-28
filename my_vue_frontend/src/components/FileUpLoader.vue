<template>
  <el-container>
    <el-header><sub_Header></sub_Header></el-header>
    <el-container>
      <el-aside><Left></Left></el-aside>
      <el-main><Right></Right></el-main>
    </el-container>
  </el-container>
</template>

<script>
import { Container, Header, Aside, Main } from 'element-ui';
import Right from '../sub_components/Right';
import Left from '../sub_components/Left';
import sub_Header from '../sub_components/sub_Header';

export default {
  name: "FileUpLoader",
  components: {
    'el-container': Container, // 注册 Element UI 组件
    'el-header': Header,
    'el-aside': Aside,
    'el-main': Main,
    sub_Header,
    Right,
    Left
  },
  created() {
    if (localStorage.getItem('uid') === '' || localStorage.getItem('uid') === undefined) {
      const confirmed = window.confirm('您还未登陆/或者登陆已过期');
      if (confirmed) {
        this.$router.push({ path: '/' });
      } else {
        this.$router.push({ path: '/' });
      }
    }
  },
  methods: {

  }
}
</script>

<style scoped>
 .el-header{
   width: 100%;
   box-shadow:  0 2px 6px 0 rgba(0,0,0,.05);

 }
  .el-container{
    height: 100%;

  }

.el-aside{
  background-color:  #f7f7f7;
  max-width: 194px;

}
.el-main{
  position: absolute;
    top: 229px;
    right: 0px;
  height: calc(100% - 62px);
  max-width: calc(95% - 192px);
}



</style>
