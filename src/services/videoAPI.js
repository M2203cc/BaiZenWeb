import api from './api'

const videoAPI = {
  async getVideos(params) {
    try {
      const response = await api.get('/videos/by-date', { 
        params: {
          page: params.page || 1,
          page_size: params.page_size || 10,
          start_date: params.start_date,
          end_date: params.end_date,
          search: params.search
        }
      });
      
      // 确保返回格式符合预期
      return {
        data: response.data.data || [],
        total: response.data.total || 0,
        message: response.data.message
      };
    } catch (error) {
      console.error('Error in getVideos:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch videos');
    }
  },

  // 修改获取视频详情的方法
  async getVideoDetails(videoId) {
    try {
      // 使用 api 实例而不是直接使用 fetch
      const response = await api.get(`/videos/${videoId}`);
      
      // 直接返回响应数据
      return response.data;
    } catch (error) {
      console.error('Error fetching video details:', error);
      throw error;
    }
  },

  // 修改获取视频人口统计数据的方法
  async getVideoDemographics(videoId) {
    try {
      const response = await api.get(`/videos/${videoId}/demographics`);
      return response.data;
    } catch (error) {
      console.error('Error fetching demographics:', error);
      throw error;
    }
  }
}

export default videoAPI