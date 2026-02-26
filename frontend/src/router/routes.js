import { createRouter, createWebHistory } from 'vue-router'
import Kategorien from '../pages/Kategorien.vue'
import Aussagenpaare from '../pages/Aussagenpaare.vue'
import Admindashboard from '../pages/Admindashboard.vue'
import Login from '../pages/Login.vue'
import Startseite from '../pages/Startseite.vue'
import Uebungen from '../pages/Uebungen.vue'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/startseite',
    children: [
      {
        path: 'admindashboard',
        name: 'Admindashboard',
        component: Admindashboard
      },
      {
        path: 'aussagenpaare',
        name: 'Aussagenpaare',
        component: Aussagenpaare
      },
      {
        path: 'kategorien',
        name: 'Kategorien',
        component: Kategorien
      },
      {
        path: 'startseite',
        name: 'Startseite',
        component: Startseite
      },
      {
        path: 'uebungen',
        name: 'Übungen',
        component: Uebungen
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
