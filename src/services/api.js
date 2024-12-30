import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 添加 influencersAPI
export const influencersAPI = {
  async getInfluencers(page = 1, pageSize = 12) {
    try {
      const response = await api.get('/influencers', {
        params: {
          page,
          page_size: pageSize
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
      const response = await api.get(`/influencers/email`, {
        params: {
          users: handle
        }
      });
      
      if (response.data && response.data.code === 0 && response.data.data) {
        const emailData = response.data.data;
        if (Array.isArray(emailData) && emailData.length > 0) {
          const email = emailData[0].email;
          if (email && !email.includes('%XXXX@XXXX.com')) {
            return {
              code: 0,
              data: [{ email: email }]
            };
          }
        }
      }
      return { code: 0, data: [{ email: '' }] };
    } catch (error) {
      console.error('Failed to fetch email:', error);
      return { code: 0, data: [{ email: '' }] };
    }
  }
}

// 添加请求拦截器
api.interceptors.request.use(
  config => {
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