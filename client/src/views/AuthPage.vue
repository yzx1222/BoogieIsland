<template>
 <Header />
  <div class="row">
    <router-view></router-view>
  </div>
 <Footer />
</template>

<script>
import Header from '../components/AuthHeader.vue';

export default({
  name: "AuthPage",
  components: {
    Header,
  },
});
</script>

<style>
.row {
  margin-bottom: 20px;
}

.list-group {
  height: 20px;
  background-color: #87CEFA;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
}

.list-group-item {
  padding-left: 10px;
  padding-right: 10px;
  font-size: 20px;
}

.list-group-item:hover {
  background-color: #B0C4DE;
}

.list-group-item.active {
  background-color: #337ab7;
  color: #fff;
}

.router-link-exact-active {
  text-decoration: none;
}
</style>
