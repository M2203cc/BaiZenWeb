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

  // 添加获取视频详情的方法
  async getVideoDetails(videoId) {
    try {
      const response = await fetch(`/api/content-analysis/videos/${videoId}`, {
        method: 'GET',
        headers: {
          'accept': '*/*',
          'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'dnt': '1',
          'referer': 'https://app.euka.ai/content-analysis/videos',
          'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
          'x-requested-with': 'XMLHttpRequest'
        },
        credentials: 'include'
      })

      console.log('Video Details Response Status:', response.status)
      
      const text = await response.text()
      console.log('Raw Video Details Response:', text)
      
      try {
        const data = JSON.parse(text)
        console.log('Parsed Video Details:', data)
        return data
      } catch (parseError) {
        console.error('JSON Parse Error:', parseError)
        throw new Error('Invalid JSON response')
      }
    } catch (error) {
      console.error('Error fetching video details:', error)
      throw error
    }
  },

  // 修改获取视频人口统计数据的方法
  async getVideoDemographics(videoId) {
    try {
      const response = await fetch(`/api/content-analysis/demographics?video-ids=${videoId}`, {
        method: 'GET',
        headers: {
          'accept': '*/*',
          'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'dnt': '1',
          'referer': 'https://app.euka.ai/content-analysis/videos',
          'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        },
        credentials: 'include'
      })
      return response.json()
    } catch (error) {
      console.error('Error fetching demographics:', error)
      throw error
    }
  }
}

export default videoAPI 