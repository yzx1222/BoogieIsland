<template>
  <div class="login-container">
    <h2>登录</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">用户名：</label>
        <input type="text" id="username" v-model="formData.username" required>
      </div>
      <div class="form-group">
        <label for="password">密码：</label>
        <input type="password" id="password" v-model="formData.password" required>
      </div>
      <button type="submit" class="login-button">登录</button>
    </form>
    <div v-if="message" class="mt-3 alert alert-danger">{{ message }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        password: ''
      },
      message: ''
    };
  },
  methods: {
    login() {
      this.message = '';
      axios
        .post('/login', this.formData)
        .then(response => {
          // 处理登录成功情况
          const token = response.data.token;
          // 将令牌保存在localStorage中，用于后续的认证和请求
          localStorage.setItem('token', token);
          // 重定向到受保护的页面或仪表板
          this.$router.push('/dashboard');
        })
        .catch(error => {
          // 处理登录失败情况
          this.message = error.response.data.message;
        });
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: scale(1.2);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.login-button {
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #0056b3;
}
</style>