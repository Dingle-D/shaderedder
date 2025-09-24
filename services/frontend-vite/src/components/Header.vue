<template>
    <nav class="bg-gray-50">
      <div class="mx-auto max-w-full px-4 sm:px-6 lg:px-8">
        <div class="relative flex h-16 items-center justify-between border-b border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <a href="#" @click="onLogo">
              <img class="h-10 w-auto" src="@/assets/icons/logo.svg" alt="Shaderedder Icon">
              </a>
            </div>

            <!-- Links section -->
            <div class="hidden lg:ml-10 lg:block">
              <div class="flex space-x-4">
                
                  <a href="#" @click="onExplore" class="hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium text-gray-900" x-state-description="Explore tab">
                    Explore
                  </a>
                
                  <a href="#" @click="onEditor" class="hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium text-gray-900" x-state-description="Editor tab">
                    Editor
                  </a>
                
                  <a href="#" @click="onAbout" class="hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium text-gray-900" x-state-description="About tab">
                    About
                  </a>
                
              </div>
            </div>
          </div>

          <div class="flex flex-1 justify-center px-2 lg:ml-6 lg:justify-end">
            <!-- Search section -->
            <!--
            <div class="w-full max-w-lg lg:max-w-xs">
              <label for="search" class="sr-only">Search</label>
              <div class="relative text-gray-400 focus-within:text-gray-500">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <svg class="h-5 w-5" x-description="Heroicon name: mini/magnifying-glass" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <input 
                  id="search" 
                  class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-10 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500 sm:text-sm" 
                  placeholder="Search" 
                  type="search" 
                  name="search" 
                  v-model="searchPattern" 
                  @keydown.enter="onSearch(searchPattern)">
              </div>
            </div>
            -->
          </div>
          <!-- Mobile menu button -->
          <div class="flex lg:hidden">
            <button type="button" class="inline-flex items-center justify-center rounded-md bg-gray-50 p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-50" aria-controls="mobile-menu" @click="open = !open" :aria-expanded="open.toString()">
              <span class="sr-only">Open main menu</span>
              <svg class="h-6 w-6" :class="{ 'hidden': open, 'block': !(open) }" x-description="Heroicon name: outline/bars-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"></path>
              </svg>
              <svg class="h-6 w-6" :class="{ 'block': open, 'hidden': !(open) }" x-description="Heroicon name: outline/x-mark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div> <!-- -->

          <!-- Actions section -->
          <div class="hidden lg:ml-4 lg:block">
            <div class="flex items-center">

              <div v-if="isAuthenticated" class="flex items-center space-x-3">
                <button type="button" @click="onLogout" class="flex-shrink-0 rounded-full bg-gray-50 p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-50">
                  <svg class="h-6 w-6" x-description="Logout icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                    <path stroke="#292d32" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5" d="M6.56 14.56 4 12l2.56-2.56M9.24 12H4.07M14.24 12h-1.96M18.01 6.48C19.25 7.84 20 9.71 20 12c0 5-3.58 8-8 8M12 4c1.05 0 2.05.17 2.97.49"/>
                  </svg>
                </button>

                <!-- Profile dropdown -->
                <div>
                  <div>
                    <button type="button" class="flex rounded-full bg-gray-50 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-50" id="user-menu-button" ref="profileButton1" @click="onProfile" @keyup.space.prevent="onButtonEnter()" @keydown.enter.prevent="onButtonEnter()" aria-haspopup="true" :aria-expanded="open.toString()">
                      <span class="sr-only">Profile</span>
                      <img class="h-10 w-10 rounded-full" src="@/assets/icons/user.png" alt="">
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="flex items-center space-x-3">
                <!--
                <button type="button" class="px-6 py-2 min-w-[120px] text-center text-violet-600 border border-violet-600 rounded hover:bg-violet-600 hover:text-white active:bg-indigo-500 focus:outline-none focus:ring">
                  SingIn
                </button>
                -->
                <a href="#" @click="onSignIn" class="hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900" x-state-description="Sign in button">
                  SignIn
                </a>
              </div>

            </div>
          </div>
        </div>
      </div>

      <div x-description="Mobile menu, show/hide based on menu state." class="border-b border-gray-200 bg-gray-50 lg:hidden" id="mobile-menu" v-show="open">
        <div class="space-y-1 px-2 pt-2 pb-3">
          
            <a href="#" @click="onExplore" class="bg-gray-100 block px-3 py-2 rounded-md font-medium text-gray-900" aria-current="page" x-state:on="Current" x-state:off="Default" x-state-description="Current: &quot;bg-gray-100&quot;, Default: &quot;hover:bg-gray-100&quot;">
              Explore
            </a>
          
            <a href="#" @click="onEditor" class="hover:bg-gray-100 block px-3 py-2 rounded-md font-medium text-gray-900" x-state-description="undefined: &quot;bg-gray-100&quot;, undefined: &quot;hover:bg-gray-100&quot;">
              Editor
            </a>
          
            <a href="#" @click="onAbout" class="hover:bg-gray-100 block px-3 py-2 rounded-md font-medium text-gray-900" x-state-description="undefined: &quot;bg-gray-100&quot;, undefined: &quot;hover:bg-gray-100&quot;">
              About
            </a>
          
        </div>
        <div class="border-t border-gray-200 pt-4 pb-3">
          <div class="flex items-center px-5">
            <div v-if="isAuthenticated" class="flex items-center space-x-3">
              <div class="flex-shrink-0">
                <button type="button" class="flex rounded-full bg-gray-50 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-50" id="user-menu-button" ref="profileButton1" @click="onProfile" @keyup.space.prevent="onButtonEnter()" @keydown.enter.prevent="onButtonEnter()" aria-haspopup="true" :aria-expanded="open.toString()">
                  <span class="sr-only">Profile</span>
                  <img class="h-10 w-10 rounded-full" src="@/assets/icons/user.png" alt="">
                </button>
              </div>
              <div class="ml-3">
                <div class="text-base font-medium text-gray-800">{{userAuthenticated}}</div>
                <div class="text-sm font-medium text-gray-500">{{emailAuthenticated}}</div>
              </div>
              <button @click="onLogout" type="button" class="inline-flex items-center justify-center rounded-md bg-gray-50 p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-50">
                <span class="sr-only">logout</span>
                <!-- Bell icon
                <svg class="h-6 w-6" x-description="Logout icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"></path>
                </svg>
                -->
                <!-- Logout icon stroke="#292d32"-->
                <svg class="h-6 w-6" x-description="Logout icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                  <path stroke="#adadad" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5" d="M6.56 14.56 4 12l2.56-2.56M9.24 12H4.07M14.24 12h-1.96M18.01 6.48C19.25 7.84 20 9.71 20 12c0 5-3.58 8-8 8M12 4c1.05 0 2.05.17 2.97.49"/>
                </svg>
              </button>
            </div>
            <div v-else class="flex flex-1 items-center space-x-3">
              <a href="#" @click="onSignIn" class="w-full bg-gray-900 hover:text-gray-100 block py-2 rounded-md font-medium text-white text-center" x-state-description="Sign in button">
                SignIn
              </a>
            </div>
          </div>
          <!--
          <div class="mt-3 space-y-1 px-2">
              <a href="#" class="block rounded-md py-2 px-3 text-base font-medium text-gray-900 hover:bg-gray-100">
                Your Profile
              </a>
            
              <a href="#" class="block rounded-md py-2 px-3 text-base font-medium text-gray-900 hover:bg-gray-100">
                Sign out
              </a>
            
          </div>
          -->
        </div>
      </div>
    </nav>
