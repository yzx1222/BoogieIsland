<template>
  <el-card class="box-card">
    <a href="javascript:void(0)"  class="nav first">网盘</a>
    <a href="javascript:void(0)"  class="nav"></a>
    <a href="javascript:void(0)"  class="nav"></a>
    <span style="float: right;" class="name">{{name}}</span>
      <el-dropdown class="avatar">
  <span class="el-dropdown-link">
     <img src="../assets/avatar.svg" alt=""  slot="reference" >

  </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>设置</el-dropdown-item>
        <el-dropdown-item divided ><a @click="loginout">退出登陆</a></el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>


  </el-card>
</template>

<script>
import { Card, Dropdown, DropdownMenu, DropdownItem} from 'element-ui';

    export default {
        name: "Header",
        components: {
        'el-card': Card,
        'el-dropdown': Dropdown,
        'el-dropdown-menu': DropdownMenu, 
        'el-dropdown-item': DropdownItem, 
      },
      data(){
        return{
        name:'未登录'

        }
      },
      created(){
    this.name=localStorage.getItem('name')

      },
      methods:{
        loginout(){
          localStorage.setItem('uid','')
          this.$router.push({path: '/'})
        }
      }
    }
</script>

<style scoped>
  .box-card{
height: 60px;
width: 100%;
    box-shadow: 0 0 !important;
    border: 0 !important;

  }
.nav first{
  position: absolute;
    top: 84px;
    left: 0px;
}
.nav{
  margin-top: -20px;
  margin-left: 40px;
  font-family: PingFangSC-Semibold;
  font-size: 16px;
  color: black;
  text-decoration: none;

}
  a:hover{
    color:#0098ea;
  }
  .first{
    color:#0098ea;
  }
  .avatar{
    float: right;
    width: 30px;
    height:30px;
  }
  img{
    width: 30px;
    margin-top: 12px;
  }
  .name{
    margin-left: 10px;
    font-size: 14px;
    font-weight: 500;
    color: #424e67;
  }


</style>
