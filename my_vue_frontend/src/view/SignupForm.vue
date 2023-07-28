<template>
    <div class="signup-container">
      <h2>Sign Up</h2>
      <form @submit.prevent="signup" class="signup-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" @change="onPasswordChange" required>
        </div>
        <div class="passwordstrength">
          <div :class="(password &&(isOne||isTwo||isThree||isFour||isFive||isSix||isSeven))?'colorRed' : 'colorInit'"></div>
          <div :class="(isTwo||isThree||isFour||isFive||isSix||isSeven)? 'colorRed2' : 'colorInit'"></div>
          <div :class="(isThree||isFour||isFive||isSix||isSeven)? 'colorOrange ' : 'colorInit'"></div>
          <div :class="(isFour||isFive|isSix||isSeven)? 'colorOrange2' : 'colorInit'"></div>
          <div :class="(isFive||isSix||isSeven)? 'colorGreen': 'colorInit'"></div>
          <div :class="(isSix|| isSeven)? 'colorGreen2' : 'colorInit'"></div>
          <div :class="isSeven? 'colorSafe' : 'colorInit'"></div>
          <div v-show="password" class="left5"> {{psdStrength}} </div>
        </div>
        <div class="form-group">
          <label for="confirm_password">Confirm Password:</label>
          <input type="password" id="confirm_password" v-model="confirmPassword" required>
        </div>
        <button type="submit" class="signup-button">Sign Up</button>
      </form>
    </div>
    
  </template>
  
  <script>
  import axios from 'axios';
  import { checkPassword } from '../utils/passwordUtil';
  
  export default {
    data() {
      return {
        password: null,
        psdStrength: null,
        isOne: false,
        isTwo: false,
        isThree: false,
        isFour: false,
        isFive: false,
        isSix: false,
        isSeven: false,
        email: '',
        password: '',
        confirmPassword: ''
      };
    },
    methods: {
      signup() {
        // 检查密码是否匹配
        if (this.password !== this.confirmPassword) {
          console.log('密码不匹配');
          return;
        }
        const path = 'http://127.0.0.1:5000/auth/signup'; // 修改为正确的路径
        // 使用 Axios 或其他 HTTP 客户端库发送 POST 请求，将用户输入的邮箱和密码传递到后端
        axios
          .post(path, { email: this.email, password: this.password })
          .then(response => {
            // 注册成功，可以进行其他逻辑处理
            console.log('注册成功:', response.data);
            // 可以在这里根据返回的数据进行进一步处理，例如显示提示信息、跳转页面等
            this.$router.push('/login');
          })
          .catch(error => {
            // 注册失败，可以进行其他逻辑处理
            console.error('注册失败:', error);
          });
      },
      onPasswordChange(val) {
        this.isOne = false;
        this.isTwo = false;
        this.isThree = false;
        this.isFour = false;
        this.isFive = false;
        this.isSix = false;
        this.isSeven = false;
        const psdVal = val.target.value;
        const psdStrength = checkPassword(psdVal);
        this.psdStrength = psdStrength;
        switch (psdStrength) {
          case '非常弱':
            this.isOne = true;
            break;
          case '弱':
            this.isTwo = true;
            break;
          case '比较弱':
            this.isThree = true;
            break;
          case '一般':
            this.isFour = true;
            break;
          case '强':
            this.isFive = true;
            break;
          case '安全':
            this.isSix = true;
            break;
          case '非常安全':
            this.isSeven = true;
            break;
          default:
            break;
        }
      }
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
    /* transform: scale(1.2); */ /* 先注释掉这行样式 */
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
  .passwordstrength{
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
  
  #tips span:not(:last-child) {
    float: left;
    width: 30px;
    height: 20px;
    border: 1px solid transparent;
    font-size: 15px;
    margin-right: 2px;
    line-height: 20px;
    text-align: center;
  }
  
  .left5 {
    float: left;
  }
  
  .colorRed {
    background-color: crimson;
    width:20px;
  }
  .colorRed2 {
    background-color: rgb(220, 127, 20);
    width:20px;
  }
  .colorOrange {
    background-color: rgb(253, 218, 62);
    width:20px;
  }
  .colorOrange2 {
    background-color: rgb(231, 253, 62);
    width:20px;
  }
  .colorGreen {
    background-color: rgb(155, 251, 0);
    width:20px;
  }
  .colorGreen2 {
    background-color: rgb(0, 251, 59);
    width:20px;
  }
  .colorSafe {
    background-color: rgb(13, 213, 30);
    width:20px;
  }
  
  .colorInit {
    background-color: whitesmoke;
    width:20px;
  }
  </style>
  