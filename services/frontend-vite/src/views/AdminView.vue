<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">Список пользователей</h2>

    <div v-if="loading" class="text-gray-500">Loading...</div>
    <div v-else-if="error" class="text-red-500">Error: {{ error }}</div>

    <ul v-else class="space-y-4">
      <li
        v-for="user in users"
        :key="user.id"
        class="flex items-center justify-between bg-white rounded-lg border border-gray-300 hover:border-gray-900 px-4 py-2"
      >
        <div>
          <div class="font-semibold text-lg">{{ user.username }}</div>
          <div class="text-sm text-gray-600">{{ user.email }} (id: {{user.id}})</div>
          <div class="text-xs text-gray-500 mt-1">
            State:
            <span :class="user.is_activated ? 'text-green-600' : 'text-red-600'">
              {{ user.is_activated ? 'Activated' : 'Deactivated' }}
            </span>
          </div>
        </div>

        <div class="flex space-x-4">
          <!-- Активировать/деактивировать -->
          <div class="relative group">
            <button
              @click="toggleActivation(user)"
              class="p-2 text-gray-100 bg-red-600 rounded-md hover:bg-red-400 transition"
            >
              <svg xmlns="http://www.w3.org/2000/svg"
                :class="'w-6 h-6'"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <PowerIcon/>
              </svg>
            </button>
            <span
              class="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 rounded bg-gray-800 text-white text-xs opacity-0 group-hover:opacity-100 transition"
            >
              Actiavte/Deactivate
            </span>
          </div>

          <div class="relative group">
            <button
              @click="userSettings(user)"
              class="p-2 text-gray-100 bg-gray-900 rounded-md hover:text-gray-400 transition"
            >
              Settings
            </button>
          </div>

          <!-- Сменить пароль -->
          <!-- 
          <div class="relative group">
            <button
              @click="changePassword(user)"
              class="p-2 rounded-full hover:bg-gray-100 transition"
            >
              <svg xmlns="http://www.w3.org/2000/svg"
                :class="'w-6 h-6'"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <PasswordIcon/>
              </svg>
            </button>
            <span
              class="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 rounded bg-gray-800 text-white text-xs opacity-0 group-hover:opacity-100 transition"
            >
              Change password
            </span>
          </div>
          -->

          <!-- Сменить имя -->
          <!--
          <div class="relative group">
            <button
              @click="changeName(user)"
              class="p-2 rounded-full hover:bg-gray-100 transition"
            >
              <svg xmlns="http://www.w3.org/2000/svg"
                :class="'w-6 h-6'"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <EditIcon/>
              </svg>
            </button>
            <span
              class="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 rounded bg-gray-800 text-white text-xs opacity-0 group-hover:opacity-100 transition"
            >
              Change username
            </span>
          </div>
          -->
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import ApiService from "@/common/api.service";
import PowerIcon from "@/components/icons/PowerIcon.vue";
import EditIcon from "@/components/icons/EditIcon.vue";
import PasswordIcon from "@/components/icons/PasswordIcon.vue";
import SettingsIcon from "@/components/icons/SettingsIcon.vue";

export default {
  name: "UserList",
  components: {
    PowerIcon,
    EditIcon,
    PasswordIcon
  },
  data() {
    return {
      users: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.error = null;
      try {
        const response = await ApiService.query(`admin/get-users`); // замени на реальный endpoint
        console.log("Response:", response)
        this.users = response.data.data;
      } catch (err) {
        console.error(err)
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    async toggleActivation(user, is_activated) {
      try {
        let result
        if (user.is_activated)
          result = await ApiService.post(`/admin/deactivate-user/${user.id}`);
        else 
          result = await ApiService.post(`/admin/activate-user/${user.id}`);
        if (result.data && result.data.success == true)
          user.is_activated = !user.is_activated;
      } catch {
        alert("Ошибка при смене статуса");
      }
    },
    async settings(user) {

    },
    async changePassword(user) {
      const newPassword = prompt(`Введите новый пароль для ${user.username}:`);
      if (!newPassword) return;
      try {
        await fetch(`/api/users/${user.id}/password`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ password: newPassword }),
        });
        alert("Пароль успешно изменен");
      } catch {
        alert("Ошибка при смене пароля");
      }
    },
    async changeName(user) {
      const newName = prompt(`Введите новое имя для ${user.username}:`);
      if (!newName) return;
      try {
        await fetch(`/api/users/${user.id}/name`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: newName }),
        });
        user.username = newName;
        alert("Имя успешно изменено");
      } catch {
        alert("Ошибка при смене имени");
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>
