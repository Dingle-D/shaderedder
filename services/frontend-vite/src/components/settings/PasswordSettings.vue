<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Edit your personal profile</h2>
    <form class="space-y-4">
      <div class="border-t pt-4">
        <div class="flex flex-1 px-2 mb-4">
          <!-- Input section -->
          <div class="w-64 pt-2">
            <p> Current password </p>
          </div>
          <div class="w-full max-w-lg lg:max-w-xs">
            <label for="currentPassword" class="sr-only">Current password</label>
            <div class="relative text-gray-400 focus-within:text-gray-500">
              <input 
                id="CurrentPassword" 
                class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-2 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500 sm:text-sm" 
                placeholder="Current password" 
                type="currentPassword" 
                name="currentPassword" 
                v-model="currentPasswordPattern" 
              >
            </div>
          </div>
        </div>
        <div class="flex flex-1 px-2 mb-4">
          <!-- Input section -->
          <div class="w-64 pt-2">
            <p> New Password </p>
          </div>
          <div class="w-full max-w-lg lg:max-w-xs">
            <label for="newPassword" class="sr-only">New password</label>
            <div class="relative text-gray-400 focus-within:text-gray-500">
              <input 
                id="NewPassword" 
                class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-2 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500 sm:text-sm" 
                placeholder="New password" 
                type="newPassword" 
                name="newPassword" 
                v-model="newPasswordPattern" 
              >
            </div>
          </div>
        </div>
        <div class="flex flex-1 px-2">
          <!-- Input section -->
          <div class="w-64 pt-2">
            <p> New Password </p>
          </div>
          <div class="w-full max-w-lg lg:max-w-xs">
            <label for="confirmPassword" class="sr-only">Confirm password</label>
            <div class="relative text-gray-400 focus-within:text-gray-500">
              <input 
                id="ConfirmPassword" 
                class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-2 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500 sm:text-sm" 
                placeholder="Re type new password" 
                type="confirmPassword" 
                name="confirmPassword" 
                v-model="confirmPasswordPattern" 
              >
            </div>
          </div>
        </div>
      </div>
      <div class="border-t pt-4">
        <button class="w-full flex items-center justify-center hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900">
          <h3 class="text-lg">CHANGE PASSWORD</h3>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "EmailSettings",
  data() {
    return {
      emailPattern: '',
      passwordPattern: ''
    }
  }
}
</script>
