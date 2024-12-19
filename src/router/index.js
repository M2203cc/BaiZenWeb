import { createRouter, createWebHistory } from 'vue-router'
import Influencers from '../views/Influencers.vue'
import Lists from '../views/Lists.vue'
import ListDetail from '../views/ListDetail.vue'
import ProductDetail from '../views/ProductDetail.vue'
import Brands from '../views/Brands.vue'
import BrandDetail from '../views/BrandDetail.vue'
import CategoryDetail from '../views/CategoryDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/influencers'
  },
  {
    path: '/influencers',
    name: 'Influencers',
    component: () => import('../views/Influencers.vue'),
    meta: {
      keepAlive: true
    }
  },
  {
    path: '/lists',
    name: 'Lists',
    component: Lists
  },
  {
    path: '/lists/:id',
    name: 'ListDetail',
    component: ListDetail
  },
  {
    path: '/videos',
    name: 'Videos',
    component: () => import('../views/Videos.vue')
  },
  {
    path: '/brands',
    name: 'Brands',
    component: Brands
  },
  {
    path: '/brands/:id',
    name: 'BrandDetail',
    component: BrandDetail,
    props: true
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/Products.vue')
  },
  {
    path: '/categories',
    name: 'Categories',
    component: () => import('../views/Categories.vue')
  },
  {
    path: '/videos/:id',
    name: 'VideoDetail',
    component: () => import('../views/VideoDetail.vue')
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: ProductDetail
  },
  {
    path: '/categories/:name',
    name: 'CategoryDetail',
    component: CategoryDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 