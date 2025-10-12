import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/test',
    name: 'test',
    component: () => import('@/views/TestView.vue')
  },
  {
    path: '/login',
    name: 'login',
    meta: {header: false},
    component: () => import('@/views/LoginPage.vue')
  },
  {
    path: '/register',
    name: 'register',
    meta: {header: false},
    component: () => import('@/views/RegisterPage.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/user/:id',
    name: 'home',
    component: () => import('@/views/UserView.vue'),
    props: true,
    children: [
      {
        path: '',
        name: 'user-home',
        component: () => import('@/views/ProfileView.vue'),
        props: true
      },
      {
        path: 'settings',
        name: 'user-settings',
        component: () => import('@/views/UserSettingsView.vue'),
        props: true
      }
    ]
  },
  {
    path: '/explore',
    name: 'explore',
    component: () => import('@/views/ExploreView.vue')
  },
  {
    path: '/editor/:id?',
    name: 'editor',
    meta: {header: false},
    component: () => import('@/views/EditorView.vue')
  },
  {
    path: '/welcome',
    name: 'welcome',
    component: () => import('@/views/WelcomePage.vue'),
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
    component: () => import('@/views/ActivateAccountPage.vue'),
  },
  {
    path: '/admin',
    children: [
      {
        path: '',
        name: 'admin-page',
        component: () => import('@/views/AdminView.vue')
      },
      {
        path: 'settings',
        name: 'admin-settings',
        component: () => import('@/views/AdminUserSettingsView.vue')
      }
    ]
  },
  {
    path: '/me',
    name: 'me',
    component: () => import('@/views/MeView.vue')
  },
  {
    path: '/auth-callback',
    name: 'auth-callback',
    component: () => import('@/views/AuthCallbackView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})


export default router
