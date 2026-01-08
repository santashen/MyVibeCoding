import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/crops',
    name: 'Crops',
    component: () => import('@/views/CropsView.vue')
  },
  {
    path: '/animals',
    name: 'Animals',
    component: () => import('@/views/AnimalsView.vue')
  },
  {
    path: '/flowers',
    name: 'Flowers',
    component: () => import('@/views/FlowersView.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/views/StatisticsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
