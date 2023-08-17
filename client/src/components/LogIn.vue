<template>

  <div class="login-container">
  
    <h2>Login</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="email">E-mail:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="login-button">Login</button>
    </form>
  
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // 导入useRouter

const router = useRouter(); // 获取路由器实例

const email = ref('');
const password = ref('');


const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/auth/login', {
      email: email.value,
      password: password.value
    });

    const token = response.data.token;
    const userdata = response.data.user_data;
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('userid', userdata.id);
    sessionStorage.setItem('useremail', userdata.email);
    sessionStorage.setItem('username', userdata.name);

    console.log('登录成功:', token, userdata);
    router.push('/home'); // 使用router进行导航
  } catch (error) {
    console.error('登录失败:', error);
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

.login-form {
  display: flex;
  flex-direction: column;
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
