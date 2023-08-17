<template>
  <div>
    <h2>Uploaded Files</h2>
    <button @click="uploadFile">上传文件</button>
    <button @click="getFiles">获取文件列表</button>
    <input type="file" ref="fileInput" style="display: none" @change="handleFileChange($event)" />
    <ul>
      <li v-for="file in files" :key="file.filename">
        <a :href="getFileUrl(file.filename)" target="_blank">{{ file.filename }}</a>
        <button @click="downloadFile(file.filename)">下载</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      files: []
    };
  },
  methods: {
    async getFiles() {
      try {
        const response = await axios.get('/api/files');
        this.files = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    getFileUrl(filename) {
      return `/api/download/${filename}`;
    },
    uploadFile() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('fileData', file);

      axios
        .post('/api/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then(response => {
          console.log('File uploaded successfully:', response.data);
          this.getFiles();
        })
        .catch(error => {
          console.error('Error uploading file:', error);
        });
    },
    downloadFile(filename) {
      axios
        .get(`/api/download/${filename}`, {
          responseType: 'blob'
        })
        .then(response => {
          const blob = new Blob([response.data], { type: response.headers['content-type'] });
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = filename;
          link.click();
          URL.revokeObjectURL(url);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    this.getFiles();
  }
};
</script>
