<template>
  <div id="app">
    <Header />
    <div class="content">
      <router-view />
      <FileList ref="fileList" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import FileList from '../components/FileList.vue';
import Header from '../components/HomeHeader.vue';

export default {
  components: {
    Header,
    FileList
  },
  methods: {
    async uploadFile(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        await axios.post('http://localhost:3000/api/upload', formData);
        this.$refs.fileList.getFiles();
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
.content {
  margin: 20px;
}
/* 其他样式可以在这里添加 */
</style>
