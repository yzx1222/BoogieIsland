<template>
  <Header />
    <div>
      <h1>About Us</h1>
      <p>Welcome to our file sharing app! Here's some information about us.</p>
    </div>
  </template>
  
  <script>
  import Header from '../components/HomeHeader.vue';

  export default {
    name: 'AppAbout',
    components:{
      Header,
    }
  };
  </script>
  
  <style scoped>
  /* 样式可以在这里添加 */
  </style>
  