import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://192.168.0.123:8080/api',
  timeout: 10000,
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
        timeout: 10000
      });
      
      // 检查响应数据的格式和内容
      if (response.data && response.data.code === 0 && response.data.data) {
        const emailData = response.data.data;
        // 检查是否有邮箱数据
        if (Array.isArray(emailData) && emailData.length > 0) {
          // 如果邮箱是 %XXXX@XXXX.com 格式，则返回空字符串
          const email = emailData[0].email;
          if (email && !email.includes('%XXXX@XXXX.com')) {
            return {
              code: 0,
              data: [{ email: email }]
            };
          }
        }
      }
      // 如果邮箱格式不正确或没有邮箱，返回空字符串
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