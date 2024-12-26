import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false  // 不发送凭证
})

// 添加重试配置
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加重试配置
    config.retryCount = 0;
    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    // 打印请求信息
    console.log('Request:', {
      url: config.url,
      method: config.method,
      params: config.params,
      headers: config.headers
    })
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const { config, response } = error
    
    // 如果是超时错误并且还没有超过最大重试次数
    if (error.code === 'ECONNABORTED' && config && config.retryCount < MAX_RETRIES) {
      config.retryCount += 1;
      console.log(`Retrying request (${config.retryCount}/${MAX_RETRIES})...`);
      
      // 等待一段时间后重试
      await sleep(RETRY_DELAY * config.retryCount);
      return request(config);
    }

    if (response) {
      console.error('API Error:', response.status, response.data)
    } else if (error.request) {
      console.error('Network Error:', error.message)
    } else {
      console.error('Request Error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default request 