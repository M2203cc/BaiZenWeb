import axios from 'axios'

const baseURL = 'http://192.168.0.131:8080/api'

const api = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'accept': 'application/json',
    'Content-Type': 'application/json'
  }
})

export const influencersAPI = {
  // 获取达人数据
  getInfluencers: async (page = 1, size = 12) => {
    try {
      const response = await api.post(
        `/getdata/tkPersons?page=${page}&size=${size}`,
        {}
      )
      return response.data
    } catch (error) {
      console.error('Failed to fetch influencers:', error)
      throw error
    }
  },

  // 删除达人
  deleteInfluencer: async (params) => {
    try {
      const response = await api.delete('/deluser/deleteuser', { data: params })
      return response.data
    } catch (error) {
      console.error('Failed to delete influencer:', error)
      throw error
    }
  },

  // 修改获取邮箱的方法
  getEmail: async (handle) => {
    try {
      const response = await api.get(`/getemail?users=${handle}`)
      return response.data
    } catch (error) {
      // 如果是 404 错误，返回空结果而不是抛出错误
      if (error.response && error.response.status === 404) {
        return { code: 0, data: [] }
      }
      console.error('Failed to fetch email:', error)
      throw error
    }
  }
} 