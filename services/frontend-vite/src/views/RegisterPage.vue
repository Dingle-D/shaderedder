<!-- <template>
  <form @submit.prevent="handleRegister">
    <h1>РЕГИСТРАЦИЯ</h1>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div>
      <label for="username">Имя пользователя</label>
      <input 
        id="username" 
        type="text" 
        v-model="username"
        placeholder="введите username"
        required
      >
    </div>
    
    <div>
      <label for="email">Email</label>
      <input 
        id="email" 
        type="email" 
        v-model="email"
        placeholder="введите email"
        required
      >
    </div>
    
    <div>
      <label for="password">Пароль</label>
      <input 
        id="password" 
        type="password" 
        v-model="password"
        placeholder="введите password"
        required
      >
    </div>
    
    <button type="submit">Зарегистрироваться</button>
    
    <span class="toggle-link" @click="goToLogin">
      Есть аккаунт? Войти
    </span>
  </form>
</template>
-->

<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create new account
        </h2>
    </div>
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form @submit.prevent="onSubmit(username, email, password)" class="space-y-5">

          <div v-if="error" class="flex flex-1 px-3 py-2 rounded-md bg-red-500 text-white">
            {{ error }}
          </div>
          
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Login
            </label>
            <div class="mt-1">
              <input 
                id="username" 
                name="username"
                type="text" 
                v-model="username" 
                required
                  class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Enter your username"
              >
            </div>
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email
            </label>
            <div class="mt-1">
              <input 
                id="email" 
                name="email"
                type="email" 
                v-model="email" 
                required
                  class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Enter your email"
              >
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input 
                id="password" 
                name="password"
                type="password" 
                v-model="password" 
                required
                  class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Enter your password"
              >
            </div>
          </div>

          <div class="flex justify-center">
            <button type="submit" :disabled="loading" class="px-20 py-2 text-white font-semibold rounded-full bg-gradient-to-r from-green-600 via-green-700 to-green-600 hover:opacity-90 transition duration-200">
              {{ loading ? 'Loading...' : 'SignUp' }}
            </button>
          </div>
          
        </form>
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-gray-100 text-gray-500">
                Or continue with
              </span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-3 gap-3">
            <div>
              <a href="#"
                class="w-full flex items-center justify-center px-8 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                <img class="h-5 w-5" src="@/assets/icons/google-1.svg"
                  alt="">
              </a>
            </div>
            <div>
              <a href="#"
                class="w-full flex items-center justify-center px-8 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                <img class="h-5 w-5" src="@/assets/icons/github-1.svg"
                  alt="">
              </a>
            </div>
            <div>
              <a href="#"
                class="w-full flex items-center justify-center px-8 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                <img class="h-5 w-5" src="@/assets/icons/vk-2.svg"
                  alt="">
              </a>
            </div>
          </div>
        </div>
        <div class="mt-8">
          <div class="flex text-sm justify-center">
            <span>
              Already have an account?
              <a href="#" class="font-semibold text-green-600 hover:text-green-500 hover:underline" @click="onSignIn">
                SignIn
              </a>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import api from '@/api'
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        error: ''
      }
    }
  },
  methods: {
    ...mapActions('auth', ['REGISTER']),

    onSubmit(username, email, password) {
      this.$store
        .dispatch('REGISTER', { 
          username: username, 
          email: email,
          password: password
        })
        .then(() => this.$router.push({ name: "confirm-email" }))
        .catch((error) => console.log("Error in onSubmit:", error));
    },

    onSignIn() {
      this.$router.push({ name: "login" })
      .catch((error) => console.log("Error in onSignIn:", error));
    }

    // There starts bad api
    /*
    async handleRegister() {
  try {
    const response = await api.post('/register/new', {
      username: this.username,
      email: this.email,
      password: this.password
    });

    if (response.data.success) {
      // Сохраняем токен для активации
      localStorage.setItem('activation_token', response.data.activation_token);
      this.$router.push('/confirm-email');
    }
  } catch (error) {
    this.error = error.response?.data?.detail || 'Registration failed';
  }
},
    goToLogin() {
      this.$router.push('/');
    }
  */
  },
  computed: {
    ...mapState({
      error: state => state.auth.errors
    })
  }
}
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
.error-message {
  color: red;
}
</style>
