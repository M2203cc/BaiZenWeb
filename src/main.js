import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/styles/main.css'
import * as echarts from 'echarts'
import VChart from 'vue-echarts'
import axios from 'axios'
import VCalendar from 'v-calendar';
import 'v-calendar/dist/style.css';

const app = createApp(App)
app.use(router)
app.use(store)
app.component('v-chart', VChart)

// 将 echarts 挂载到全局，方便在组件中使用
app.config.globalProperties.$echarts = echarts

// 配置 axios 默认值
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'

app.mount('#app') 
app.use(VCalendar, {});