import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import MainMap from '../components/Map.vue'
import Home from '../components/Home.vue'
import Auth from '../components/Auth.vue'
import Navigation from '../components/Navigation.vue'
import Register from '../components/Register.vue'
import Login from '../components/Login.vue'
import Explorer from '../components/Explorer.vue'
import Watershed from '../components/Watershed.vue'

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
    },
    {
      path: '/login',
      name: 'Login',
      component: Login  
    },
    {
      path: '/explorer',
      name: 'Explorer',
      component: Explorer

    },
    {
      path: '/watershed',
      name: 'Watershed',
      component: Watershed,
    }

      

  ]
})

export default router
