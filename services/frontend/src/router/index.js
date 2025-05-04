import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginPage')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterPage')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/HomeView')
  },
  {
    path: '/welcome',
    name: 'welcome',
    component: () => import('@/views/WelcomePage'),
    meta: { requiresAuth: true }
  },
  {
    path: '/confirm-email',
    name: 'confirm-email',
    component: () => import('@/views/ConfirmEmailPage.vue')
  },
  {
    path: '/activate-account',
    name: 'activate-account',
    component: () => import('../views/ActivateAccountPage.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


export default router
