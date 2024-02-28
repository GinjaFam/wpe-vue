import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Books from '../components/Books.vue'
import Map from '../components/Map.vue'

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
      name: 'Books',
      component: Books
    }
    ,
    {
      path: '/map',
      name: 'Map',
      component: Map
    }
  ]
})

export default router
