import axios from 'axios'

// 添加缓存对象
const cache = {
  videos: new Map(),
  ttl: 5 * 60 * 1000 // 缓存有效期 5 分钟
}

const videoAPI = {
  async getVideos(page = 1, pageSize = 10, filters = {}) {
    try {
      const response = await axios.get('/api/content-analysis/videos', {
        params: {
          page,
          pageSize,
          search: filters.search || '',
          brand: filters.brand || '',
          product: filters.product || '',
          viewCount: filters.viewCount || ''
        },
        headers: {
          'accept': '*/*',
          'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching videos:', error);
      throw error;
    }
  },

  async getVideoDetails(videoId) {
    try {
      const response = await axios.get(`/api/content-analysis/videos/${videoId}`, {
        headers: {
          'accept': '*/*',
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching video details:', error);
      throw error;
    }
  },

  async getVideoDemographics(videoId) {
    try {
      const response = await axios.get('/api/content-analysis/demographics', {
        params: {
          'video-ids': videoId
        },
        headers: {
          'accept': '*/*',
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching video demographics:', error);
      throw error;
    }
  }
}

export default videoAPI; 