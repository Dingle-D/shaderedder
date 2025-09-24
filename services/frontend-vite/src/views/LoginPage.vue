<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
        </h2>
    </div>
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form @submit.prevent="onSubmit(login, password)" class="space-y-5">

          <div v-if="error" class="flex flex-1 px-3 py-2 rounded-md bg-red-500 text-white">
            {{ error }}
          </div>
          
          <div>
            <label for="login" class="block text-sm font-medium text-gray-700">
              Login
            </label>
            <div class="mt-1">
              <input 
                id="login" 
                name="login"
                type="text" 
                v-model="login" 
                required
                  class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Enter your username or email"
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


          <div class="flex text-sm justify-end">
              <a href="#" class="font-medium text-green-600 hover:text-green-500 hover:underline">
                  Forgot your password?
              </a>
          </div>
          
          <div class="flex justify-center">
            <button type="submit" :disabled="loading" class="px-20 py-2 text-white font-semibold rounded-full bg-gradient-to-r from-green-600 via-green-700 to-green-600 hover:opacity-90 transition duration-200">
              {{ loading ? 'Loading...' : 'SignIn' }}
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

          <div>
            <button @click="onGuglSignIn"
              class="w-full flex space-x-2 items-center justify-center px-8 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
              <img class="h-5 w-5" src="@/assets/icons/google-1.svg"
                alt="">
              <p>SignIn with Google</p>
            </button>
          </div>
        </div>
        <div class="mt-8">
          <div class="flex text-sm justify-center">
            <span>
              Don't have an account?
              <a href="#" class="font-semibold text-green-600 hover:text-green-500 hover:underline" @click="onSignUp">
                SignUp
              </a>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from "@/common/api.service";
import { mapState, mapActions } from "vuex";

export default {
  name: "AppLogin",
  data() {
    return {
      form: {
        login: '',
        password: ''
      }
    }
  },
  methods: {
    ...mapActions('auth', ['LOGIN']),

    onSubmit(login, password) {
      this.$store
        .dispatch('LOGIN', { 
          username: login, 
          password: password
        })
        .then(() => this.$router.push({ name: "explore" }))
        .catch((error) => console.log("Error in onSubmit:", error));
    },

    onGuglSignIn() {
      window.location.href = `${ApiService.getApiUrl()}/login/google-login-rd`;
    },

    onSignUp() {
      this.$router.push({ name: "register" })
      .catch((error) => console.log("Error in onSignUp:", error));
    }
  },
  computed: {
    ...mapState({
      error: state => state.auth.errors
    })
  }
};
</script>

<style scoped>
.error-message {
  color: #ff4444;
  margin-bottom: 15px;
}
</style>
