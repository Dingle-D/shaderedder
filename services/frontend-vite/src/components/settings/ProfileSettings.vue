<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Edit your personal profile</h2>
    <form class="space-y-4">
      <div class="flex space-x-4">
        <img class="aspect-square w-24 mr-6" 
             src="https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg" 
             alt="PROFILE IMG"/>
        <div>
          <button class="hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900"> 
            <h3>UPLOAD NEW PICTURE</h3>
          </button>
          <p class="text-sm text-gray-700"> JPG or PNG and 1MB max </p>
        </div>
      </div>
      <div class="border-t pt-4">
        <div class="flex flex-1 px-2">
          <!-- Input section -->
          <div class="w-64 pt-2">
            <p> Username </p>
          </div>
          <div class="w-full max-w-lg lg:max-w-xs">
            <label for="username" class="sr-only">Username</label>
            <div class="relative text-gray-400 focus-within:text-gray-500">
              <input 
                id="username" 
                class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-2 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500 sm:text-sm" 
                placeholder="Ivan Ivanov" 
                type="username" 
                name="username" 
                v-model="usernamePattern" 
              >
            </div>
          </div>
        </div>
      </div>
      <div class="border-t pt-4">
        <button class="w-full flex items-center justify-center hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900">
          <h3 class="text-lg">SAVE PROFILE</h3>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "ProfileSettings",
  data() {
    return {
      usernamePattern: ''
    }
  }
}
</script>