</template>

<script>
  import { mapState, mapActions } from "vuex";
  export default {
    name: "AppHeader",
    data() {
      return {
        open: false,
        searchPattern: ''
      }
    },
    methods: {
      ...mapActions('auth', ['LOGOUT']),

      onLogout() {
        this.$store
          .dispatch('LOGOUT')
          .then(() => this.$router.push({ name: "home" }));
      },

      onLogo() {
        console.log("Clicked home (logo) menu")
        this.$router.push({name: "home"});
      },
      onExplore() {
        console.log("Clicked explore menu")
        this.$router.push({name: "explore"});
      },
      onEditor() {
        console.log("Clicked editor menu")
        this.$router.push({name: "editor"});
      },
      onAbout() {
        console.log("Clicked about menu")
        this.$router.push({name: "about"});
      },
      onSearch(pattern) {
        console.log("Search:", pattern);
      },
      onProfile() {
        console.log("Clicked profile icon");
        this.$router.push({name: "me"})
      },
      onSignIn() {
        console.log("Clicked sign in button");
        this.$router.push({name: "login"});
      }
    },
    computed: {
      ...mapState({
        isAuthenticated: state => state.auth.isAuthenticated,
        userAuthenticated: state => state.auth.user.username,
        emailAuthenticated: state => state.auth.user.email
      })
    }
  }
</script>

