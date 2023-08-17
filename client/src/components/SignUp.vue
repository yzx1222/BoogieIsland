<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="signup" class="signup-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" @input="onPasswordChange" required>
      </div>
      <div class="passwordstrength">
        <div :class="(password && (isOne || isTwo || isThree || isFour || isFive || isSix || isSeven)) ? 'colorRed' : 'colorInit'"></div>
        <div :class="(isTwo || isThree || isFour || isFive || isSix || isSeven) ? 'colorRed2' : 'colorInit'"></div>
        <div :class="(isThree || isFour || isFive || isSix || isSeven) ? 'colorOrange' : 'colorInit'"></div>
        <div :class="(isFour || isFive || isSix || isSeven) ? 'colorOrange2' : 'colorInit'"></div>
        <div :class="(isFive || isSix || isSeven) ? 'colorGreen' : 'colorInit'"></div>
        <div :class="(isSix || isSeven) ? 'colorGreen2' : 'colorInit'"></div>
        <div :class="isSeven ? 'colorSafe' : 'colorInit'"></div>
        <div v-show="password" class="left5">{{ psdStrength }}</div>
      </div>
      <div class="form-group">
        <label for="confirm_password">Confirm Password:</label>
        <input type="password" id="confirm_password" v-model="confirmPassword" required>
      </div>
      <button type="submit" class="signup-button">Sign Up</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { checkPassword } from '../utils/passwordUtils';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const psdStrength = ref(null);
const isOne = ref(false);
const isTwo = ref(false);
const isThree = ref(false);
const isFour = ref(false);
const isFive = ref(false);
const isSix = ref(false);
const isSeven = ref(false);

const signup = () => {
  if (password.value !== confirmPassword.value) {
    console.log('密码不匹配');
    return;
  }

  axios
    .post('http://127.0.0.1:5000/auth/signup', {
      email: email.value,
      password: password.value,
      confirmPassword: confirmPassword.value,
      username: username.value
    })
    .then(response => {
      console.log('注册成功:', response.data);
      router.push('/login');
    })
    .catch(error => {
      console.error('注册失败:', error);
    });
};

const onPasswordChange = (event) => {
  isOne.value = false;
  isTwo.value = false;
  isThree.value = false;
  isFour.value = false;
  isFive.value = false;
  isSix.value = false;
  isSeven.value = false;
  const psdVal = event.target.value;
  const strength = checkPassword(psdVal);
  psdStrength.value = strength;
  switch (strength) {
    case '非常弱':
      isOne.value = true;
      break;
    case '弱':
      isTwo.value = true;
      break;
    case '比较弱':
      isThree.value = true;
      break;
    case '一般':
      isFour.value = true;
      break;
    case '强':
      isFive.value = true;
      break;
    case '安全':
      isSix.value = true;
      break;
    case '非常安全':
      isSeven.value = true;
      break;
    default:
      break;
  }
};
</script>

<style scoped>
.signup-container {
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
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.passwordstrength {
  display: flex;
  background-color: #f5f5f5;
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

.signup-button {
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.signup-button:hover {
  background-color: #0056b3;
}

.left5 {
  float: left;
}

.colorRed {
  background-color: crimson;
  width: 20px;
}

.colorRed2 {
  background-color: rgb(220, 127, 20);
  width: 20px;
}

.colorOrange {
  background-color: rgb(253, 218, 62);
  width: 20px;
}

.colorOrange2 {
  background-color: rgb(231, 253, 62);
  width: 20px;
}

.colorGreen {
  background-color: rgb(155, 251, 0);
  width: 20px;
}

.colorGreen2 {
  background-color: rgb(0, 251, 59);
  width: 20px;
}

.colorSafe {
  background-color: rgb(13, 213, 30);
  width: 20px;
}

.colorInit {
  background-color: whitesmoke;
  width: 20px;
}
</style>
