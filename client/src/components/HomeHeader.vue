<template>
    <header>
      <nav>
        <ul>
          <li><router-link to="/home">Home</router-link></li>
          <li><router-link to="/about">About</router-link></li>
          <!-- 添加其他导航链接 -->
        </ul>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: 'AppHeader'
  };
  </script>
  
  <style scoped>
  header {
    background-color: #333;
    color: white;
    padding: 10px;
  }
  
  nav ul {
    list-style-type: none;
    padding: 0;
    display: flex;
  }
  
  nav li {
    margin-right: 20px;
  }
  
  router-link {
    color: white;
    text-decoration: none;
  }
  </style>
  