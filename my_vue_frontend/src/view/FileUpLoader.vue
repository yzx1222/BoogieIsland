<template>
    <div>
      <input type="file" @change="onFileChange" />
      <div v-if="imageUrl">
        <img :src="imageUrl" alt="Uploaded Image" />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        imageUrl: null,
      };
    },
    methods: {
      onFileChange(event) {
        const file = event.target.files[0];
        this.imageUrl = URL.createObjectURL(file);
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  