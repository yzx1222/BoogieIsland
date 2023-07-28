<template>
  <div>
    <h2>文件下载</h2>
    <FileDownload />
  </div>
</template>

<script>
import FileDownload from '@/components/FileDownload.vue';

export default {
  name: 'DownloadPage',
  components: {
    FileDownload,
  },
};
</script>
