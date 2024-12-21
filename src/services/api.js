import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://192.168.0.123:8080/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'accept': 'application/json'
  }
})

export const influencersAPI = {
  async getInfluencers(page = 1, pageSize = 12) {
    try {
      const response = await api.post('/getdata/tkPersons', {}, {
        params: {
          page,
          size: pageSize
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch influencers:', error);
      throw error;
    }
  },

  async getEmail(handle) {
    try {
      const response = await api.get(`/getemail`, {
        params: {
          users: handle
        },
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch email:', error);
      return { code: 0, data: [] };
    }
  }
}

// 添加请求拦截器
api.interceptors.request.use(
  config => {
    // 在这里可以添加认证信息等
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
      console.log('Request timeout');
    }
    return Promise.reject(error);
  }
);

export default api; 