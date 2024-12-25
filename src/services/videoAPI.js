// 基本的 videoAPI 实现
const cookies = {
  '_gcl_au': '1.1.582945540.1733194843',
  'sb-btsplwsgjvpilxywmaba-auth-token': '["eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1NzhjYmI1YS0wN2U2LTQ4MTctYjI3Ni1hNWI3ZWJkZjU4ODkiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0OTM3MjQ3LCJpYXQiOjE3MzQ5MzM2NDcsImVtYWlsIjoibTIyMDNjQHByb3Rvbi5tZSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJtMjIwM2NAcHJvdG9uLm1lIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjU3OGNiYjVhLTA3ZTYtNDgxNy1iMjc2LWE1YjdlYmRmNTg4OSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzMzMTk0ODUzfV0sInNlc3Npb25faWQiOiI4MDZhZTY3NC0yZDhlLTQxODctYjE5Yi00MzBlYTFjZDc2OTkiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.j06DTqs7cd9HyHoJUx-ilzIoZF3W7iDnTJHm0SzV4fE","pQ5Cfu_W5ettVg6ZW8MPZQ",null,null,null]'
}

const videoAPI = {
  async getVideos(params) {
    const queryString = new URLSearchParams(params).toString()
    try {
      const response = await fetch(`/api/content-analysis/videos?${queryString}`, {
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

      console.log('Response Status:', response.status)
      
      const text = await response.text()
      console.log('Raw Response:', text)
      
      try {
        const data = JSON.parse(text)
        console.log('Parsed Data:', data)
        return data
      } catch (parseError) {
        console.error('JSON Parse Error:', parseError)
        throw new Error('Invalid JSON response')
      }
    } catch (error) {
      console.error('Error in getVideos:', error)
      throw error
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