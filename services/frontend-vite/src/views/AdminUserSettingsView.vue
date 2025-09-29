<template>
  <div v-if="user == null">...</div>
  <div v-else class="p-6">
    <div class="font-semibold text-xl">
      ID: {{ user.id }}
    </div>
    <div class="font-semibold text-lg">
      {{ user.username }}
    </div>
    <div class="text-md text-gray-600">
      {{ user.email }}
    </div>
    <div :class="user.is_activated ? 'text-green-600' : 'text-red-600'">
      {{ user.is_activated ? 'Activated' : 'Deactivated' }}
    </div>
    <hr></hr>
    <div class="mt-8 space-y-10">
      <form class="space-y-4 border-b">
        <h1 class="text-xl font-semibold">
          Account settings:
        </h1>
        <div class="pt-2">
          <div class="flex flex-1 px-2 mb-4 space-x-8 items-center">
            <button 
              type="button"
              @click="toggleActivation(user)" 
              class="justify-center hover:text-gray-400 px-4 py-2 rounded-md text-sm font-medium text-white bg-gray-900"
            >
              <h3 class="text-lg"> ACTIVATE/DEACTIVATE </h3>
            </button>
          </div>
        </div>
      </form>
      <form class="space-y-4 border-b pb-4">
        <h1 class="text-xl font-semibold">
          Password settings:
        </h1>
        <div class="pt-4">
          <div class="flex flex-1 px-2 mb-4">
            <!-- Input section -->
            <div class="w-64 pt-2">
              <p> New password </p>
            </div>
            <div class="w-full max-w-lg lg:max-w-xs">
              <label for="currentPassword" class="sr-only">Current password</label>
              <div class="relative text-gray-400 focus-within:text-gray-500">
                <input 
                  id="NewPassword" 
                  class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-2 pr-3 leading-5 text-gray-900 placeholder-gray-500 focus:border-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-purple-500 sm:text-sm" 
                  placeholder="New password" 
                  name="newPassword" 
                  v-model="newPassword" 
                >
              </div>
            </div>
          </div>
          <div class="flex flex-1 px-2 mb-4">
            <div class="w-64 pt-2">
              <p> Reset on sign in </p>
            </div>
            <div class="w-full max-w-lg lg:max-w-xs flex items-center">
              <input 
                class="h-5 w-5" 
                type="checkbox" 
                id="checkbox" 
                v-model="checked"
              >
            </div>
          </div>
          <div class="text-gray-600 text-sm">
            *leave password input field empty to change only 'reset on sign in' parameter
          </div>
        </div>
        <div class="pt-4">
          <button class="w-full flex items-center justify-center hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900">
            <h3 class="text-lg">CHANGE PASSWORD</h3>
          </button>
        </div>
      </form>
      <div >
        <h1 class="text-xl font-semibold mb-8">
          Sessions:
        </h1>
        <div v-if="sessions == null" class="text-red-500">Could not load sessions</div>
        <ul v-else class="space-y-4">
          <li
            v-for="session in sessions"
            :key="session.id"
            class="flex items-center justify-between bg-white rounded-lg border border-gray-300 hover:border-gray-900 px-4 py-2"
          >
            <div class="flex flex-1 px-4 py-2 space-x-4">
              <p class="text-sm text-gray-900"> {{ session.creation_date}} </p>
              <p class="text-sm text-gray-400"> {{ session.token }} </p>
            </div>

            <div class="flex space-x-4">
              <!-- Активировать/деактивировать -->
              <div class="relative group">
                <button
                  @click="deleteSession(session.id)"
                  class="p-2 text-gray-100 bg-red-600 rounded-md hover:bg-red-400 transition"
                >
                  <svg xmlns="http://www.w3.org/2000/svg"
                    :class="'w-4 h-4'"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <PowerIcon/>
                  </svg>
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <!--
    -->
  </div>
</template>

<script setup lang="ts">
  import ApiService from "@/common/api.service"
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import PowerIcon from "@/components/icons/PowerIcon.vue";

  const route = useRoute()
  const uid = route.query.user

  const user = ref<object>(null)

  const sessions = ref<object>(null)

  const newPassword = ref<string>("")

  onMounted(async () => {
    if (uid == null) return

    const uresponse = await ApiService.query(`/admin/get-user/${uid}`)
    if (!uresponse.data) return 
    user.value = uresponse.data 

    const sresponse = await ApiService.query(`/admin/user-sessions/${uid}`)
    if (!sresponse.data) return 
    sessions.value = sresponse.data

  })

  async function toggleActivation(user) {
    try {
      let result
      if (user.is_activated)
        result = await ApiService.post(`/admin/deactivate-user/${user.id}`);
      else 
        result = await ApiService.post(`/admin/activate-user/${user.id}`);
      if (result.data && result.data.success == true)
        user.is_activated = !user.is_activated;
    } catch {
      alert("error on activation change");
    }
  }

  async function deleteSession(id: int) {
    try {
      const result = await ApiService.post(`/admin/delete-session/${id}`)
    } catch (error) {
      alert("error on session deletion")
    }
  }

</script>
