import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import MainMap from '../components/Map.vue'
import Home from '../components/Home.vue'
import Auth from '../components/Auth.vue'
import Navigation from '../components/Navigation.vue'
import Register from '../components/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/map',
      name: 'Map',
      component: MainMap
    },
    {
      path: '/auth',
      name: 'Auth',
      component: Auth
    },
    {
      path: '/navigation',
      name: 'Navigation',
      component: Navigation
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    }
  ]
})

export default router
