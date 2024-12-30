import axios from 'axios'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const BASE_URL = 'http://localhost:8000'

// 将所有方法和工具函数放在一个对象中
const videoAPI = {
  // 获取视频列表
  async getVideosByDate(params = {}) {
    try {
      // 处理日期格式
      const formattedParams = {
        ...params,
        start_date: params.start_date ? params.start_date.toISOString().split('T')[0] : null,
        end_date: params.end_date ? params.end_date.toISOString().split('T')[0] : null,
        // 处理视图范围参数
        view_counts: params.view_counts ? params.view_counts.map(range => ({
          min: range[0],
          max: range[1] === Infinity ? null : range[1]
        })) : null
      }

      const response = await axios.get(`http://localhost:8000/videos/by-date`, { 
        params: formattedParams,
        // 添加错误处理配置
        validateStatus: function (status) {
          return status >= 200 && status < 500
        }
      })
      
      if (response.status === 200) {
        return {
          message: response.data.message,
          data: response.data.data.map(video => ({
            id: video.video_id,
            video_id: video.video_id,
            thumbnail_url: video.thumbnail_url,
            creator: video.creators?.handle || 'Unknown',
            creatorAvatar: video.creator_profile_url,
            posted_date: video.posted_date,
            views_count: video.views_count,
            likes_count: video.likes_count,
            description: video.description,
            product: video.seller_products?.title,
            productImage: video.seller_product_photo_url,
            brand: video.seller_products?.sellers?.name,
            brandImage: video.seller_photo_url
          })),
          total: response.data.total
        }
      } else {
        throw new Error(response.data.message || 'Failed to fetch videos')
      }
    } catch (error) {
      console.error('获取视频列表失败:', error)
      // 返回一个默认的空结果而不是抛出错误
      return {
        message: error.message || 'Failed to fetch videos',
        data: [],
        total: 0
      }
    }
  },

  // 格式化数字显示
  formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M'
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K'
    }
    return num.toString()
  },

  // 添加重试函数
  async retryRequest(fn, retries = 3, delay = 1000) {
    let lastError
    
    for (let i = 0; i < retries; i++) {
      try {
        return await fn()
      } catch (error) {
        lastError = error
        console.log(`Retry attempt ${i + 1} failed`)
        if (i < retries - 1) {
          await new Promise(resolve => setTimeout(resolve, delay))
        }
      }
    }
    
    throw lastError
  },

  // 获取视频详情
  async getVideoDetail(videoId) {
    return this.retryRequest(async () => {
      try {
        const response = await axios.get(`http://localhost:8000/videos/${videoId}`, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          timeout: 10000,  // 10秒超时
          validateStatus: function (status) {
            return status >= 200 && status < 500  // 允许任何非500的状态码
          }
        })

        // 打印响应信息以便调试
        console.log('API Response:', {
          status: response.status,
          statusText: response.statusText,
          data: response.data
        })

        if (response.status === 200 && response.data) {
          return response.data
        } else {
          throw new Error(
            response.data?.detail || 
            response.data?.message || 
            'Failed to fetch video details'
          )
        }
      } catch (error) {
        console.error('获取视频详情失败:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        })
        throw error
      }
    })
  },

  // 添加获取视频人口统计数据的方法
  async getVideoDemographics(videoId) {
    try {
      const response = await axios.get(`${BASE_URL}/videos/${videoId}/demographics`)
      return response
    } catch (error) {
      console.error('Error fetching video demographics:', error)
      throw error
    }
  }
}

// 导出默认对象
export default videoAPI

// 同时提供具名导出
export { videoAPI }
