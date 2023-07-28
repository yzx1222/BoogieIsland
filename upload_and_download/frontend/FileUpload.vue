<template>
  <div>
    <input type="file" @change="onFileSelected" accept=".doc,.docx,.ppt,.pptx,.pdf,.png,.jpg,.jpeg" />
    <button @click="uploadFile" :disabled="!selectedFile">上传文件</button>
  </div>
</template>

<script>
import CryptoJS from 'crypto-js';
import api from '@/api.js';

export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    upload() {
      if (!this.selectedFile) {
        alert('请选择要上传的文件！');
        return;
      }
      

       // 检查文件类型是否合法
       if (!this.isValidFileType(this.selectedFile.type)) {
        alert('不支持的文件类型！仅支持普通office文件和常见图片格式。');
        return;
      }

      // 随机生成加密密钥
      let file_key = Array.from(crypto.getRandomValues(new Uint8Array(16)))
        .map((x) => x.toString(16))
        .join('');
      file_key = CryptoJS.MD5(file_key).toString();
      console.log('对称密钥：' + file_key);

      const reader = new FileReader();
      reader.readAsDataURL(this.selectedFile);
      reader.onload = (event) => {
        const file_content_base64 = event.target.result.split('base64,')[1];
        const srcs = CryptoJS.enc.Utf8.parse(file_content_base64);
        const encrypted = CryptoJS.AES.encrypt(srcs, CryptoJS.enc.Utf8.parse(file_key), {
          mode: CryptoJS.mode.ECB,
          padding: CryptoJS.pad.Pkcs7,
        }).toString();

        api.upload({
          encrypted,
          file_key,
          name: this.selectedFile.name,
          type: this.selectedFile.type,
        })
          .then(() => {
            this.$emit('fileUploaded');
          })
          .catch((error) => {
            console.error('上传文件时出错：', error);
            alert('上传失败！');
          });
      };
    },
  },
};
</script>
