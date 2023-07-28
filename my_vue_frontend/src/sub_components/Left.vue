<template>
  <el-container>
    <el-header>
      <el-menu default-active="2" class="el-menu-vertical-demo">
        <el-menu-item index="2">
          <i class="el-icon-tickets"></i>
          <span slot="title">全部文件</span>
        </el-menu-item>
        <el-menu-item index="3" class="item">
          <i class="el-icon-minus"></i>
          <span slot="title">图片</span>
        </el-menu-item>
        <el-menu-item index="3" class="item">
          <i class="el-icon-minus"></i>
          <span slot="title">文档</span>
        </el-menu-item>
        <el-menu-item index="3">
          <i class="el-icon-minus"></i>
          <span slot="title">视频</span>
        </el-menu-item>
        <el-menu-item index="3">
          <i class="el-icon-minus"></i>
          <span slot="title">音乐</span>
        </el-menu-item>
        <el-menu-item index="3">
          <i class="el-icon-minus"></i>
          <span slot="title">其他</span>
        </el-menu-item>
      </el-menu>
    </el-header>
    <el-main></el-main>
    <el-footer>
      <div class="footer-progress">
        <el-progress
          :text-inside="false"
          :stroke-width="10"
          :percentage="use"
          :show-text="false"
        ></el-progress>
      </div>
      <div class="footer-breadcrumb">
        <el-breadcrumb separator="/" class="breadcrumb-container">
          <el-breadcrumb-item>{{ usesize }}</el-breadcrumb-item>
          <el-breadcrumb-item>500M</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
import { Container, Header, Menu, MenuItem, Main, Footer, Progress, Breadcrumb, BreadcrumbItem } from 'element-ui';
import qs from 'qs';

export default {
  name: "Left",
  data() {
    return {
      use: 0,
      usesize: "0",
    };
  },
  components: {
    'el-container': Container,
    'el-header': Header,
    'el-menu': Menu,
    'el-menu-item': MenuItem,
    'el-main': Main,
    'el-footer': Footer,
    'el-progress': Progress,
    'el-breadcrumb': Breadcrumb,
    'el-breadcrumb-item': BreadcrumbItem,
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios.post(this.$HOST + "v2/getusesize", qs.stringify({ sign: this.$sign }))
        .then((res) => {
          var MB = 524288000;
          var persent = parseInt(res.data.data.size / MB);
          this.use = (persent === 0) ? 1 : persent;
          this.usesize = res.data.data.realsize;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.el-menu {
  background-color: #f7f7f7;
  border: 0;
}

.item {
  color: #424e67;
  font-size: 14px;
}

.footer-progress {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.footer-breadcrumb {
  margin-top: 5px;
  display: flex;
  justify-content: center;
}

.breadcrumb-container {
  font-size: 12px;
}

.el-breadcrumb__inner {
  color: #909399;
}

.el-breadcrumb__inner:hover {
  color: #409eff;
}
</style>
