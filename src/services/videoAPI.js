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

      const response = await axios.get(`${BASE_URL}/videos/by-date`, { 
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

  // 获取视频详情
  async getVideoDetail(videoId) {
    try {
      const response = await axios.get(`${BASE_URL}/videos/${videoId}`)
      return response.data
    } catch (error) {
      console.error('获取视频详情失败:', error)
      throw error
    }
  }
}

// 导出默认对象
export default videoAPI

// 同时提供具名导出
export { videoAPI }
