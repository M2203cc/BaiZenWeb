import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VCalendar from 'v-calendar'
import 'v-calendar/dist/style.css'
import './assets/styles/main.css'

// 创建应用实例
const app = createApp(App)

// 注册插件
app.use(router)
app.use(store)
app.use(VCalendar, {})

// 挂载应用
app.mount('#app')