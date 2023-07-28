<template>
  <div>
    <button @click="downloadFile">下载文件</button>
    <button @click="downloadOriginalFile">下载解密前的文件</button>
    <button @click="downloadSignatureFile">下载数字签名文件</button>
  </div>
</template>

<script>
import CryptoJS from 'crypto-js';
import api from '@/api.js';

export default {
  methods: {
    download() {
      api.download(file_id) 
        .then((data) => {
          
          // 解密对称密钥
          let key = data.file_enc_key;
          key = CryptoJS.AES.decrypt(
            key,
            CryptoJS.enc.Utf8.parse(store.state.AuthModule.user.master_key),
            {
              mode: CryptoJS.mode.ECB,
              padding: CryptoJS.pad.Pkcs7,
            }
          ).toString(CryptoJS.enc.Utf8);
          console.log('解密后的对称密钥：' + key);

          // 解密文件内容
          let file_content = data.content;
          const decrypt = CryptoJS.AES.decrypt(file_content, CryptoJS.enc.Utf8.parse(key), {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7,
          });
          file_content = decrypt.toString(CryptoJS.enc.Utf8);
          console.log('解密后的文件内容：' + file_content);

          // 创建下载链接并模拟点击下载
          const blob = new Blob([file_content], { type: data.type });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', file_id); // 替换为实际的文件名
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch((error) => {
          console.error('下载文件时出错：', error);
          alert('下载失败！');
        });
    },

    downloadOriginalFile() {
      api.downloadOriginalFile(file_id) // 替换为要下载的文件ID
        .then((data) => {
          // 直接获取解密前的文件内容，并创建下载链接
          const file_content = data.content;
          const blob = new Blob([file_content], { type: data.type });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', file_id); // 替换为实际的文件名
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch((error) => {
          console.error('下载解密前的文件时出错：', error);
          alert('下载失败！');
        });
    },



    downloadSignatureFile() {
      api.downloadSignatureFile(file_id) // 替换为要下载的文件ID
        .then((data) => {
          // 直接获取数字签名文件内容，并创建下载链接
          const signature_file_content = data.signature_file_content;
          const blob = new Blob([signature_file_content], { type: 'application/octet-stream' });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'signature.txt'); // 替换为实际的数字签名文件名
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch((error) => {
          console.error('下载数字签名文件时出错：', error);
          alert('下载失败！');
        });
    },



  },
};
</script>
