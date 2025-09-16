<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <h1 class="text-2xl font-bold mb-6">Настройки аккаунта</h1>

    <div class="flex flex-col lg:flex-row gap-6">
      <!-- Меню -->
      <div class="lg:w-1/4 w-full">

        <!-- Мобильное выпадающее меню -->
        <div class="mb-4 lg:hidden">
          <select
            v-model="selected"
            @change="handleSelectTabAndLayout"
            class="w-full bg-white border border-gray-900 rounded-md p-2 text-sm"
          >
            <option
              v-for="item in menu"
              :key="item.key"
              :value="item.key"
            >
              {{ item.label }}
            </option>
          </select>
        </div>

        <!-- Десктопное меню -->
        <div class="hidden lg:flex lg:flex-col gap-4">
          <button
            v-for="item in menu"
            :key="item.key"
            @click="changeTabAndLayout(item.key, item.comp)"
            class="px-4 py-2 rounded-lg border text-sm text-left transition-all duration-150"
            :class="selected === item.key
              ? 'bg-gray-900 text-white border-gray-900'
              : 'bg-white text-gray-800 border-gray-600 hover:bg-gray-100'"
          >
            {{ item.label }}
          </button>
        </div>

      </div>

      <!-- Контент -->
      <div class="flex-1 bg-white border border-gray-900 rounded-lg p-6">
        <component :is="tab" />
      </div>
    </div>
  </div>
</template>

<script setup>
// Никаких props/логики в этом базовом примере
import ProfileSettings from "@/components/settings/ProfileSettings.vue"
import EmailSettings from "@/components/settings/EmailSettings.vue"
import PasswordSettings from "@/components/settings/PasswordSettings.vue"
import { ref, markRaw } from 'vue'

// Элементы меню и соответствующие компоненты
const menu = [
  { key: 'profile', label: 'Profile', comp: ProfileSettings },
  { key: 'email', label: 'Email', comp: EmailSettings },
  { key: 'password', label: 'Password & API', comp: PasswordSettings },
]

const selected = ref('profile')
const tab = ref(null)

tab.value = markRaw(ProfileSettings)

function changeTabAndLayout(tab_name, layout) {
  selected.value = tab_name;
  tab.value = markRaw(layout);
}

function handleSelectTabAndLayout(event) {
  const selectedKey = event.target.value 
  const selectedItem = menu.find(item => item.key === selectedKey)

  if (selectedItem) {
    changeTabAndLayout(selectedItem.key, selectedItem.comp)
  }
  else {
    console.error("Could not find tab by requested key.")
  }
}

</script>


