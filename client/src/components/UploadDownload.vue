<!-- src/components/UploadDownload.vue -->
<template>
    <div>
      <h1>Simple File Sharin</h1>
      <input type="file" @change="uploadFile">
      <h2>Uploaded Files</h2>
      <ul>
        <li v-for="file in uploadedFiles" :key="file">
          <a :href="getFileUrl(file)" target="_blank">{{ file }}</a>
        </li>
      </ul>
    </div>
  </template>
  
  <script>

  import axios from 'axios';
  export default {
    data() {
      return {
        uploadedFiles: []
      };
    },
    methods: {
      uploadFile(event) {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        axios.post('/upload', formData).then(() => {
          this.getUploadedFiles();
        });
      },
      getUploadedFiles() {
        axios.get('/files').then(response => {
          this.uploadedFiles = response.data;
        });
      },
      getFileUrl(filename) {
        return `/download/${filename}`;
      }
    },
    created() {
      this.getUploadedFiles();
    }
  };
  </script>
  