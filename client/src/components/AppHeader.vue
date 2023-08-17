<template>
  <header>
    <nav>
      <ul>
        
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
