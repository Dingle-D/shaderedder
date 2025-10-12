import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { VueReCaptcha } from 'vue-recaptcha-v3'

//import './style.css'
import './index.css'

import ApiService from "@/common/api.service";

ApiService.init();

router.beforeEach(async (to, from, next) => {
  await store.dispatch('CHECK_AUTH');
  if (to.meta.requresAuth && !store.getters.isAuthenticated) {
    console.error("Authorization required");
    next({ name: 'login' });
  } else {
    console.log("Authorized");
    next();
  }
});

const app = createApp(App);

app.use(VueReCaptcha, {
  siteKey: import.meta.env.VITE_RECAPTCHA_SITE_KEY,
})

app.use(store);
app.use(router);

app.mount('#app');

