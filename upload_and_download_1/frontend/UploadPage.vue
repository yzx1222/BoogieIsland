<template>
  <div>
    <h2>文件上传</h2>
    <FileUpload @fileUploaded="onFileUploaded" />
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue';

export default {
  name: 'UploadPage',
  components: {
    FileUpload,
  },
  methods: {
    onFileUploaded() {
      alert('上传成功！');
    },
  },
};
</script>
